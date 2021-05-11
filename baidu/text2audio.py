#!/usr/bin/env python3
# -*- coding : utf-8 -*-
import os
import sys
import time
from urllib.parse import quote, unquote
import requests

for filename in os.listdir():
    if ".tmp" == filename[-4::]:
        os.remove(filename)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    txt = f.readlines()
if len(sys.argv) > 2:
    ffmpegout = sys.argv[2]
else:
    ffmpegout = "out.mp3"

filelist = []
prefix = int(time.time())
ffmpegin = "{}.tmp".format(prefix)
ff = open(ffmpegin, "w", encoding="utf-8")
print(ffmpegin, "ffmpeg.txt")
for i, text in enumerate(txt):
    out = "{}.{:-04}.tmp".format(prefix, i)
    url = " https://tts.baidu.com/text2audio"
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"
    }
    params = {
        "cuid": "baike",
        "lan": "ZH",
        "ctp": 1,
        "pdt": 301,
        "vol": 9,
        "rate": 32,
        "per": 8,
        "qq-pf-to": "pcqq.group",
        "tex": quote(text, ""),
    }
    r = requests.get(url, headers=headers, timeout=5, params=params)
    print(out, r.status_code, end=" ")
    if r.status_code == 200:
        with open(out, "wb") as f:
            f.write(r.content)
        filelist.append(out)
        ff.write("file {}\n".format(out))
        print("OK")
    else:
        print()
ff.close()

os.system("ffmpeg -f concat -i {} -c copy {}".format(ffmpegin, ffmpegout))

for filename in filelist:
    os.remove(filename)
os.remove(ffmpegin)
