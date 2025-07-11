import os
import tempfile
import subprocess
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

total_files = 0
compiled_files = 0
not_compiled_files = 0
size_original = 0
size_output = 0

def comp_file(src_path, out_path):
    global compiled_files, not_compiled_files, size_original, size_output

    with open(src_path, "r", encoding="utf-8") as f:
        source = f.read()
    size_original += len(source.encode("utf-8"))

    minified = minify(source, filename=src_path, **options)

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(minified)
        tmp_path = tmp.name

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        subprocess.run(["mpy-cross", tmp_path, "-o", out_path], check=True)
        compiled_files += 1
        size_output += os.path.getsize(out_path)
        print(f"Compiled and minified {src_path} -> {out_path}")
    except subprocess.CalledProcessError:
        out_py = os.path.splitext(out_path)[0] + ".py"
        with open(out_py, "w", encoding="utf-8") as f:
            f.write(minified)
        not_compiled_files += 1
        size_output += os.path.getsize(out_py)
        print(f"mpy-cross failed, saved minified source as {out_py}")

    os.remove(tmp_path)

def comp_folder(src_folder, out_folder):
    global total_files
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py"):
                total_files += 1
                rel_path = os.path.relpath(os.path.join(root, file), src_folder).replace("\\", "/")
                src_path = os.path.join(root, file)
                out_path = os.path.join(out_folder, os.path.splitext(rel_path)[0] + ".mpy")
                comp_file(src_path, out_path)

if __name__ == "__main__":
    comp_folder(SRC_DIR, OUT_DIR)

    print("\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Compiled to .mpy: {compiled_files}")
    print(f"Not compiled, saved as .py: {not_compiled_files}")
    print(f"Original total size: {size_original / 1024:.2f} KB")
    print(f"Output total size: {size_output / 1024:.2f} KB")
    if size_original > 0:
        saved = 100 * (size_original - size_output) / size_original
        print(f"Space saved: {saved:.2f}%")
