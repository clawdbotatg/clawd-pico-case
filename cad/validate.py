"""Executable geometric audit; scenarios are not proof of physical fit.

Run .venv/bin/python cad/validate.py from the repository root.
Writes renders/validation.json, with source hashes for reproducibility.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from build123d import Pos, Rot
import model as M
import params as P

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-5  # numerical intersection-volume tolerance, mm^3


def source_hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / 'cad').glob('*.py'))}


def run():
    parts = {n: f() for n, (f, _) in M.PARTS.items()}
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))
        print(('PASS ' if passed else 'FAIL ') + name + (f': {value}' if value is not None else ''), flush=True)

    def clear(name, a, b):
        intersection = a & b
        vol = abs(intersection.volume) if intersection is not None else 0.0
        check(name, vol < TOL, round(vol, 8))

    for name in ('base', 'lid', 'button_caps', 'joystick_cap'):
        p = parts[name]
        check(name + ' valid solid count', p.is_valid and len(p.solids()) == (4 if name == 'button_caps' else 1), len(p.solids()))
        oriented = Rot(180, 0, 0) * p if name in ('lid', 'joystick_cap') else p
        zmin = oriented.bounding_box().min.Z
        # Every independent solid must have a real planar bed contact.
        for i, solid in enumerate(oriented.solids()):
            bed = sum(f.area for f in solid.faces()
                      if abs(f.bounding_box().min.Z - zmin) < TOL
                      and abs(f.bounding_box().max.Z - zmin) < TOL)
            check(f'{name}[{i}] bed contact', bed > 1, round(bed, 3))

    # Flag is intentionally unresolved and reported separately, not hidden as a pass.
    for a, b in itertools.combinations([n for n in parts if n != 'fpc_tape'], 2):
        clear(f'assembled {a}/{b}', parts[a], parts[b])

    sharp = M.box(0, P.L2, 0, P.L1, -P.L3, 0)
    clear('sharp PCB/base', sharp, parts['base'])
    clear('sharp PCB/lid', sharp, parts['lid'])
    for dx, dy in itertools.product((-0.1, 0, 0.1), repeat=2):  # V4
        clear(f'PCB XY sensitivity {dx},{dy}', Pos(dx, dy, 0) * sharp, parts['base'])

    # Remove only moving plungers from the hardware proxy for button press tests.
    fixed_hat = parts['hat']
    for x, y in M.BUTTONS:
        fixed_hat -= M.box(x - P.B4X / 2, x + P.B4X / 2,
                           y - P.B4Y / 2, y + P.B4Y / 2, P.B3, P.B5 + P.EPS)
    for dz in np.linspace(0, P.B6, 9):  # V4: measured travel, no force estimate
        cap = Pos(0, 0, -float(dz)) * parts['button_caps']
        clear(f'button travel {dz:.4f}/lid', cap, parts['lid'])
        clear(f'button travel {dz:.4f}/fixed hardware', cap, fixed_hat)
    caps = sorted(parts['button_caps'].solids(), key=lambda s: s.center().X)
    for i, (a, b) in enumerate(zip(caps, caps[1:])):
        clear(f'neighbour caps at lateral limits {i}', Pos(P.CAP_HOLE_CLEAR, 0, 0) * a,
              Pos(-P.CAP_HOLE_CLEAR, 0, 0) * b)
    for i, cap in enumerate(caps):
        check(f'button {i} retained upward', (Pos(0, 0, P.CAP_POCKET_CLEAR + 0.1) * cap & parts['lid']).volume > TOL)

    # Entire rectangular swept volume establishes continuous vertical insertion.
    # Conservative envelope for Pico PCB+USB; hat's downward-facing sockets are
    # inside that plan rectangle. Unmodelled solder/components still need inspection.
    pcb_sweep = M.box(M.PICO_CX - P.P2 / 2, M.PICO_CX + P.P2 / 2,
                     M.PICO_Y0, M.PICO_Y1, M.Z_PICO_BOT, P.L1)
    usb_sweep = M.box(M.PICO_CX - P.P12 / 2, M.PICO_CX + P.P12 / 2,
                     min(M.USB_EDGE_Y, M.USB_EDGE_Y + M.USB_SIGN * P.P11),
                     max(M.USB_EDGE_Y, M.USB_EDGE_Y + M.USB_SIGN * P.P11), M.Z_USB_BOT, P.L1)
    clear('continuous Pico insertion', pcb_sweep, parts['base'])
    clear('continuous USB insertion', usb_sweep, parts['base'])
    clear('continuous hat insertion', M.box(0, P.L2, 0, P.L1, -P.L3, P.L1), parts['base'])
    # Fin translates down with lid; check sampled path against seated hardware.
    for dz in (0, 1, 3, 6, 12, 20):
        clear(f'lid approach {dz}/hardware', Pos(0, 0, dz) * parts['lid'], parts['hat'] + parts['pico'])
    for stand in (P.P15, P.A1_USB - P.A1_PCB):
        shell = M.box(M.PICO_CX - P.P12 / 2, M.PICO_CX + P.P12 / 2,
                      M.IY1, M.Y1, M.Z_PICO_BOT - stand, M.Z_PICO_BOT - stand + P.P13)
        clear(f'USB stand-off {stand:.2f}', shell, parts['base'] + parts['lid'])
    check('snap positive overlap', P.SNAP_H > P.MATE_CLEAR, P.SNAP_H - P.MATE_CLEAR)
    check('snap catches on lift', (parts['base'] & (Pos(0, 0, P.SNAP_WIN_CLEAR + 0.1) * parts['lid'])).volume > TOL)

    # Sensitivity only: actual joystick pivot, angular travel and click unknown.
    jx, jy = M.JOY_C
    fixed_joy_hat = parts['hat'] - M.box(jx - P.J4 / 2, jx + P.J4 / 2,
                                        jy - P.J4 / 2, jy + P.J4 / 2, P.J3, P.J6 + P.EPS)
    for pivot in (0, 3):  # V4
        for angle in (0, 5, 10):
            for direction in range(0, 360, 45):
                cap = (Pos(jx, jy, pivot - 0.3) * Rot(0, 0, direction)
                       * Rot(angle, 0, 0) * Rot(0, 0, -direction)
                       * Pos(-jx, -jy, -pivot) * parts['joystick_cap'])
                clear(f'joystick scenario pivot={pivot}, tilt={angle}, az={direction}, press=.3', cap, parts['lid'])
                clear(f'joystick fixed hardware pivot={pivot}, tilt={angle}, az={direction}', cap, fixed_joy_hat)

    unresolved = {
        'blue_flag_lid_intersection_mm3': round((parts['fpc_tape'] & parts['lid']).volume, 6),
        'not_verified': ['actual joystick travel/pivot/body/lip/press fit',
                         'snap force, fatigue, layer adhesion and release',
                         'PCB corner landing areas and underside solder clearance',
                         'A1 datum, USB position and actual cable overmould',
                         'slicer bridges, dimensional accuracy and physical fit'],
    }
    result = dict(source_sha256=source_hashes(), checks=checks, unresolved=unresolved,
                  passed=all(c['passed'] for c in checks))
    (ROOT / 'renders' / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    raise SystemExit(0 if run()['passed'] else 1)
