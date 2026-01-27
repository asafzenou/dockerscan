class PackageUsageResolver:
    def resolve(self, package_name: str, runtime_context: dict) -> dict:
        runtime_cmd = (
            runtime_context.get("cmd", []) +
            runtime_context.get("entrypoint", [])
        )

        referenced = any(
            package_name.lower() in part.lower()
            for part in runtime_cmd
        )

        return {
            "used_at_runtime": referenced,
            "confidence": "high" if referenced else "low",
            "source": "cmd_entrypoint_analysis"
        }
