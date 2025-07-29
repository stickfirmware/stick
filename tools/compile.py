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

compilations = 0
total_files = 0
compiled_files = 0
not_compiled_files = 0
size_original = 0
size_minified = 0
size_output = 0

def comp_file(src_path, out_folder):
    global compiled_files, not_compiled_files, size_original, size_minified, size_output

    ext = os.path.splitext(src_path)[1].lower()
    size_original += os.path.getsize(src_path)

    rel_path = os.path.relpath(src_path, SRC_DIR).replace("\\", "/")
    base_name = os.path.splitext(rel_path)[0]
    
    if ext == ".py" and not rel_path.endswith("main.py"):
        with open(src_path, "r", encoding="utf-8") as f:
            source = f.read()

        minified = minify(source, filename=src_path, **options)
        size_minified += len(minified.encode("utf-8"))

        os.makedirs(os.path.join(out_folder, os.path.dirname(rel_path)), exist_ok=True)

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(minified)
            tmp_path = tmp.name

        out_mpy_path = os.path.join(out_folder, base_name + ".mpy")
        out_py_path = os.path.join(out_folder, rel_path)

        try:
            subprocess.run(["mpy-cross", tmp_path, "-o", out_mpy_path, "-march=xtensawin"], check=True)
            compiled_files += 1
            size_output += os.path.getsize(out_mpy_path)
            print(f"Compiled and minified {src_path} -> {out_mpy_path}")
        except subprocess.CalledProcessError:
            with open(out_py_path, "w", encoding="utf-8") as f:
                f.write(minified)
            not_compiled_files += 1
            size_output += os.path.getsize(out_py_path)
            print(f"mpy-cross failed, saved minified source as {out_py_path}")
        finally:
            os.remove(tmp_path)

    else:
        out_other_path = os.path.join(out_folder, rel_path)
        os.makedirs(os.path.dirname(out_other_path), exist_ok=True)
        shutil.copy2(src_path, out_other_path)
        size_output += os.path.getsize(out_other_path)
        print(f"Copied {src_path} -> {out_other_path}")

def comp_folder(src_folder, out_folder):
    global total_files
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            total_files += 1
            src_path = os.path.join(root, file)
            comp_file(src_path, out_folder)

if __name__ == "__main__":
    print("Stick firmware compile script")
    l_dir = os.listdir("./configs")
    for file in l_dir:
        if file.endswith(".py"):
            total_files = 0
            compiled_files = 0
            not_compiled_files = 0
            size_original = 0
            size_minified = 0
            size_output = 0
            print("Compilation started for: " + str(file))
            if "osconstants.py" in os.listdir("./src/modules"):
                try:
                    os.remove("./src/modules/os-constants.py")
                except FileNotFoundError:
                    pass
            try:
                os.rename(os.path.join("./configs", file), "./src/modules/os_constants.py")
            except Exception as e:
                continue
            compilations += 1
            comp_folder(SRC_DIR, os.path.join(OUT_DIR, file.replace(".py","")))
            print("\nBuild summary:")
            print(f"Total files processed: {total_files}")
            print(f"Compiled to .mpy: {compiled_files}")
            print(f"Not compiled, saved as .py: {not_compiled_files}")
            print(f"Original total size (all files): {size_original / 1024:.2f} KB")
            print(f"Minified .py total size: {size_minified / 1024:.2f} KB")
            print(f"Output total size (.mpy + copied files): {size_output / 1024:.2f} KB")

            if size_original > 0:
                saved = 100 * (size_original - size_output) / size_original
                print(f"Space saved by mpy-cross: {saved:.2f}%")
    print("\nScript summary:")
    print("Builds: " + str(compilations))
