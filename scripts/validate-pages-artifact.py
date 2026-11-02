"""Reject incomplete Hugo output and repository sources before Pages upload."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
errors = []
for language in ("", "pt-br/"):
    for page in ("", "about/", "articles/", "projects/", "contact/"):
        target = root / language / page / "index.html"
        if not target.is_file() or target.stat().st_size == 0:
            errors.append(f"Missing institutional HTML: {target} (check draft approval)")

for path in root.rglob("*"):
    relative = path.relative_to(root)
    if path.is_symlink():
        errors.append(f"Symbolic link is not allowed: {relative}")
    if any(part.startswith(".") for part in relative.parts):
        errors.append(f"Hidden repository file/directory: {relative}")
    if path.is_file() and (
        path.suffix.lower() in {".md", ".markdown", ".toml", ".yaml", ".yml"}
        or path.name.lower().startswith("readme")
        or path.name in {"go.mod", "go.sum", "Makefile", "Dockerfile.dev"}
    ):
        errors.append(f"Repository source/configuration is not allowed: {relative}")
    if path.is_file() and "foundation-example" in relative.parts:
        errors.append(f"Demonstration output is not allowed: {relative}")

if errors:
    sys.exit("\n".join(errors))
print("Pages artifact validated: both languages, institutional HTML, no repository sources.")
