import sys

args = sys.argv[1:]
if len(args) != 2:
    print(f"Usage: python {sys.argv[0]} markdown header")
    sys.exit(1)

md = args[0]
h  = args[1].strip()

with open(md) as f:
    it = iter(f)
    while (line := next(it, None)) is not None:
        if line.strip() == h:
            first = True
            while (line := next(it, None)) and line.startswith("|"):
                if first:
                    first = False
                else:
                    print(line.strip())
