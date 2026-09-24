#!/usr/bin/env python3
"""Read plan-view dimensions off a 600 dpi flatbed scan.

    tools/measure_scan.py <scan.jpg> <outdir>

Prints every number it finds (mm) and writes annotated crops to <outdir> so
a human can check each fit against the picture. Scale comes from the steel
rule in the frame (mm tick spacing), cross-checked against the file's dpi.
A face-down board is MIRRORED in the scan; the caller decides which side was
down and flips x when quoting positions "looking at the screen".

Stdlib + numpy + scipy.ndimage + Pillow. No third-party geometry.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

# Crops in scan-01 pixel coordinates (x0, y0, x1, y1); found from the 150 dpi
# preview. Re-derive for any other scan.
CROPS = {
    "rule": (100, 0, 900, 4694),
    "lcd_top": (1750, 450, 2600, 1850),
    "pico_top": (1000, 450, 1700, 1850),
    "crypto": (950, 3750, 2550, 4500),
}


# ---------------------------------------------------------------- scale

def scale_from_rule(img, crop, band=(150, 230)):
    """px per mm from the rule's mm ticks: thin BRIGHT etched lines on dark
    steel, one per mm, in the column band `band` (scan x, full res). Their
    positions along y are fit to integer mm indices; the slope is the scale."""
    g = np.asarray(img.crop((band[0], crop[1], band[1], crop[3])).convert("L"), dtype=float)
    nominal = img.info.get("dpi", (600, 600))[1] / 25.4
    prof = g.mean(axis=1)
    prof = prof - ndi.uniform_filter1d(prof, int(nominal * 4))
    sm = ndi.gaussian_filter1d(prof, 1.0)
    thr = sm.mean() + 1.2 * sm.std()
    peaks = [i for i in range(2, len(sm) - 2)
             if sm[i] >= sm[i - 1] and sm[i] > sm[i + 1] and sm[i - 2] < sm[i] and sm[i] > thr]
    keep = [peaks[0]]
    for m in peaks[1:]:
        if m - keep[-1] > nominal * 0.5:
            keep.append(m)
        elif sm[m] > sm[keep[-1]]:
            keep[-1] = m
    pk = np.array(keep, dtype=float)
    # sub-pixel: parabolic refinement on the smoothed profile
    for j, i in enumerate(pk.astype(int)):
        y0, y1, y2 = sm[i - 1], sm[i], sm[i + 1]
        d = (y0 - y2) / (2 * (y0 - 2 * y1 + y2)) if (y0 - 2 * y1 + y2) != 0 else 0
        pk[j] = i + d
    idx = np.concatenate([[0], np.cumsum(np.round(np.diff(pk) / nominal))])
    slope, off = np.polyfit(idx, pk, 1)
    resid = pk - (slope * idx + off)
    good = np.abs(resid) < 3
    slope, off = np.polyfit(idx[good], pk[good], 1)
    resid = pk[good] - (slope * idx[good] + off)
    return {"px_per_mm": float(slope), "nominal_px_per_mm": float(nominal),
            "ticks_used": int(good.sum()), "ticks_rejected": int((~good).sum()),
            "span_mm": float(idx[good].max() - idx[good].min()),
            "tick_fit_rms_px": float(np.sqrt(np.mean(resid ** 2)))}


# ---------------------------------------------------------------- geometry

def largest(mask, min_area=0):
    lab, n = ndi.label(mask)
    if n == 0:
        return np.zeros_like(mask)
    sizes = ndi.sum(mask, lab, range(1, n + 1))
    i = int(np.argmax(sizes)) + 1
    return lab == i if sizes[i - 1] >= min_area else np.zeros_like(mask)


def components(mask, min_area, max_area):
    lab, n = ndi.label(mask)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        a = int(m.sum())
        if min_area <= a <= max_area:
            cy, cx = ndi.center_of_mass(m)
            ys, xs = np.nonzero(m)
            out.append({"cx": float(cx), "cy": float(cy), "area": a,
                        "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1)})
    return out


def hull(points):
    """Convex hull, Andrew's monotone chain. points: (N,2) array."""
    pts = sorted(map(tuple, points))
    if len(pts) <= 2:
        return np.array(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def min_rect(mask):
    """Minimum-area bounding rectangle of a mask's boundary. Returns centre,
    size (long, short), angle of the long axis in degrees, and the 4 corners."""
    edge = mask & ~ndi.binary_erosion(mask)
    ys, xs = np.nonzero(edge)
    pts = np.column_stack([xs, ys]).astype(float)
    h = hull(pts)
    best = None
    for i in range(len(h)):
        dx, dy = h[(i + 1) % len(h)] - h[i]
        ang = np.arctan2(dy, dx)
        c, s = np.cos(-ang), np.sin(-ang)
        r = pts @ np.array([[c, -s], [s, c]]).T
        w, hgt = np.ptp(r[:, 0]), np.ptp(r[:, 1])
        if best is None or w * hgt < best[0]:
            best = (w * hgt, ang, r[:, 0].min(), r[:, 0].max(), r[:, 1].min(), r[:, 1].max())
    _, ang, x0, x1, y0, y1 = best
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s], [s, c]])
    corners = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) @ R.T
    centre = corners.mean(axis=0)
    w, hgt = x1 - x0, y1 - y0
    if hgt > w:
        w, hgt, ang = hgt, w, ang + np.pi / 2
    ang = (np.degrees(ang) + 90) % 180 - 90
    return {"cx": float(centre[0]), "cy": float(centre[1]), "long": float(w), "short": float(hgt),
            "angle_deg": float(ang), "corners": corners.tolist()}


