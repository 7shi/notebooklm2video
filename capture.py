import sys, os, time, pyautogui
import numpy as np

mx, my = 526, 864
rect = (80, 226, 800, 600)

p = 1
c = -1
args = sys.argv[1:]
try:
    while args:
        if args[0] == "-s":
            p = int(args[1])
            args = args[2:]
        elif args[0] == "-c":
            c = int(args[1])
            args = args[2:]
        else:
            raise Exception(f"unknown: {args[0]}")
except Exception as e:
    print(e, file=sys.stderr)
    print(f"Usage: python {sys.argv[0]} [-s start] [-c count]", file=sys.stderr)
    sys.exit(1)

outdir = "dst2"
if not os.path.exists(outdir):
    os.makedirs(outdir)

def images_are_equal(img1, img2):
    if img1 is None or img2 is None:
        return False
    return np.array_equal(img1, img2)

def fix_text(text):
    text2 = ""
    prev = ""
    for ch in text:
        if ch == " ":
            if prev and ord(prev) >= 0x800:
                continue
        else:
            prev = ch
        text2 += ch
    ret = ""
    for line in text2.split("\n") + [""]:
        line = line.strip()
        if line:
            ret += line
        elif not ret.endswith("\n"):
            ret += "\n"
    return ret

ok = True
while ok and c != 0:
    print(p)
    img = pyautogui.screenshot(region=rect)
    img.save(f"{outdir}/{p:03d}.png")
    p += 1
    c -= 1
    p1 = pyautogui.screenshot(region=rect)
    ok = False
    for i in range(3):
        if i:
            print("retry")
        pyautogui.click(mx, my)
        time.sleep(1)
        p2 = pyautogui.screenshot(region=rect)
        if not images_are_equal(p1, p2):
            ok = True
            break
