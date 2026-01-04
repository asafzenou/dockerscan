# dockerscan

A minimal MVP Docker image scanner that detects OS information from Docker images.

## Installation

```bash
pip install -e .
```

## Usage

```bash
dockerscan scan <image_name>
```

Example:
```bash
dockerscan scan ubuntu:20.04
```

## What it does

1. Saves the Docker image using `docker save`
2. Extracts the image tar archive
3. Reconstructs the merged filesystem from Docker layers
4. Reads `/etc/os-release` from the filesystem
5. Prints the detected OS name and version

## Example Output

```
Scanning Docker image: ubuntu:20.04
Extracting image to temporary directory...
  Running: docker save ubuntu:20.04
  Extracting tar archive...
Reconstructing filesystem from layers...
  Found 3 layers
Detecting OS...
Detected OS: Ubuntu 20.04.6 LTS
```

## Requirements

- Python 3.11+
- Docker installed and running
- The Docker image must exist locally or be pullable
