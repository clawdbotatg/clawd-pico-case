"""The stack (hat + Pico) and the case around it, in build123d.

Returns plain Parts placed in the frame from params.py. build.py exports
them. Run this file directly for a bounding-box sanity print.
"""
from build123d import (Axis, Box, Cylinder, Location, Part, Pos, Rot,
                       fillet, Plane, Rectangle, extrude, Circle, Polygon)
import params as P


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from corner to corner."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def wedge_x(pts_xz, y0, y1):
    """Prism: a polygon in the XZ plane (list of (x, z)), extruded from y0 to y1."""
    return extrude(Plane.XZ.offset(-y0) * Polygon(*pts_xz, align=None), y1 - y0, dir=(0, 1, 0))


def rbox(x0, x1, y0, y1, z0, z1, r):
    """Box with rounded vertical edges."""
    b = box(x0, x1, y0, y1, z0, z1)
    return fillet(b.edges().filter_by(Axis.Z), r)


# ---------------------------------------------------------------- positions

CX, CY = P.L2 / 2, P.L1 / 2                       # LCD board centre
GLASS_C = (CX + P.S_DV, CY + P.S_DU)
BUTTONS = [(CX + dv, CY + P.B_DU) for dv in P.B_DV]
JOY_C = (CX + P.J_DV, CY + P.J_DU)

Z_LCD_BACK = -P.L3
Z_PICO_TOP = Z_LCD_BACK - P.A2                    # Pico PCB face toward the LCD
Z_PICO_BOT = Z_PICO_TOP - P.P3
Z_USB_BOT = Z_PICO_BOT - P.P15                    # lowest point of the stack

PICO_CX = CX if P.PICO_CENTRED_X else CX
PICO_CY = CY if P.PICO_CENTRED_Y else CY
USB_SIGN = 1 if P.USB_END == "top" else -1
PICO_Y0, PICO_Y1 = PICO_CY - P.P1 / 2, PICO_CY + P.P1 / 2
USB_EDGE_Y = PICO_Y1 if USB_SIGN > 0 else PICO_Y0


# ---------------------------------------------------------------- hardware

def hat():
    pcb = rbox(0, P.L2, 0, P.L1, Z_LCD_BACK, 0, P.L4)
    gx, gy = GLASS_C
    glass = box(gx - P.S2 / 2, gx + P.S2 / 2, gy - P.S1 / 2, gy + P.S1 / 2, 0, P.S3)
    parts = pcb + glass
    for bx, by in BUTTONS:
        parts += box(bx - P.B2 / 2, bx + P.B2 / 2, by - P.B1 / 2, by + P.B1 / 2, 0, P.B3)
        parts += Pos(bx, by, P.B3) * extrude(Plane.XY * Rectangle(P.B4X, P.B4Y), P.B5 - P.B3)
    jx, jy = JOY_C
    parts += Pos(jx, jy, 0) * Rot(0, 0, 45) * extrude(Plane.XY * Rectangle(P.J_BASE_X, P.J_BASE_Y), P.J3)
    parts += box(jx - P.J4 / 2, jx + P.J4 / 2, jy - P.J4 / 2, jy + P.J4 / 2, P.J3, P.J6)
    # two 20-way female sockets on the back, at the header pitch
    for sx in (CX - P.P10 / 2, CX + P.P10 / 2):
        parts += box(sx - 1.27, sx + 1.27, CY - 25.4, CY + 25.4, Z_LCD_BACK - P.L7, Z_LCD_BACK)
    return parts


def pico():
    pcb = rbox(PICO_CX - P.P2 / 2, PICO_CX + P.P2 / 2, PICO_Y0, PICO_Y1, Z_PICO_BOT, Z_PICO_TOP, 1.0)
    # USB-C shell: P12 wide, P13 tall, sits with its top P15 below the component face
    # (P15 is the tallest point, so the shell spans P15-P13 .. P15 below the PCB)
    y_in = USB_EDGE_Y - USB_SIGN * 7.0
    y_out = USB_EDGE_Y + USB_SIGN * P.P11
    shell = box(PICO_CX - P.P12 / 2, PICO_CX + P.P12 / 2, min(y_in, y_out), max(y_in, y_out),
                Z_PICO_BOT - P.P15, Z_PICO_BOT - (P.P15 - P.P13))
    return pcb + shell


def fpc_tape():
    """The blue tape as scanned: a thin flag past the right edge, level with the glass."""
    return box(P.L2 - 1.0, P.L2 + P.F_OUT, P.F_Y0, P.F_Y1, P.S3 - 0.3, P.S3)


# ---------------------------------------------------------------- case

