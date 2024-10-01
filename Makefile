SCRDIR = ..
PYTHON = python

all:

mp3:
	ffmpeg -i src.wav -vn -ac 1 -ar 44100 -ab 128k -acodec libmp3lame -f mp3 src.mp3

convert1: log1.json log2.json
	$(PYTHON) $(SCRDIR)/json2md $^

convert2: log1.py log2.py
	for py in $^; do python $$py > $${py%.*}.md; done

extract:
	$(PYTHON) $(SCRDIR)/extract-table.py log1.md "| timecode | speaker | caption |" > table0.txt
	$(PYTHON) $(SCRDIR)/extract-table.py log1.md "| 時間 | 話者 | 英語 | 日本語訳 | 注釈 |" > table1.txt
	$(PYTHON) $(SCRDIR)/extract-table.py log2.md "| No | Time | Theme | Illustration Description |" > table2.txt

check:
	$(PYTHON) $(SCRDIR)/check-table.py table0.txt table1.txt
	diff -u table0_.txt table1_.txt

rename:
	$(PYTHON) $(SCRDIR)/rename.py src

resize:
	$(PYTHON) $(SCRDIR)/resize.py -o dst1 src

generate:
	$(PYTHON) $(SCRDIR)/generate.py

capture:
	$(PYTHON) $(SCRDIR)/capture.py

cut:
	ffmpeg -i dst4.mp4 -ss 00:00:02 -to 00:02:02 dst4-cut.mp4

.PHONY: all mp3 convert1 convert2 extract check rename resize generate capture cut
