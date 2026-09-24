#!/usr/bin/env python3
"""Flatbed scan over eSCL (driverless), straight to a JPEG.

    tools/scan.py <dpi> <out.jpg> [x_mm y_mm w_mm h_mm]

Region is in mm from the platen's top-left; default is the whole platen.
The scanner is found by mDNS (_uscan._tcp) unless SCANNER_HOST is set. No
network identifiers live in this file on purpose: the repo is public.
600 dpi is this scanner's optical maximum.
"""
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

NS = ('xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03" '
      'xmlns:pwg="http://www.pwg.org/schemas/2010/12/sm"')


def find_scanner():
    host = os.environ.get("SCANNER_HOST")
    if host:
        return host
    out = subprocess.run(["avahi-browse", "-t", "-r", "-p", "_uscan._tcp"],
                         capture_output=True, text=True, timeout=15).stdout
    for line in out.splitlines():
        f = line.split(";")
        if f[0] == "=" and f[2] == "IPv4" and re.match(r"\d+\.\d+\.\d+\.\d+$", f[7]):
            return f[7]
    sys.exit("no eSCL scanner found; set SCANNER_HOST")


def scan(dpi, out, region):
    host = find_scanner()
    base = "http://%s" % host
    x, y, w, h = (int(round(v / 25.4 * 300)) for v in region)  # eSCL: 1/300 in
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<scan:ScanSettings {NS}><pwg:Version>2.9</pwg:Version>
<pwg:ScanRegions><pwg:ScanRegion><pwg:ContentRegionUnits>escl:ThreeHundredthsOfInches</pwg:ContentRegionUnits>
<pwg:XOffset>{x}</pwg:XOffset><pwg:YOffset>{y}</pwg:YOffset><pwg:Width>{w}</pwg:Width><pwg:Height>{h}</pwg:Height>
</pwg:ScanRegion></pwg:ScanRegions><pwg:InputSource>Platen</pwg:InputSource>
<scan:ColorMode>RGB24</scan:ColorMode><scan:XResolution>{dpi}</scan:XResolution><scan:YResolution>{dpi}</scan:YResolution>
<pwg:DocumentFormat>image/jpeg</pwg:DocumentFormat></scan:ScanSettings>"""
    req = urllib.request.Request(base + "/eSCL/ScanJobs", data=body.encode(),
                                 headers={"Content-Type": "text/xml"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        job = r.headers["Location"]
    if job.startswith("/"):
        job = base + job
    job = job.replace("https://", "http://")
    t0 = time.time()
    while True:
        try:
            with urllib.request.urlopen(job + "/NextDocument", timeout=240) as r:
                data = r.read()
                break
        except urllib.error.HTTPError as e:
            if e.code == 503 and time.time() - t0 < 240:
                time.sleep(2)
                continue
            raise
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %.0fs)" % (out, len(data), time.time() - t0))


if __name__ == "__main__":
    if len(sys.argv) not in (3, 7):
        sys.exit(__doc__)
    region = [float(v) for v in sys.argv[3:7]] if len(sys.argv) == 7 else [0, 0, 215.9, 297.0]
    scan(int(sys.argv[1]), sys.argv[2], region)
