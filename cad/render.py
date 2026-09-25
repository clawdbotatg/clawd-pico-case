"""Render a static engineering preview directly from our CAD tessellation.

No reference images, imported geometry, or generative imagery. Painter-order
orthographic preview with a depth buffer; use STEP and solid checks for measurements.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import model

ROOT = Path(__file__).resolve().parents[1]


def render():
    mesh = {}
    for name, (fn, color) in model.PARTS.items():
        if name == 'fpc_tape':
            continue  # unresolved removable-flag hypothesis; disclosed in caption
        verts, triangles = fn().tessellate(0.12)
        mesh[name] = (np.array([tuple(v) for v in verts]), triangles,
                      np.array([int(color[i:i+2], 16) for i in (1, 3, 5)]))
    panels = [
        ('R4 / assembled', dict.fromkeys(mesh, 0), (1, -1.6, 1.7)),
        ('Assembly / exploded', {'base': -12, 'pico': -3, 'hat': 9,
                                 'lid': 23, 'button_caps': 32, 'joystick_cap': 32}, (1, -1.6, 1.2)),
        ('Lid / inside and USB fin', {'lid': 0}, (-1, -1.6, -1.7)),
        ('Base / sloped supports', {'base': 0}, (1, -1.6, 1.7)),
    ]
    canvas = Image.new('RGB', (1600, 1600), '#eeece5')
    font = ImageFont.load_default(size=26)
    small = ImageFont.load_default(size=19)
    light = np.array((-.3, -.5, 1.0)); light /= np.linalg.norm(light)
    for panel, (title, offsets, direction) in enumerate(panels):
        ox, oy = (panel % 2) * 800, (panel // 2) * 760
        view = np.array(direction, dtype=float); view /= np.linalg.norm(view)
        right = np.cross(view, (0, 0, 1)); right /= np.linalg.norm(right)
        up = np.cross(right, view)
        tris = []
        for name, dz in offsets.items():
            verts, indices, rgb = mesh[name]
            verts = verts + (0, 0, dz)
            for ids in indices:
                pts = verts[list(ids)]
                normal = np.cross(pts[1] - pts[0], pts[2] - pts[0])
                norm = np.linalg.norm(normal)
                if norm < 1e-10 or normal @ view <= 0:
                    continue
                normal /= norm
                shade = .68 + .30 * abs(normal @ light)
                face_rgb = rgb
                if name == 'hat' and np.allclose(pts[:, 2], model.P.S3 + dz):
                    face_rgb = np.array((24, 29, 33))
                color = tuple(np.clip(face_rgb * shade, 0, 255).astype(int))
                projected = np.column_stack((pts @ right, -pts @ up))
                tris.append((pts @ view, projected, color))
        bounds = np.concatenate([t[1] for t in tris])
        lo, hi = bounds.min(axis=0), bounds.max(axis=0)
        scale = min(680 / (hi - lo)[0], 640 / (hi - lo)[1])
        centre = (lo + hi) / 2
        pixels = np.full((760, 800, 3), (238, 236, 229), dtype=np.uint8)
        depth = np.full((760, 800), -np.inf)
        for heights, pts, color in tris:
            pix = (pts - centre) * scale + (400, 395)
            x0, y0 = np.maximum(np.floor(pix.min(axis=0)).astype(int), (0, 0))
            x1, y1 = np.minimum(np.ceil(pix.max(axis=0)).astype(int), (799, 759))
            if x1 < x0 or y1 < y0:
                continue
            yy, xx = np.mgrid[y0:y1+1, x0:x1+1]
            xx = xx + .5; yy = yy + .5
            a, b, c = pix
            den = (b[1]-c[1])*(a[0]-c[0]) + (c[0]-b[0])*(a[1]-c[1])
            if abs(den) < 1e-10:
                continue
            wa = ((b[1]-c[1])*(xx-c[0]) + (c[0]-b[0])*(yy-c[1])) / den
            wb = ((c[1]-a[1])*(xx-c[0]) + (a[0]-c[0])*(yy-c[1])) / den
            wc = 1 - wa - wb
            z = wa * heights[0] + wb * heights[1] + wc * heights[2]
            old = depth[y0:y1+1, x0:x1+1]
            mask = (wa >= -1e-8) & (wb >= -1e-8) & (wc >= -1e-8) & (z > old)
            old[mask] = z[mask]
            pixels[y0:y1+1, x0:x1+1][mask] = color
        canvas.paste(Image.fromarray(pixels), (ox, oy))
        draw = ImageDraw.Draw(canvas)
        draw.text((ox + 35, oy + 20), title, font=font, fill='#252b31')
    draw.text((35, 1530), 'Original measured-board prototype / MIT / unverified physical fit', font=font, fill='#252b31')
    draw.text((35, 1570), 'Illustrative hardware; blue flag omitted pending identification. No other case geometry used.', font=small, fill='#4d535a')
    canvas.save(ROOT / 'renders' / 'r4-preview.png')


if __name__ == '__main__':
    render()
