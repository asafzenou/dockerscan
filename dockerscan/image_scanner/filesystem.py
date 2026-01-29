import json
from dockerscan.config.os_packages import RELEVANT_PATHS
import subprocess
import tarfile
from pathlib import Path
import tempfile
from dockerscan.config.logger import Logger

class Filesystem:

    def save_and_extract_image(self, image_name: str, extract_dir: Path) -> None:
        """Save Docker image to tar and extract it"""
        extract_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as temp_tar:
            temp_tar_path = temp_tar.name

        try:
            Logger().info(f"Running: docker save {image_name}")
            with open(temp_tar_path, "wb") as tar_file:
                result = subprocess.run(
                    ["docker", "save", image_name],
                    stdout=tar_file,
                    stderr=subprocess.PIPE,
                    check=True
                )

            with tarfile.open(temp_tar_path, "r") as tar:
                tar.extractall(path=extract_dir)

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else "Unknown error"
            raise RuntimeError(f"Failed to save Docker image: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract image: {e}")
        finally:
            Path(temp_tar_path).unlink(missing_ok=True)

    def reconstruct_filesystem(self, extract_dir: Path, filesystem_dir: Path) -> None:
        """
        Reconstruct merged filesystem from Docker image layers.
        Later layers override earlier ones (Docker semantics).
        """

        filesystem_dir.mkdir(parents=True, exist_ok=True)

        layer_tars = self._load_docker_layers(extract_dir)

        Logger().info(f"Path: {filesystem_dir}")
        Logger().info(f"Reconstructing filesystem from {len(layer_tars)} layers")


        for i, layer_tar in enumerate(layer_tars, 1):
            Logger().info(f"    Applying layer {i}/{len(layer_tars)}: {layer_tar.name}")
            self._apply_layer(layer_tar, filesystem_dir)


    def _apply_layer(self, layer_tar: Path, filesystem_dir: Path) -> None:
        """
        Apply a single Docker layer. Handles both direct filesystem tars and wrapper tars containing layer.tar.
        """

        if not layer_tar.exists():
            raise RuntimeError(f"Layer not found: {layer_tar}")

        with tarfile.open(layer_tar, "r:*") as tar:
            inner_layer = self._find_inner_layer_tar(tar)

            if inner_layer:
                Logger().debug("Found nested layer.tar")
                with tarfile.open(fileobj=tar.extractfile(inner_layer), mode="r:*") as inner_tar:
                    self._extract_relevant(inner_tar, filesystem_dir)
            else:
                self._extract_relevant(tar, filesystem_dir)


    def _find_inner_layer_tar(self, tar: tarfile.TarFile):
        """
        Detect nested layer.tar inside OCI / docker layer wrapper.
        """
        for member in tar:
            name = member.name.lstrip("./")
            if name == "layer.tar":
                return member
        return None


    def _extract_relevant(self, tar: tarfile.TarFile, filesystem_dir: Path) -> None:
        """
        Extract only relevant filesystem paths from a tar archive.
        """

        for member in tar:
            name = member.name.lstrip("./")

            if not self._is_relevant(name):
                continue

            try:
                member.uid = 0
                member.gid = 0
                member.uname = ""
                member.gname = ""
                member.mode = 0o644 if member.isfile() else 0o755

                tar.extract(member, path=filesystem_dir, set_attrs=False)

            except Exception as e:
                Logger().debug(f"Skip {name}: {e}")


    def _is_relevant(self, member_name: str) -> bool:
        """
        Check if a tar member path is relevant for package / OS scanning.
        """
        return any(
            member_name == p or member_name.startswith(p + "/")
            for p in RELEVANT_PATHS
        )

    def _load_docker_layers(self, extract_dir: Path) -> list[Path]:
        """Load filesystem layer tar files from docker save output."""

        manifest_path = extract_dir / "manifest.json"
        if not manifest_path.exists():
            raise RuntimeError("manifest.json not found")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        if isinstance(manifest, dict) and "layers" in manifest:
            blobs_dir = extract_dir / "blobs" / "sha256"
            layer_paths: list[Path] = []

            for layer in manifest["layers"]:
                media_type = layer.get("mediaType", "")
                if "layer" not in media_type:
                    continue

                digest = layer["digest"].replace("sha256:", "")
                layer_path = blobs_dir / digest

                if not layer_path.exists():
                    raise RuntimeError(f"Layer blob not found: {digest}")

                layer_paths.append(layer_path)

            return layer_paths

        if isinstance(manifest, list) and manifest:
            image = manifest[0]
            layers = image.get("Layers")

            if not layers:
                raise RuntimeError("No Layers found in legacy manifest")

            return [extract_dir / layer for layer in layers]

        raise RuntimeError("Unsupported manifest.json format")
