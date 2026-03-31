import subprocess
import json

def run_checkov(file_path):
    try:
        result = subprocess.run(
            ["checkov", "-f", file_path, "--output", "json"],
            capture_output=True,
            text=True
        )

        data = json.loads(result.stdout)

        issues = []
        severity_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

        for check in data.get("results", {}).get("failed_checks", []):
            severity = check.get("severity", "LOW")

            severity_count[severity] = severity_count.get(severity, 0) + 1

            issues.append({
                "id": check.get("check_id"),
                "title": check.get("check_name"),
                "severity": severity,
                "file": check.get("file_path"),
                "fix_hint": "Refer Checkov docs or fix configuration"
            })

        return {
            "summary": {
                "total": len(issues),
                "high": severity_count.get("HIGH", 0),
                "medium": severity_count.get("MEDIUM", 0),
                "low": severity_count.get("LOW", 0)
            },
            "issues": issues
        }

    except Exception as e:
        return {"error": str(e)}