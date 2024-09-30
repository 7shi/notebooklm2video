import os, time, pyautogui
import numpy as np

mx, my = 526, 864
rect = (80, 226, 800, 600)

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

p = 1
ok = True
while ok:
    print(p)
    img = pyautogui.screenshot(region=rect)
    img.save(f"{outdir}/{p:03d}.png")
    p += 1
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
