"""Filesystem reconstruction from Docker layers."""

import json
from pathlib import Path
import shutil
from dockerscan.logger import Logger
import tempfile
import tarfile


def reconstruct_filesystem(extract_dir: Path, filesystem_dir: Path) -> None:
    """Reconstruct merged filesystem from Docker layers.
    Docker images are stored as layers. Each layer has a directory with files.
    We need to merge all layers in order, with later layers overriding earlier ones."""
    filesystem_dir.mkdir(parents=True, exist_ok=True)
    
    manifest_path = extract_dir / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"manifest.json not found in {extract_dir}")
    
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    if not manifest:
        raise RuntimeError("Empty manifest.json")
    
    image_data = manifest[0]
    layer_tar_files = image_data.get("Layers", [])
    
    if not layer_tar_files:
        raise RuntimeError("No layers found in manifest")
    
    Logger().info(f"  Found {len(layer_tar_files)} layers")
    
    for layer_tar in layer_tar_files:
        layer_path = extract_dir / layer_tar
        if not layer_path.exists():
            raise RuntimeError(f"Layer not found: {layer_path}")
        
        with tempfile.TemporaryDirectory() as temp_layer_dir:
            with tarfile.open(layer_path, "r") as tar:
                # members = [
                #     m for m in tar.getmembers()
                #     if m.name.startswith("etc/")
                # ]
                members = [
                    m for m in tar.getmembers()
                    if m.name in ("etc/os-release", "usr/lib/os-release")
                ]
                tar.extractall(path=temp_layer_dir, members=members)

            layer_root = Path(temp_layer_dir)
            if (layer_root / "layer.tar").exists():
                with tarfile.open(layer_root / "layer.tar", "r") as nested_tar:
                    # nested_tar.extractall(path=filesystem_dir)
                    members = [
                        m for m in tar.getmembers()
                        if m.name in ("etc/os-release", "usr/lib/os-release")
                    ]
                    tar.extractall(path=temp_layer_dir, members=members)
            else:
                _merge_directory(layer_root, filesystem_dir)


def _merge_directory(source: Path, destination: Path) -> None:
    """Merge source directory into destination, with source taking precedence."""
    for item in source.iterdir():
        dest_item = destination / item.name
        
        if item.is_dir():
            if dest_item.exists() and dest_item.is_dir():
                _merge_directory(item, dest_item)
            else:
                if dest_item.exists():
                    dest_item.unlink()
                shutil.copytree(item, dest_item)
        else:
            if dest_item.exists() and dest_item.is_dir():
                shutil.rmtree(dest_item)
            shutil.copy2(item, dest_item)