X0, X1 = -P.CLEAR - P.WALL, P.L2 + P.CLEAR + P.WALL       # outer footprint
Y0, Y1 = -P.CLEAR - P.WALL, P.L1 + P.CLEAR + P.WALL
IX0, IX1 = -P.CLEAR, P.L2 + P.CLEAR                        # inner pocket
IY0, IY1 = -P.CLEAR, P.L1 + P.CLEAR
Z_FLOOR_TOP = Z_USB_BOT - P.CLEAR
Z_BOTTOM = Z_FLOOR_TOP - P.FLOOR
Z_SPLIT = 0.0                                              # lid meets base at the LCD front face
Z_LID_TOP = P.S3 + P.GLASS_CLEAR + P.LID_TOP


def base():
    outer = rbox(X0, X1, Y0, Y1, Z_BOTTOM, Z_SPLIT, P.CORNER_R)
    pocket = rbox(IX0, IX1, IY0, IY1, Z_FLOOR_TOP, Z_SPLIT + 1, P.POCKET_R)
    b = outer - pocket
    # tongue: the top TONGUE_H of the wall steps in by SKIRT so the lid skirt sits flush outside
    step = rbox(X0, X1, Y0, Y1, Z_SPLIT - P.TONGUE_H, Z_SPLIT + 1, P.CORNER_R) \
        - rbox(X0 + P.SKIRT, X1 - P.SKIRT, Y0 + P.SKIRT, Y1 - P.SKIRT, Z_SPLIT - P.TONGUE_H - 1, Z_SPLIT + 2,
               max(P.CORNER_R - P.SKIRT, 0.5))
    b -= step
    # snap bumps on the tongue's outer face, two per long side. Wedge: flat catch face
    # at the bottom, ramp on top so the lid skirt rides over it going down.
    zlo, zhi = P.SNAP_Z - P.SNAP_BUMP_T / 2, P.SNAP_Z + P.SNAP_BUMP_T / 2
    xl, xr = X0 + P.SKIRT, X1 - P.SKIRT                    # tongue outer faces
    for yb in (CY - P.L1 / 4, CY + P.L1 / 4):
        y0, y1 = yb - P.SNAP_LEN / 2, yb + P.SNAP_LEN / 2
        b += wedge_x([(xl + 0.2, zlo), (xl - P.SNAP_H, zlo), (xl, zhi), (xl + 0.2, zhi)], y0, y1)
        b += wedge_x([(xr - 0.2, zlo), (xr + P.SNAP_H, zlo), (xr, zhi), (xr - 0.2, zhi)], y0, y1)
    # ledge the LCD PCB rests on: the wall itself (pocket is the PCB outline + CLEAR), so the
    # PCB sits on the socket-clearance shelf. Shelf: fill the pocket back in below the LCD PCB
    # except where the sockets and the Pico live.
    shelf = rbox(IX0, IX1, IY0, IY1, Z_LCD_BACK - 0.01 - P.SHELF_T, Z_LCD_BACK - 0.01, P.POCKET_R)
    inner_keep = box(PICO_CX - P.P2 / 2 - P.CLEAR, PICO_CX + P.P2 / 2 + P.CLEAR,
                     PICO_Y0 - P.CLEAR - P.P11 - 1, PICO_Y1 + P.CLEAR + P.P11 + 1, Z_BOTTOM - 1, Z_SPLIT + 1)
    b += shelf - inner_keep
    # USB-C cutout through the end wall
    zc0 = Z_PICO_BOT - P.P15 - P.USB_CLEAR
    zc1 = Z_PICO_BOT - (P.P15 - P.P13) + P.USB_CLEAR
    ywall0, ywall1 = (IY1 - 1, Y1 + 1) if USB_SIGN > 0 else (Y0 - 1, IY0 + 1)
    cut = box(PICO_CX - P.P12 / 2 - P.USB_CLEAR, PICO_CX + P.P12 / 2 + P.USB_CLEAR, ywall0, ywall1, zc0, zc1)
    cut = fillet(cut.edges().filter_by(Axis.Y), min(1.5, (zc1 - zc0) / 2 - 0.05))
    b -= cut
    return b


