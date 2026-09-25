"""Executable geometric audit; scenarios are not proof of physical fit.

Run .venv/bin/python cad/validate.py from the repository root.
Writes renders/validation.json, with source hashes for reproducibility.
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from build123d import Pos, Rot, Cylinder
import model as M
import params as P

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-5  # numerical intersection-volume tolerance, mm^3


def source_hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / 'cad').glob('*.py'))}


def run(output_path=None):
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
        oriented = Rot(180, 0, 0) * p if name in ('lid', 'joystick_cap', 'button_caps') else p
        zmin = oriented.bounding_box().min.Z
        # Every independent solid must have a real planar bed contact.
        for i, solid in enumerate(oriented.solids()):
            bed = sum(f.area for f in solid.faces()
                      if abs(f.bounding_box().min.Z - zmin) < TOL
                      and abs(f.bounding_box().max.Z - zmin) < TOL)
            check(f'{name}[{i}] bed contact', bed > 1, round(bed, 3))
            if name == 'lid':
                check('lid broad flat face directly on bed', bed > 300, round(bed, 3))
    check('lid has no raised collar', abs(parts['lid'].bounding_box().max.Z - M.Z_LID_TOP) < .001)
    check('screen recess at most 1mm', M.Z_LID_TOP - P.S3 <= 1 + TOL, M.Z_LID_TOP-P.S3)
    check('lid has no USB fin', abs(parts['lid'].bounding_box().min.Z + P.TONGUE_H) < .001)
    check('earlier socket width restored', abs(P.J4 + P.JOY_SOCKET_CLEAR - 2.01) < TOL)
    check('earlier socket roof restored', abs(P.J6 + P.JOY_SOCKET_TIP_CLEAR - 5.3) < TOL)
    check('earlier socket bottom restored', abs(P.J6 - P.JOY_ENGAGE - 3.4) < TOL)
    # D6-SOCKET: reproduce the earlier 4010773 lower shape below the new lip.
    jx, jy = M.JOY_C
    lower_zone = M.box(jx-5, jx+5, jy-5, jy+5, 3.4, 5.0)
    old_lower = Pos(jx, jy, 4.2) * Cylinder(2.5, 1.6)
    old_lower -= M.box(jx-2.01/2, jx+2.01/2, jy-2.01/2, jy+2.01/2, 3.3, 5.3)
    new_lower = parts['joystick_cap'] & lower_zone
    check('earlier lower joystick shape: no added material', abs((new_lower - old_lower).volume) < TOL)
    check('earlier lower joystick shape: no missing material', abs((old_lower - new_lower).volume) < TOL)

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
                     max(M.USB_EDGE_Y, M.USB_EDGE_Y + M.USB_SIGN * P.P11), M.Z_USB_SHELL_BOT, P.L1)
    clear('continuous Pico insertion', pcb_sweep, parts['base'])
    # Closed V1-style port deliberately prevents vertical USB insertion.
    # Do not present this rejected assembly path as a valid one.
    # V6: reverse USB-first insertion with Pico separate from the hat.
    py = M.USB_EDGE_Y + P.P11
    pz = M.Z_USB_SHELL_BOT + P.P13 / 2
    poses = [(a, 0, 0) for a in (0, -2, -4, -6, -8, -10, -12)]
    poses += [(-12, y, 0) for y in (-.3, -.6, -.9, -1.2, -1.5, -1.8)]
    poses += [(-12, -1.8, z) for z in (1, 3, 6, 12, 20, 30)]
    for angle, dy, dz in poses:
        pose = Pos(0, dy, dz) * Pos(0, py, pz) * Rot(angle, 0, 0) * Pos(0, -py, -pz) * parts['pico']
        clear(f'USB-first separate Pico path {angle},{dy},{dz}', pose, parts['base'])
    clear('continuous hat insertion', M.box(0, P.L2, 0, P.L1, -P.L3, P.L1), parts['base'])
    # Fin translates down with lid; check sampled path against seated hardware.
    for dz in (0, 1, 3, 6, 12, 20):
        clear(f'lid approach {dz}/hardware', Pos(0, 0, dz) * parts['lid'], parts['hat'] + parts['pico'])
    for stand in (P.USB_STAND,):  # D5-USB chooses higher A1 placement; old P15 is unresolved
        shell = M.box(M.PICO_CX - P.P12 / 2, M.PICO_CX + P.P12 / 2,
                      M.IY1, M.Y1, M.Z_PICO_BOT - stand, M.Z_PICO_BOT - stand + P.P13)
        clear(f'USB stand-off {stand:.2f}', shell, parts['base'] + parts['lid'])
    check('snap positive overlap', P.SNAP_H > P.MATE_CLEAR, P.SNAP_H - P.MATE_CLEAR)
    check('rectangular button rejects 90-degree insertion', P.CAP_D > P.CAP_W + 2 * P.CAP_HOLE_CLEAR)
    ax, ay = M.ACCESS_C
    tool = Pos(ax, ay, (M.Z_BOTTOM + M.Z_PICO_BOT - P.BOARD_BUTTON_H) / 2) * Cylinder(
        P.BOARD_BUTTON_D / 2, M.Z_PICO_BOT - P.BOARD_BUTTON_H - M.Z_BOTTOM)
    clear('bottom button tool path/base', tool, parts['base'])
    clear('bottom button tool path/hardware before contact', tool, parts['pico'])
    check('bottom access larger than scanned button proxy', P.ACCESS_D > P.BOARD_BUTTON_D)
    check('snap catches on lift', (parts['base'] & (Pos(0, 0, P.SNAP_WIN_CLEAR + 0.1) * parts['lid'])).volume > TOL)

    # Sensitivity only: actual joystick pivot, angular travel and click unknown.
    jx, jy = M.JOY_C
    check('ball passes opening; rear tab retained', P.JOY_BALL_D < min(P.JOY_OPEN_X, P.JOY_OPEN_Y) and max(y for y,z in P.JOY_ARM_PROFILE)>P.JOY_OPEN_DY+P.JOY_OPEN_Y/2)
    check('joystick upward retention before socket disengagement', (Pos(0, 0, 1.5) * parts['joystick_cap'] & parts['lid']).volume > TOL)
    # Conservative continuous downward sweeps relative to the descending lid.
    sweep_bottom = M.Z_BOTTOM
    flange_top = P.JOY_FLANGE_Z + P.JOY_FLANGE_T
    ball_top = P.JOY_BALL_Z + P.JOY_BALL_D / 2
    sweep = M.box(jx-P.JOY_BALL_D/2, jx+P.JOY_BALL_D/2, jy-P.JOY_BALL_D/2, jy+P.JOY_BALL_D/2, sweep_bottom, ball_top)
    # Exact upper silhouette extruded downward: each edge of the rear arm
    # contributes a quadrilateral to the continuous installation envelope.
    for (ya,za),(yb,zb) in zip(P.JOY_ARM_PROFILE,P.JOY_ARM_PROFILE[1:]):
        if abs(ya-yb)<TOL: continue
        if ya>yb: ya,yb,za,zb=yb,ya,zb,za
        swept_arm=M.wedge_x([(ya,sweep_bottom),(yb,sweep_bottom),(yb,zb),(ya,za)],-P.JOY_ARM_HALF_Y,P.JOY_ARM_HALF_Y)
        sweep += Pos(jx,jy,0)*Rot(0,0,90)*swept_arm
    clear('continuous lid installation over mounted joystick', sweep, parts['lid'])
    for side, x0, x1 in [('left', M.X0 - .2, M.X0 + .7), ('right', M.X1 - .7, M.X1 + .2)]:
        tool = M.box(x0, x1, M.CY - 2, M.CY + 2, -P.TONGUE_H - .3, -P.TONGUE_H + .3)
        clear(f'{side} pry tool access', tool, parts['base'] + parts['lid'])
    check('pry notch leaves 1.2mm wall', P.WALL - P.PRY_DEPTH >= 1.2 - TOL, P.WALL - P.PRY_DEPTH)
    fixed_joy_hat = parts['hat'] - M.box(jx - P.J4 / 2, jx + P.J4 / 2,
                                        jy - P.J4 / 2, jy + P.J4 / 2, P.J3, P.J6 + P.EPS)
    hardware_sensitivity = []
    rear_arm = M.joystick_rear_arm()
    for pivot, press in itertools.product((0, 3), (0, .3)):  # V5 scenarios, not measured
        for angle in (0, 5, 10):
            for direction in range(0, 360, 45):
                transform = (Pos(jx, jy, pivot - press) * Rot(0, 0, direction)
                       * Rot(angle, 0, 0) * Rot(0, 0, -direction)
                       * Pos(-jx, -jy, -pivot))
                cap = transform * parts['joystick_cap']
                clear(f'joystick scenario pivot={pivot}, tilt={angle}, az={direction}, press={press}', cap, parts['lid'])
                clear(f'joystick/base pivot={pivot}, tilt={angle}, az={direction}, press={press}', cap, parts['base'])
                clear(f'joystick/PCB pivot={pivot}, tilt={angle}, az={direction}, press={press}', cap, sharp)
                clear(f'new rear arm/hardware pivot={pivot}, tilt={angle}, az={direction}, press={press}', transform * rear_arm, fixed_joy_hat)
                # Restore user's working earlier interface, not geometry changed to
                # clear an unmeasured guessed body in an assumed pivot scenario.
                intersection = cap & fixed_joy_hat
                volume = abs(intersection.volume) if intersection is not None else 0
                if volume > TOL:
                    hardware_sensitivity.append(dict(pivot=pivot, press=press,
                                                     angle=angle, direction=direction, mm3=round(volume, 6)))

    unresolved = {
        'joystick_guessed_body_scenario_intersections': hardware_sensitivity,
        'closed_port_requires_USB_first_assembly': True,
        'blue_flag_lid_intersection_mm3': round((parts['fpc_tape'] & parts['lid']).volume, 6),
        'not_verified': ['actual joystick travel/pivot/body/lip/press fit',
                         'bottom button identity, scan registration and assumed height',
                         'USB uses higher A1 placement; lower P15 placement no longer fits aperture',
                         'snap force, fatigue, layer adhesion and release',
                         'PCB corner landing areas and underside solder clearance',
                         'A1 datum, USB position and actual cable overmould',
                         'slicer bridges, dimensional accuracy and physical fit'],
    }
    result = dict(source_sha256=source_hashes(), checks=checks, unresolved=unresolved,
                  passed=all(c['passed'] for c in checks))
    target = Path(output_path) if output_path else ROOT / 'renders' / 'validation.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    raise SystemExit(0 if run()['passed'] else 1)
