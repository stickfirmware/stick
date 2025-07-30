import os
import subprocess
import shutil

SRC_DIR = "src"
OUT_DIR = "out"

compilations = 0
total_files = 0
compiled_files = 0
not_compiled_files = 0
size_original = 0
size_output = 0

def comp_file(src_path, out_folder):
    global compiled_files, not_compiled_files, size_original, size_output

    ext = os.path.splitext(src_path)[1].lower()
    size_original += os.path.getsize(src_path)

    rel_path = os.path.relpath(src_path, SRC_DIR).replace("\\", "/")
    base_name = os.path.splitext(rel_path)[0]

    if ext == ".py" and not rel_path.endswith("main.py"):
        out_mpy_path = os.path.join(out_folder, base_name + ".mpy")
        os.makedirs(os.path.dirname(out_mpy_path), exist_ok=True)
        subprocess.run(["mpy-cross", src_path, "-o", out_mpy_path, "-march=xtensawin"], check=True)
        compiled_files += 1
        size_output += os.path.getsize(out_mpy_path)
        print(f"Compiled {src_path} -> {out_mpy_path}")
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
    for file in os.listdir("./configs"):
        if file.endswith(".py"):
            total_files = 0
            compiled_files = 0
            not_compiled_files = 0
            size_original = 0
            size_output = 0

            print(f"\nCompilation started for: {file}")

            try:
                os.remove("./src/modules/os_constants.py")
            except FileNotFoundError:
                pass

            try:
                os.rename(os.path.join("./configs", file), "./src/modules/os_constants.py")
            except Exception as e:
                print(f"Failed to apply config {file}: {e}")
                continue

            compilations += 1
            comp_folder(SRC_DIR, os.path.join(OUT_DIR, file.replace(".py", "")))

            print("\nBuild summary:")
            print(f"Total files processed: {total_files}")
            print(f"Compiled to .mpy: {compiled_files}")
            print(f"Not compiled, saved as .py: {not_compiled_files}")
            print(f"Original total size: {size_original / 1024:.2f} KB")
            print(f"Output total size: {size_output / 1024:.2f} KB")

            if size_original > 0:
                saved = 100 * (size_original - size_output) / size_original
                print(f"Space saved: {saved:.2f}%")

    print("\nScript summary:")
    print(f"Builds: {compilations}")