def lid():
    outer = rbox(X0, X1, Y0, Y1, Z_SPLIT - P.TONGUE_H, Z_LID_TOP, P.CORNER_R)
    # skirt cavity: over the tongue
    cav = rbox(X0 + P.SKIRT, X1 - P.SKIRT, Y0 + P.SKIRT, Y1 - P.SKIRT, Z_SPLIT - P.TONGUE_H - 1, Z_SPLIT,
               max(P.CORNER_R - P.SKIRT, 0.5))
    # ceiling cavity: over the PCB, up to the glass clearance
    cav2 = rbox(IX0, IX1, IY0, IY1, Z_SPLIT - 1, P.S3 + P.GLASS_CLEAR, 0.5)
    l = outer - cav - cav2
    # snap windows: through the skirt where the bumps are (the old blind notches were cut on
    # the cavity side and removed nothing). A window also lets a fingernail push a bump in to open.
    zlo = P.SNAP_Z - P.SNAP_BUMP_T / 2 - P.SNAP_WIN_CLEAR
    zhi = P.SNAP_Z + P.SNAP_BUMP_T / 2 + P.SNAP_WIN_CLEAR
    for yb in (CY - P.L1 / 4, CY + P.L1 / 4):
        y0, y1 = yb - P.SNAP_LEN / 2 - 0.3, yb + P.SNAP_LEN / 2 + 0.3
        l -= box(X0 - 1, X0 + P.SKIRT + 0.01, y0, y1, zlo, zhi)
        l -= box(X1 - P.SKIRT - 0.01, X1 + 1, y0, y1, zlo, zhi)
    # screen window
    gx, gy = GLASS_C
    w = P.WINDOW_CLEAR
    l -= rbox(gx - P.S2 / 2 - w, gx + P.S2 / 2 + w, gy - P.S1 / 2 - w, gy + P.S1 / 2 + w, -1, Z_LID_TOP + 1, 0.8)
    # button pocket: the caps' flanges live under the plate, above the plungers
    pocket_top = P.B5 + P.CAP_FLANGE_T + P.CAP_POCKET_CLEAR
    bx0 = min(b[0] for b in BUTTONS) - P.CAP_FLANGE_W / 2 - 0.3
    bx1 = max(b[0] for b in BUTTONS) + P.CAP_FLANGE_W / 2 + 0.3
    by0 = BUTTONS[0][1] - P.CAP_FLANGE_W / 2 - 0.3
    by1 = BUTTONS[0][1] + P.CAP_FLANGE_W / 2 + 0.3
    l -= rbox(bx0, bx1, by0, by1, -1, pocket_top, 0.8)
    # button holes: square, a web of lid between each
    hw = P.CAP_W + 2 * P.CAP_HOLE_CLEAR
    for bx, by in BUTTONS:
        l -= rbox(bx - hw / 2, bx + hw / 2, by - hw / 2, by + hw / 2, pocket_top - 1, Z_LID_TOP + 1, P.CAP_R + P.CAP_HOLE_CLEAR)
    # joystick hole
    jx, jy = JOY_C
    l -= Pos(jx, jy, Z_LID_TOP / 2) * Cylinder(P.JOY_HOLE_D / 2, Z_LID_TOP + 2)
    return l


def button_caps():
    """A cap per button: a square post through the lid hole, a flange underneath
    that rests on the plunger and stops the cap coming out the top."""
    caps = None
    for bx, by in BUTTONS:
        c = rbox(bx - P.CAP_FLANGE_W / 2, bx + P.CAP_FLANGE_W / 2, by - P.CAP_FLANGE_W / 2, by + P.CAP_FLANGE_W / 2,
                 P.B5, P.B5 + P.CAP_FLANGE_T, P.CAP_R)
        c += rbox(bx - P.CAP_W / 2, bx + P.CAP_W / 2, by - P.CAP_W / 2, by + P.CAP_W / 2,
                  P.B5 + P.CAP_FLANGE_T - 0.01, Z_LID_TOP + P.CAP_PROUD, P.CAP_R)
        caps = c if caps is None else caps + c
    return caps


def joystick_cap():
    jx, jy = JOY_C
    bot = P.J3 + P.JOY_CAP_LIFT
    top = Z_LID_TOP + P.JOY_CAP_TOP
    cap = Pos(jx, jy, (bot + top) / 2) * Cylinder(P.JOY_HOLE_D / 2 - P.JOY_CAP_SIDE_CLEAR, top - bot)
    cap += Pos(jx, jy, top + P.JOY_CAP_FLANGE_T / 2) * Cylinder(P.JOY_HOLE_D / 2 + P.JOY_CAP_FLANGE_OVER, P.JOY_CAP_FLANGE_T)
    s = (P.J4 + P.JOY_SOCKET_CLEAR) / 2
    socket = box(jx - s, jx + s, jy - s, jy + s, bot - 0.1, P.J6 + P.JOY_SOCKET_TIP_CLEAR)
    return cap - socket


PARTS = {
    "hat": (hat, "#1f5f7a"),
    "pico": (pico, "#d4667a"),
    "fpc_tape": (fpc_tape, "#2255cc"),
    "base": (base, "#c9c4b8"),
    "lid": (lid, "#e8e3d6"),
    "button_caps": (button_caps, "#f0a030"),
    "joystick_cap": (joystick_cap, "#f0a030"),
}

if __name__ == "__main__":
    for name, (fn, _) in PARTS.items():
        bb = fn().bounding_box()
        print(f"{name:13} x {bb.min.X:7.2f}..{bb.max.X:6.2f}  y {bb.min.Y:7.2f}..{bb.max.Y:6.2f}  z {bb.min.Z:7.2f}..{bb.max.Z:6.2f}")
