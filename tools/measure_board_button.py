"""Reproduce V2 bottom-access estimate from our own pink-board scan.

Run .venv/bin/python tools/measure_board_button.py. No external geometry.
Selection window isolates the visible pale plunger, not neighbouring pads.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
import measure_scan as s

root = Path(__file__).resolve().parents[1]
im = Image.open(root / 'measurements/2026-09-24-scan-01-all-boards-600dpi.jpg')
ppm = 23.665753243961248  # existing scan01 ruler fit
crop = s.CROPS['pico_top']
rgb, value, saturation = s.channels(im, crop)
pink = (rgb[..., 0] > rgb[..., 1] + 35) & (rgb[..., 0] > 120)
board = s.ndi.binary_fill_holes(s.largest(s.ndi.binary_closing(pink, iterations=6)))
rect = s.min_rect(board)
mask = (value > 130) & (saturation < 55) & s.ndi.binary_erosion(board, iterations=20)
blobs = s.round_blobs(s.ndi.binary_opening(mask, iterations=2), ppm, 1.4, 4, tol=.45)
button = [b for b in blobs if 270 < b['cx'] < 320 and 380 < b['cy'] < 440]
assert len(button) == 1, 'Ambiguous plunger detection; inspect scan'
b = button[0]
u, v = s.uv_mm(b, rect, ppm)
result = dict(source='scan01 pink component face', px_per_mm=ppm,
              crop=list(crop), centroid_crop_px=[b['cx'], b['cy']],
              component_face_uv_mm=[u, v], installed_xy_offset_mm=[-v, u],
              reflection='Opposite face from LCD front; USB end remains +y',
              limitations='Blurred scan and assumed board centring; fit-test estimate, not caliper measurement')
(root / 'measurements/2026-09-24-pink-button-estimate.json').write_text(json.dumps(result, indent=2) + '\n')
s.draw_overlay(im.crop(crop), [rect], button, str(root / 'measurements/2026-09-24-pink-button-fit.png'))
print(json.dumps(result, indent=2))