def to_board_frame(px, py, rect):
    """Pixel -> (u, v) in the board's own frame: origin at the rect centre,
    u along the long axis, v along the short axis. Units: px."""
    a = np.radians(rect["angle_deg"])
    dx, dy = px - rect["cx"], py - rect["cy"]
    return dx * np.cos(a) + dy * np.sin(a), -dx * np.sin(a) + dy * np.cos(a)


# ---------------------------------------------------------------- boards

def channels(img, crop):
    rgb = np.asarray(img.crop(crop).convert("RGB"), dtype=int)
    V = rgb.max(axis=-1)
    sat = V - rgb.min(axis=-1)
    return rgb, V, sat


def local_background(V, sat, step=8, size=25):
    """The platen backing is a neutral grey that drifts from V~90 to V~130
    across one scan, with a soft darker halo hugging every part. Estimate it
    per pixel: 80th percentile of the low-saturation pixels over a ~200 px
    window, computed on a downsampled grid."""
    small = V[::step, ::step].astype(float)
    ok = (sat[::step, ::step] < 12) & (small > 70)   # neutral and not a dark part
    small[~ok] = np.nan
    filled = np.where(np.isnan(small), np.nanmedian(small), small)
    bg = ndi.percentile_filter(filled, 80, size=size)
    bg = ndi.gaussian_filter(bg, 2)
    return np.kron(bg, np.ones((step, step)))[:V.shape[0], :V.shape[1]]


def not_background(V, sat):
    """Anything coloured, or clearly darker or brighter than the backing
    right there, is a part. The halo (a few units darker) is not."""
    bg = local_background(V, sat)
    return (sat > 20) | (V < bg - 30) | (V > bg + 30)


def board_mask(V, sat, close=8, open_=6, exclude=None):
    m = ndi.binary_closing(not_background(V, sat), iterations=close)
    m = ndi.binary_fill_holes(m)
    if exclude is not None:
        m &= ~exclude
    m = ndi.binary_opening(m, iterations=open_)
    return ndi.binary_fill_holes(largest(m))


def round_blobs(mask, ppm, d_lo, d_hi, tol=0.3):
    a_lo, a_hi = (np.pi / 4) * (d_lo * ppm) ** 2, (np.pi / 4) * (d_hi * ppm) ** 2
    return [b for b in components(mask, a_lo, a_hi) if abs(b["w"] - b["h"]) < tol * max(b["w"], b["h"])]


def corner_picks(blobs, rect):
    """One blob per quadrant of the board frame, the outermost."""
    picks = {}
    for b in blobs:
        u, v = to_board_frame(b["cx"], b["cy"], rect)
        q = (u > 0, v > 0)
        if q not in picks or abs(u) + abs(v) > picks[q][0]:
            picks[q] = (abs(u) + abs(v), b)
    return [p[1] for p in picks.values()]


def uv_mm(b, rect, ppm):
    return [c / ppm for c in to_board_frame(b["cx"], b["cy"], rect)]


def diam_mm(b, ppm):
    return 2 * np.sqrt(b["area"] / np.pi) / ppm


