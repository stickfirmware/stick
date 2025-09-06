import pdoc
import pathlib

MODULES_DIR = "src/modules"
DOCS_DIR = "docs"

pathlib.Path(DOCS_DIR).mkdir(exist_ok=True)

for root, _, files in os.walk(MODULES_DIR):
    for file in files:
        if file.endswith(".py"):
            full_path = pathlib.Path(root) / file
            rel_path = full_path.relative_to(MODULES_DIR)
            name = str(rel_path).replace(".py", "").replace("/", "_")
            output_file = pathlib.Path(DOCS_DIR) / f"{name}.md"

            print(f"Generating {output_file} from {full_path}")

            module = pdoc.Module(full_path)
            md = pdoc.render_markdown(module)
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(md)
