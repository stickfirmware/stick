import os
import pdoc

MODULES_DIR = "src/modules"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

for root, _, files in os.walk(MODULES_DIR):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, MODULES_DIR)
            name = os.path.splitext(rel_path)[0].replace(os.sep, "_")
            output_file = os.path.join(DOCS_DIR, f"{name}.md")
            print(f"Generating {output_file} from {path}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(pdoc.render_markdown(path))