def measure_lcd_top(img, crop, ppm, outdir):
    """Waveshare Pico-LCD-1.3, screen side down. Board outline, glass, four
    tact-switch plungers, joystick stem. Board frame: u along the long axis,
    v across; the joystick end is made +u."""
    rgb, V, sat = channels(img, crop)
    R, B = rgb[..., 0], rgb[..., 2]
    # the PCB substrate is a dark teal; the FPC tape is a brighter blue (V>110)
    # and the shadow halo is neutral, so neither gets in. The glass, switches
    # and joystick are holes in this mask that a closing + fill covers.
    pcb = (B > R + 25) & (sat > 20) & (V < 105)
    tape = ndi.binary_dilation(largest(ndi.binary_opening((B > 100) & (R < 30), iterations=3)), iterations=int(0.8 * ppm))
    pcb &= ~tape                               # the tape's blurred edge passes the colour test; cut it and a margin
    very_dark = (V < 40) & (sat < 20)          # the glass; it spans the full width and joins the two PCB ends
    board = ndi.binary_fill_holes(largest(ndi.binary_closing(pcb | very_dark, iterations=12)))
    board = ndi.binary_opening(board, iterations=3)
    rect = min_rect(board)
    inner = ndi.binary_erosion(board, iterations=8)

    glass = largest((V < 32) & (sat < 16) & inner, min_area=int((15 * ppm) ** 2))
    grect = min_rect(glass)

    # joystick: silver square (flat grey, V 80-120) is the biggest low-sat mid-grey blob
    silver = largest(ndi.binary_opening((V > 78) & (V < 125) & (sat < 14) & inner & ~glass, iterations=3),
                     min_area=int((5 * ppm) ** 2))
    # orient the frame first: the glass sits toward the -u end, the joystick beyond it at +u
    if to_board_frame(grect["cx"], grect["cy"], rect)[0] > 0:
        rect["angle_deg"] += 180
    gmax = max(to_board_frame(x, y, rect)[0] for x, y in grect["corners"])
    stem = None
    stems = round_blobs(ndi.binary_opening((V < 45) & inner & ~ndi.binary_dilation(glass, iterations=12), iterations=2),
                        ppm, 1.5, 6.0, tol=0.35)
    stems = [b for b in stems if to_board_frame(b["cx"], b["cy"], rect)[0] > gmax + 2 * ppm]
    if stems:
        stem = max(stems, key=lambda b: b["area"])

    # plungers: light beige discs (V>130, low sat), 2-5 mm, at the -u end
    plung = round_blobs(ndi.binary_opening((V > 130) & (sat < 50) & inner & ~glass, iterations=2), ppm, 1.8, 5.5, tol=0.35)
    plung = [b for b in plung if to_board_frame(b["cx"], b["cy"], rect)[0] < 0]
    plung = sorted(sorted(plung, key=lambda b: -b["area"])[:4], key=lambda b: to_board_frame(b["cx"], b["cy"], rect)[1])

    res = {"board_long_mm": rect["long"] / ppm, "board_short_mm": rect["short"] / ppm,
           "board_angle_deg": rect["angle_deg"],
           "glass_long_mm": grect["long"] / ppm, "glass_short_mm": grect["short"] / ppm,
           "glass_centre_uv_mm": [c / ppm for c in to_board_frame(grect["cx"], grect["cy"], rect)],
           "glass_angle_rel_deg": (grect["angle_deg"] - rect["angle_deg"] + 90) % 180 - 90,
           "plungers_uv_mm": [uv_mm(b, rect, ppm) for b in plung],
           "plunger_diam_mm": [diam_mm(b, ppm) for b in plung],
           "joystick_stem_uv_mm": uv_mm(stem, rect, ppm) if stem else None,
           "joystick_stem_diam_mm": diam_mm(stem, ppm) if stem else None}
    if silver.any():
        srect = min_rect(silver)
        res["joystick_base_mm"] = [srect["long"] / ppm, srect["short"] / ppm]
        res["joystick_base_centre_uv_mm"] = [c / ppm for c in to_board_frame(srect["cx"], srect["cy"], rect)]
    draw_overlay(img.crop(crop), [rect, grect] + ([srect] if silver.any() else []),
                 plung + ([stem] if stem else []), f"{outdir}/lcd_top.png")
    return res


