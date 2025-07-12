import os
import tempfile
# nosec: B404
import subprocess
from python_minifier import minify, RemoveAnnotationsOptions
import shutil

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

    ext = os.path.splitext(src_path)[1].lower()
    size_original += os.path.getsize(src_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if ext == ".py":
        with open(src_path, "r", encoding="utf-8") as f:
            source = f.read()

        minified = minify(source, filename=src_path, **options)

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(minified)
            tmp_path = tmp.name

        try:
            # nosec: B607 B603
            subprocess.run(["mpy-cross", tmp_path, "-o", out_path], check=True)
            compiled_files += 1
            size_output += os.path.getsize(out_path)
            print(f"Compiled and minified {src_path} -> {out_path}")
        # nosec: B110
        except subprocess.CalledProcessError:
            out_py = os.path.splitext(out_path)[0] + ".py"
            with open(out_py, "w", encoding="utf-8") as f:
                f.write(minified)
            not_compiled_files += 1
            size_output += os.path.getsize(out_py)
            print(f"mpy-cross failed, saved minified source as {out_py}")
        finally:
            os.remove(tmp_path)
    else:
        shutil.copy2(src_path, out_path)
        size_output += os.path.getsize(out_path)
        print(f"Copied {src_path} -> {out_path}")

def comp_folder(src_folder, out_folder):
    global total_files
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            total_files += 1
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, src_folder).replace("\\", "/")
            out_path = os.path.join(out_folder, rel_path)
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
