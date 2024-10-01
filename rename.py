import sys, os

args = sys.argv[1:]
if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} <directory>", file=sys.stderr)
    sys.exit(1)

def rename(dir, src, dst):
    src1 = os.path.join(dir, src)
    dst1 = os.path.join(dir, dst)
    if os.path.exists(dst1):
        print(f"Error: {dst1} already exists")
        return
    os.rename(src1, dst1)

dir = args[0]
files1 = os.listdir(dir)
files1.sort(key=lambda x: os.path.getmtime(os.path.join(dir, x)))
files2 = []
for i, file in enumerate(files1):
    ext = os.path.splitext(file)[1]
    new_name = f"{i+1:03}{ext}"
    tmp_name = "tmp-" + new_name
    files2.append((file, tmp_name, new_name))
    rename(dir, file, tmp_name)
for file, tmp_name, new_name in files2:
    rename(dir, tmp_name, new_name)
    print(f"{file} -> {new_name}")