def measure_pico_top(img, crop, ppm, outdir):
    """Pink Pico clone, component side down: outline, four mounting holes,
    USB shell. Board frame: USB end = +u."""
    rgb, V, sat = channels(img, crop)
    R, G = rgb[..., 0], rgb[..., 1]
    pink = (R > G + 35) & (R > 120)
    board = ndi.binary_fill_holes(largest(ndi.binary_closing(pink, iterations=6)))
    rect = min_rect(board)
    inner = ndi.binary_erosion(board, iterations=4)
    # USB shell: the one dark neutral block that crosses a short edge. Work in
    # the board frame: u beyond +-(long/2 - 8 mm), within the board's width.
    yy, xx = np.mgrid[0:V.shape[0], 0:V.shape[1]]
    U, W = to_board_frame(xx, yy, rect)
    # only the part of the shell that overhangs the edge is unambiguous
    end_zone = (np.abs(U) > rect["long"] / 2 + 0.3 * ppm) & (np.abs(U) < rect["long"] / 2 + 5 * ppm) & (np.abs(W) < rect["short"] / 2)
    usb = largest(ndi.binary_opening((V < 95) & (sat < 25) & end_zone, iterations=2), min_area=int((2 * ppm) ** 2))
    urect = min_rect(usb) if usb.any() else None
    if urect and to_board_frame(urect["cx"], urect["cy"], rect)[0] < 0:
        rect["angle_deg"] += 180
    # a hole shows the backing through it (grey, sometimes dark); the edge
    # pads are also grey but touch the outline, so demand the blob sit inside
    # the board eroded by ~0.7 mm
    hole_zone = ndi.binary_erosion(board, iterations=int(0.7 * ppm))
    holes = corner_picks(round_blobs(ndi.binary_opening(~pink & (sat < 30) & hole_zone, iterations=2), ppm, 1.4, 3.2, tol=0.3), rect)
    holes = sorted(holes, key=lambda b: tuple(np.sign(to_board_frame(b["cx"], b["cy"], rect))))
    res = {"board_long_mm": rect["long"] / ppm, "board_short_mm": rect["short"] / ppm,
           "board_angle_deg": rect["angle_deg"],
           "holes_uv_mm": [uv_mm(b, rect, ppm) for b in holes],
           "hole_diam_mm": [diam_mm(b, ppm) for b in holes],
           "usb_overhang_mm": None, "usb_width_mm": None, "usb_centre_v_mm": None}
    if urect:
        us = [to_board_frame(x, y, rect) for x, y in urect["corners"]]
        res["usb_overhang_mm"] = (max(u for u, _ in us) - rect["long"] / 2) / ppm
        res["usb_width_mm"] = (max(v for _, v in us) - min(v for _, v in us)) / ppm
        res["usb_centre_v_mm"] = to_board_frame(urect["cx"], urect["cy"], rect)[1] / ppm
    draw_overlay(img.crop(crop), [rect] + ([urect] if urect else []), holes, f"{outdir}/pico_top.png")
    return res


def measure_crypto(img, crop, ppm, outdir):
    """Two ATECC608 breakouts. Outline and the four mounting holes of each;
    a hole shows the grey backing through it."""
    rgb, V, sat = channels(img, crop)
    nb = ndi.binary_fill_holes(ndi.binary_closing(not_background(V, sat), iterations=8))
    lab, n = ndi.label(ndi.binary_opening(nb, iterations=6))
    sizes = ndi.sum(lab > 0, lab, range(1, n + 1))
    out, rects, allholes = [], [], []
    for i in np.argsort(sizes)[::-1][:2]:
        board = ndi.binary_fill_holes(lab == (i + 1))
        rect = min_rect(board)
        inner = ndi.binary_erosion(board, iterations=int(0.7 * ppm))
        holes = corner_picks(round_blobs(ndi.binary_opening((V > 85) & (V < 145) & (sat < 16) & inner, iterations=2),
                                         ppm, 1.4, 4.0, tol=0.3), rect)
        out.append({"board_long_mm": rect["long"] / ppm, "board_short_mm": rect["short"] / ppm,
                    "holes_uv_mm": [uv_mm(b, rect, ppm) for b in holes],
                    "hole_diam_mm": [diam_mm(b, ppm) for b in holes]})
        rects.append(rect)
        allholes += holes
    draw_overlay(img.crop(crop), rects, allholes, f"{outdir}/crypto.png")
    return out


def draw_overlay(im, rects, blobs, path):
    im = im.convert("RGB")
    d = ImageDraw.Draw(im)
    for r in rects:
        pts = [tuple(p) for p in r["corners"]]
        d.line(pts + [pts[0]], fill=(255, 0, 0), width=3)
    for b in blobs:
        rad = np.sqrt(b["area"] / np.pi)
        d.ellipse([b["cx"] - rad, b["cy"] - rad, b["cx"] + rad, b["cy"] + rad], outline=(0, 255, 0), width=3)
        d.line([b["cx"] - 15, b["cy"], b["cx"] + 15, b["cy"]], fill=(0, 255, 0), width=1)
        d.line([b["cx"], b["cy"] - 15, b["cx"], b["cy"] + 15], fill=(0, 255, 0), width=1)
    im.save(path)


def main():
    img = Image.open(sys.argv[1])
    outdir = sys.argv[2]
    sc = scale_from_rule(img, CROPS["rule"])
    ppm = sc["px_per_mm"]
    res = {"scale": sc,
           "lcd_top": measure_lcd_top(img, CROPS["lcd_top"], ppm, outdir),
           "pico_top": measure_pico_top(img, CROPS["pico_top"], ppm, outdir),
           "crypto": measure_crypto(img, CROPS["crypto"], ppm, outdir)}
    print(json.dumps(res, indent=1, default=lambda o: round(float(o), 3)))
    json.dump(res, open(f"{outdir}/measure.json", "w"), indent=1, default=lambda o: round(float(o), 3))


if __name__ == "__main__":
    main()
