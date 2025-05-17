import os
from python_minifier import minify, RemoveAnnotationsOptions

SRC_DIR = "src"
OUT_DIR = "out"

options = dict(
    remove_annotations=RemoveAnnotationsOptions(
        remove_variable_annotations=True,
        remove_return_annotations=True,
        remove_argument_annotations=True,
        remove_class_attribute_annotations=False,
    ),
    remove_pass=True,
    remove_literal_statements=True,
    combine_imports=True,
    hoist_literals=True,
    rename_locals=True,
    preserve_locals=None,
    rename_globals=False,
    preserve_globals=None,
    remove_object_base=True,
    convert_posargs_to_args=True,
    preserve_shebang=True,
    remove_asserts=True,
    remove_debug=True,
    remove_explicit_return_none=False,
    remove_builtin_exception_brackets=True,
    constant_folding=True,
)

def minify_file(src_path, out_path):
    with open(src_path, "r", encoding="utf-8") as f:
        source = f.read()
    minified = minify(source, filename=src_path, **options)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(minified)
    print(f"Minified {src_path} -> {out_path}")

def minify_folder(src_folder, out_folder):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py"):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_folder)
                out_path = os.path.join(out_folder, rel_path)
                minify_file(src_path, out_path)

if __name__ == "__main__":
    minify_folder(SRC_DIR, OUT_DIR)
