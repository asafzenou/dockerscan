"""Filesystem reconstruction from Docker layers."""

import json
from pathlib import Path
import shutil


def reconstruct_filesystem(extract_dir: Path, filesystem_dir: Path) -> None:
    """
    Reconstruct merged filesystem from Docker layers.
    
    Docker images are stored as layers. Each layer has a directory with files.
    We need to merge all layers in order, with later layers overriding earlier ones.
    
    Args:
        extract_dir: Directory containing extracted Docker image
        filesystem_dir: Directory where merged filesystem will be created
    """
    filesystem_dir.mkdir(parents=True, exist_ok=True)
    
    # Find manifest.json to get layer order
    manifest_path = extract_dir / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"manifest.json not found in {extract_dir}")
    
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    if not manifest:
        raise RuntimeError("Empty manifest.json")
    
    # Get the first image's layers (assuming single image in manifest)
    image_data = manifest[0]
    layer_tar_files = image_data.get("Layers", [])
    
    if not layer_tar_files:
        raise RuntimeError("No layers found in manifest")
    
    print(f"  Found {len(layer_tar_files)} layers")
    
    # Process layers in order
    for layer_tar in layer_tar_files:
        layer_path = extract_dir / layer_tar
        if not layer_path.exists():
            raise RuntimeError(f"Layer not found: {layer_path}")
        
        # Extract layer tar to temporary directory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_layer_dir:
            import tarfile
            with tarfile.open(layer_path, "r") as tar:
                tar.extractall(path=temp_layer_dir)
            
            # Merge layer contents into filesystem
            layer_root = Path(temp_layer_dir)
            # Docker layers typically have a rootfs directory or files at root
            if (layer_root / "layer.tar").exists():
                # Some formats have nested layer.tar
                with tarfile.open(layer_root / "layer.tar", "r") as nested_tar:
                    nested_tar.extractall(path=filesystem_dir)
            else:
                # Direct extraction - merge directories
                _merge_directory(layer_root, filesystem_dir)


def _merge_directory(source: Path, destination: Path) -> None:
    """
    Merge source directory into destination, with source taking precedence.
    
    Args:
        source: Source directory to merge from
        destination: Destination directory to merge into
    """
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

