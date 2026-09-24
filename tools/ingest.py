#!/usr/bin/env python3
"""Copy an image into measurements/ with its metadata stripped.

    tools/ingest.py <src> <measurements/YYYY-MM-DD-kind-nn-what.jpg> [dpi]

Re-encodes through Pillow so EXIF, GPS, maker notes and device serials never
reach the public repo. The dpi tag is re-added when given (scans), because
the log records it; scale is still calibrated against the rule in frame.
"""
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else None
im = Image.open(src)
clean = Image.frombytes(im.mode, im.size, im.tobytes())
kw = {"quality": 92} if dst.lower().endswith((".jpg", ".jpeg")) else {}
if dpi:
    kw["dpi"] = (dpi, dpi)
clean.save(dst, **kw)
print("%s -> %s %sx%s, metadata stripped" % (src, dst, *im.size))
