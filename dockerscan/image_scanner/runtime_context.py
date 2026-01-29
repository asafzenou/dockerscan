import subprocess
import json


class RuntimeContextExtractor:
    def extract(self, image_name: str) -> dict:
        inspect_output = subprocess.check_output(
            ["docker", "inspect", image_name],
            text=True
        )
        inspect_data = json.loads(inspect_output)[0]

        config = inspect_data.get("Config", {})

        return {
            "entrypoint": config.get("Entrypoint") or [],
            "cmd": config.get("Cmd") or [],
            "user": {
                "value": config.get("User") or "root",
                "source": "image_default" if not config.get("User") else "image_explicit"
            },
            "exposed_ports": list((config.get("ExposedPorts") or {}).keys())
        }

