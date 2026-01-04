"""Docker image save and extraction logic."""

import subprocess
import tarfile
from pathlib import Path
import tempfile


def save_and_extract_image(image_name: str, extract_dir: Path) -> None:
    """
    Save Docker image to tar and extract it.
    
    Args:
        image_name: Name of the Docker image to save
        extract_dir: Directory where the extracted image will be placed
    """
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    # Create temporary tar file
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as temp_tar:
        temp_tar_path = temp_tar.name
    
    try:
        # Run docker save and write directly to tar file
        print(f"  Running: docker save {image_name}")
        with open(temp_tar_path, "wb") as tar_file:
            result = subprocess.run(
                ["docker", "save", image_name],
                stdout=tar_file,
                stderr=subprocess.PIPE,
                check=True
            )
        
        # Extract the tar file
        print(f"  Extracting tar archive...")
        with tarfile.open(temp_tar_path, "r") as tar:
            tar.extractall(path=extract_dir)
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        raise RuntimeError(f"Failed to save Docker image: {error_msg}")
    except Exception as e:
        raise RuntimeError(f"Failed to extract image: {e}")
    finally:
        # Clean up temporary tar file
        Path(temp_tar_path).unlink(missing_ok=True)

