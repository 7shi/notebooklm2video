import re

def make_table(filename):
    with open(filename, "r") as f:
        table = []
        cols = 0
        for line in f:
            line = line.strip()
            if line:
                data = [item.strip() for item in line.split("|")[1:-1]]
                if cols == 0:
                    cols = len(data)
                while len(data) < cols:
                    data.append("")
                table.append(data)
    return table

def write_text(filename, table, column):
    with open(filename, "w") as f:
        for row in table:
            print(row[column], file=f)
    print("generated:", filename)

table1 = make_table("table1.txt")
table2 = make_table("table2.txt")
write_text("text-en.txt", table1, 2)
write_text("text-ja.txt", table1, 3)

makef  = "Makefile"
audio1 = "src.wav"
srcdir = "dst1"
imgsrc = "dst2"
mp4out = "dst3"
flistv = "dst3-v.txt"
tempv  = "dst3-v.mp4"
audio2 = "dst3-a1.wav"
flista = "dst3-a2.txt"
tempa  = "dst3-a2.aac"
output = "dst4.mp4"

def parse_time(t, loc="", use_float=False):
    if use_float:
        if r := re.match(r"(\d+):(\d+):(\d+\.\d+)", t):
            return int(r[1]) * 3600 + int(r[2]) * 60 + float(r[3])
        if r := re.match(r"(\d+):(\d+\.\d+)", t):
            return int(r[1]) * 60 + float(r[2])
    if r := re.match(r"(\d+):(\d+):(\d+)", t):
        return int(r[1]) * 3600 + int(r[2]) * 60 + int(r[3])
    if r := re.match(r"(\d+):(\d+)", t):
        return int(r[1]) * 60 + int(r[2])
    print(f"Error{loc}: {t}")
    return None

imgs = {}
i = 0

# Determine if the first entry is a title based on the speaker column
if not table1[0][1]:
    imgs[0] = f"{srcdir}/001.png"
    i = 1

for j, (_, t2, _, _) in enumerate(table2):
    if (t2s := parse_time(t2, " in table2")) is None:
        continue
    found = False
    while not found and i < len(table1) - 1:
        t1 = table1[i][0]
        if (t1s := parse_time(t1, " in table1")) is not None:
            if t1s == t2s:
                # print(f"{j} => {i}: {t1}")
                imgs[i] = f"{srcdir}/{j+2:03d}.png"
                found = True
            elif t1s > t2s:
                break
        i += 1
    if not found:
        print("Not found:", t2)
        break

with open("table.js", "w") as f1:
    print("const table = [", file=f1)
    img = f"{srcdir}/001.png"
    for i, (_, _, en, ja, det) in enumerate(table1):
        if i in imgs:
            img = imgs[i]
        det = det.replace("。", "。 ")
        print("    [" + ", ".join(repr(s) for s in (img, en, ja, det)) + "],", file=f1)
    print("];", file=f1)
print("generated: table.js")

times = []
for t1, *_ in table1:
    if (t1s := parse_time(t1, " in table1", True)) is not None:
        times.append(t1s)
times[0] -= 5
times[1] -= 1

durs = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]
durs.append(2)
for i, dur in enumerate(durs):
    if dur == 0:
        durs[i - 1] -= 0.5
        durs[i    ] += 1
        durs[i + 1] -= 0.5

with open(makef, "w") as f1:
    print(f"all: {output}", file=f1)
    print(file=f1)
    dst_v = []
    for i, dur in enumerate(durs):
        fn = f"{i+1:03d}"
        src = f"{imgsrc}/{fn}.png"
        dst = f"{mp4out}/{fn}.mp4"
        print(f"{dst}: {src}", file=f1)
        print(f"\tmkdir -p {mp4out} && rm -f $@ && ffmpeg -loop 1 -i $< -c:v libx264 -t {dur} -pix_fmt yuv420p $@", file=f1)
        dst_v.append(dst)
    print(file=f1)
    print("DST_V =", *dst_v, file=f1)
    dst_a = [f"{mp4out}/_5.wav", audio2, f"{mp4out}/_2.wav"]
    print("DST_A =", *dst_a, file=f1)
    print(f"""
{flistv}:
\tfor dst in $(DST_V); do echo file \\'$$dst\\'; done > $@

{tempv}: {flistv} $(DST_V)
\trm -f $@ && ffmpeg -f concat -i $< -c copy $@

{audio2}: {audio1}
\tffmpeg -i $< -ar 44100 -ac 1 -c:a pcm_s16le $@

{flista}:
\tfor dst in $(DST_A); do echo file \\'$$dst\\'; done > $@

{mp4out}/_5.wav:
\tffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 5 -q:a 9 -acodec pcm_s16le $@

{mp4out}/_2.wav:
\tffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 2 -q:a 9 -acodec pcm_s16le $@

{tempa}: {flista} $(DST_A)
\trm -f $@ && ffmpeg -f concat -i $< -c:a aac $@

{output}: {tempv} {tempa}
\trm -f $@ && ffmpeg -i {tempv} -i {tempa} -c:v copy -c:a copy -shortest $@

clean:
\trm -rf {mp4out} {flistv} {tempv} {audio2} {flista} {tempa} {output}
""".rstrip(), file=f1)
print("generated:", makef)
