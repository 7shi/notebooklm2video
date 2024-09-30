import sys, os

args = sys.argv[1:]
if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} <directory>", file=sys.stderr)
    sys.exit(1)

dir = args[0]
files = os.listdir(dir)
files.sort(key=lambda x: os.path.getmtime(os.path.join(dir, x)))
for i, file in enumerate(files):
    ext = os.path.splitext(file)[1]
    new_name = f"{i+1:03}{ext}"
    os.rename(os.path.join(dir, file), os.path.join(dir, new_name))
    print(f"{file} -> {new_name}")
