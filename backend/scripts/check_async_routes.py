import re
import sys
from pathlib import Path


def check_file_for_sync_routes(file_path: Path) -> list[tuple[int, str]]:
    content = file_path.read_text()
    lines = content.split('\n')

    sync_routes = []

    for i, line in enumerate(lines, 1):
        if re.match(r'^\s*@router\.(get|post|put|patch|delete)', line):
            for j in range(i, min(i + 5, len(lines) + 1)):
                next_line = lines[j - 1]
                if re.match(r'^\s*async\s+def\s+(\w+)', next_line):
                    break
                match = re.match(r'^\s*def\s+(\w+)', next_line)
                if match:
                    func_name = match.group(1)
                    sync_routes.append((j, func_name))
                    break

    return sync_routes


def main() -> int:
    backend_dir = Path(__file__).parent.parent
    routers_dir = backend_dir / "app" / "api" / "routers"

    if not routers_dir.exists():
        print(f"❌ Routers directory not found: {routers_dir}")
        return 1

    all_sync_routes = []

    for router_file in routers_dir.glob("*.py"):
        if router_file.name == "__init__.py":
            continue

        sync_routes = check_file_for_sync_routes(router_file)
        if sync_routes:
            all_sync_routes.append((router_file, sync_routes))

    if all_sync_routes:
        print("❌ ASYNC GUARD FAILED: Found synchronous route handlers!")
        print("\nAll FastAPI routes must be async per NFR-007.")
        print("\nViolations found:")
        for file_path, sync_routes in all_sync_routes:
            print(f"\n📁 {file_path.relative_to(backend_dir)}:")
            for line_num, func_name in sync_routes:
                print(f"  Line {line_num}: def {func_name}() - must be async!")
        return 1

    print("✅ ASYNC GUARD PASSED: All route handlers are async!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
