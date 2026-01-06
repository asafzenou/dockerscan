"""
Filesystem reconstruction from Docker image layers.

- Supports OCI and legacy docker save formats
- Handles nested layer.tar
- Extracts only relevant filesystem paths (fast & safe)
"""

import json
import tarfile
from pathlib import Path
from dockerscan.logger import Logger
from dockerscan.config.os_packages import RELEVANT_PATHS



def reconstruct_filesystem(extract_dir: Path, filesystem_dir: Path) -> None:
    """
    Reconstruct merged filesystem from Docker image layers.
    Later layers override earlier ones (Docker semantics).
    """

    filesystem_dir.mkdir(parents=True, exist_ok=True)

    layer_tars = _load_docker_layers(extract_dir)

    Logger().info(f"Path: {filesystem_dir}")
    Logger().info(f"Reconstructing filesystem from {len(layer_tars)} layers")


    for i, layer_tar in enumerate(layer_tars, 1):
        Logger().info(f"    Applying layer {i}/{len(layer_tars)}: {layer_tar.name}")
        _apply_layer(layer_tar, filesystem_dir)


# =============================================================================
# Layer handling
# =============================================================================

def _apply_layer(layer_tar: Path, filesystem_dir: Path) -> None:
    """
    Apply a single Docker layer.
    Handles both direct filesystem tars and wrapper tars containing layer.tar.
    """

    if not layer_tar.exists():
        raise RuntimeError(f"Layer not found: {layer_tar}")

    with tarfile.open(layer_tar, "r:*") as tar:
        inner_layer = _find_inner_layer_tar(tar)

        if inner_layer:
            Logger().debug("Found nested layer.tar")
            with tarfile.open(fileobj=tar.extractfile(inner_layer), mode="r:*") as inner_tar:
                _extract_relevant(inner_tar, filesystem_dir)
        else:
            _extract_relevant(tar, filesystem_dir)


def _find_inner_layer_tar(tar: tarfile.TarFile):
    """
    Detect nested layer.tar inside OCI / docker layer wrapper.
    """
    for member in tar:
        name = member.name.lstrip("./")
        if name == "layer.tar":
            return member
    return None


# =============================================================================
# Extraction logic
# =============================================================================

def _extract_relevant(tar: tarfile.TarFile, filesystem_dir: Path) -> None:
    """
    Extract only relevant filesystem paths from a tar archive.
    """

    for member in tar:
        name = member.name.lstrip("./")

        if not _is_relevant(name):
            continue

        try:
            # Normalize metadata (Windows-safe)
            member.uid = 0
            member.gid = 0
            member.uname = ""
            member.gname = ""
            member.mode = 0o644 if member.isfile() else 0o755

            tar.extract(member, path=filesystem_dir, set_attrs=False)

        except Exception as e:
            Logger().debug(f"Skip {name}: {e}")


def _is_relevant(member_name: str) -> bool:
    """
    Check if a tar member path is relevant for package / OS scanning.
    """
    return any(
        member_name == p or member_name.startswith(p + "/")
        for p in RELEVANT_PATHS
    )


# =============================================================================
# Manifest handling
# =============================================================================

def _load_docker_layers(extract_dir: Path) -> list[Path]:
    """
    Load filesystem layer tar files from docker save output.

    Supports:
    - OCI layout (modern docker)
    - Legacy docker save format
    """

    manifest_path = extract_dir / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("manifest.json not found")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # -------------------------------------------------------------------------
    # OCI format
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Legacy docker save format
    # -------------------------------------------------------------------------
    if isinstance(manifest, list) and manifest:
        image = manifest[0]
        layers = image.get("Layers")

        if not layers:
            raise RuntimeError("No Layers found in legacy manifest")

        return [extract_dir / layer for layer in layers]

    raise RuntimeError("Unsupported manifest.json format")
