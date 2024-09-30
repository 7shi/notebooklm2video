import sys, os

a, b = sys.argv[1:]

def add_(fn):
    fn, ext = os.path.splitext(fn)
    return fn + "_" + ext

with open(a, "r") as f:
    ta = [[col.strip() for col in l.split("|")[1:-1]] for line in f if (l := line.strip())]
with open(b, "r") as f:
    tb = [[col.strip() for col in l.split("|")[1:-1]] for line in f if (l := line.strip())]

with open(add_(a), "w") as f:
    for r in ta:
        print(("0" + r[0])[-5:], "|", r[1], "|", r[2], file=f)
with open(add_(b), "w") as f:
    for r in tb:
        print(("0" + r[0])[-5:], "|", r[1], "|", r[2], file=f)

print(len(ta), len(tb))
