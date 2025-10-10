"""Export OpenAPI specification from FastAPI app."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app


def export_openapi() -> None:
    """Export OpenAPI spec to JSON file."""
    spec = app.openapi()

    output_path = Path(__file__).parent.parent / "openapi.json"
    with open(output_path, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"OpenAPI spec exported to {output_path}")


if __name__ == "__main__":
    export_openapi()
