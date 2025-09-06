# tools/gen_docs.py
import pathlib
import sys
import pdoc

MODULES_DIR = pathlib.Path("src/modules")
DOCS_DIR = pathlib.Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(MODULES_DIR))

for file in MODULES_DIR.rglob("*.py"):
    module_name = file.stem
    print(f"Generating docs/{module_name}.md from {file}")

    try:
        module = __import__(module_name)
        md = pdoc.render_markdown(pdoc.Module(module))
        with open(DOCS_DIR / f"{module_name}.md", "w", encoding="utf-8") as f:
            f.write(md)
    except Exception as e:
        print(f"Failed to generate docs for {module_name}: {e}"
