"""The stack (hat + Pico) and the case around it, in build123d.

Returns plain Parts placed in the frame from params.py. build.py exports
them. Run this file directly for a bounding-box sanity print.
"""
from build123d import (Axis, Box, Cylinder, Sphere, Location, Part, Pos, Rot,
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
BUTTONS = [(CX + dx, CY + dy) for dx, dy in P.B_OFFSETS]
JOY_C = (CX + P.J_DV, CY + P.J_DU)
JOY_BASE_C = (CX + P.J_BASE_DV, CY + P.J_BASE_DU)

Z_LCD_BACK = -P.L3
Z_PICO_TOP = Z_LCD_BACK - P.A2                    # Pico PCB face toward the LCD
Z_PICO_BOT = Z_PICO_TOP - P.P3
Z_USB_BOT = Z_PICO_BOT - P.P15                    # lowest point of the stack

PICO_CX = CX + P.PICO_OFFSET_X
PICO_CY = CY + P.PICO_OFFSET_Y
USB_SIGN = 1 if P.USB_END == "top" else -1
PICO_Y0, PICO_Y1 = PICO_CY - P.P1 / 2, PICO_CY + P.P1 / 2
USB_EDGE_Y = PICO_Y1 if USB_SIGN > 0 else PICO_Y0
ACCESS_C = (PICO_CX + P.ACCESS_DX, PICO_CY + P.ACCESS_DY)
Z_USB_SHELL_BOT = Z_PICO_BOT - P.USB_STAND


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
    parts += Pos(*JOY_BASE_C, 0) * Rot(0, 0, P.J_BASE_ANGLE) * extrude(Plane.XY * Rectangle(P.J_BASE_X, P.J_BASE_Y), P.J3)
    parts += box(jx - P.J4 / 2, jx + P.J4 / 2, jy - P.J4 / 2, jy + P.J4 / 2, P.J3, P.J6)
    # two 20-way female sockets on the back, at the header pitch
    for sx in (CX - P.P10 / 2, CX + P.P10 / 2):
        parts += box(sx - P.HEADER_W / 2, sx + P.HEADER_W / 2,
                     CY - P.HEADER_L / 2, CY + P.HEADER_L / 2, Z_LCD_BACK - P.L7, Z_LCD_BACK)
    return parts


def pico():
    pcb = rbox(PICO_CX - P.P2 / 2, PICO_CX + P.P2 / 2, PICO_Y0, PICO_Y1, Z_PICO_BOT, Z_PICO_TOP, P.PICO_R)
    # D5-USB selects the higher A1 placement, retaining P15 for floor depth.
    y_in = USB_EDGE_Y - USB_SIGN * P.USB_IN
    y_out = USB_EDGE_Y + USB_SIGN * P.P11
    shell = box(PICO_CX - P.P12 / 2, PICO_CX + P.P12 / 2, min(y_in, y_out), max(y_in, y_out),
                Z_USB_SHELL_BOT, Z_USB_SHELL_BOT + P.P13)
    button = Pos(*ACCESS_C, Z_PICO_BOT - P.BOARD_BUTTON_H / 2) * Cylinder(P.BOARD_BUTTON_D / 2, P.BOARD_BUTTON_H)
    return pcb + shell + button


def fpc_tape():
    """The blue tape as scanned: a thin flag past the right edge, level with the glass."""
    return box(P.L2 - P.FLAG_IN, P.L2 + P.F_OUT, P.F_Y0, P.F_Y1, P.S3 - P.FLAG_T, P.S3)


# ---------------------------------------------------------------- case

X0, X1 = -P.CLEAR - P.WALL, P.L2 + P.CLEAR + P.WALL       # outer footprint
Y0, Y1 = -P.CLEAR - P.WALL, P.L1 + P.CLEAR + P.WALL
IX0, IX1 = -P.CLEAR, P.L2 + P.CLEAR                        # inner pocket
IY0, IY1 = -P.CLEAR, P.L1 + P.CLEAR
Z_FLOOR_TOP = Z_USB_BOT - P.CLEAR
Z_BOTTOM = Z_FLOOR_TOP - P.FLOOR
Z_SPLIT = 0.0                                              # lid meets base at the LCD front face
Z_LID_TOP = P.S3 + P.GLASS_CLEAR + P.LID_TOP
Z_COLLAR_TOP = P.JOY_POCKET_TOP + P.JOY_ROOF_T
TONGUE_INSET = P.SKIRT + P.MATE_CLEAR
USB_Z0 = Z_USB_SHELL_BOT - P.USB_CLEAR
USB_Z1 = Z_USB_SHELL_BOT + P.P13 + P.USB_CLEAR
USB_HALF_W = P.P12 / 2 + P.USB_CLEAR


def plug_recess():
    zm = (USB_Z0 + USB_Z1) / 2
    yr0, yr1 = ((Y1 - P.PLUG_RECESS, Y1 + P.TOOL_EXT) if USB_SIGN > 0
                else (Y0 - P.TOOL_EXT, Y0 + P.PLUG_RECESS))
    rec = box(PICO_CX - P.PLUG_W / 2, PICO_CX + P.PLUG_W / 2,
              yr0, yr1, zm - P.PLUG_H / 2, zm + P.PLUG_H / 2)
    return fillet(rec.edges().filter_by(Axis.Y), P.PLUG_R)


def pry_notches():
    """Shared shallow recess across the skirt/base seam; wall remains behind."""
    cutters = []
    for x0, x1 in ((X0 - P.TOOL_EXT, X0 + P.PRY_DEPTH),
                   (X1 - P.PRY_DEPTH, X1 + P.TOOL_EXT)):
        cut = box(x0, x1, CY - P.PRY_W / 2, CY + P.PRY_W / 2,
                  -P.TONGUE_H - P.PRY_H / 2, -P.TONGUE_H + P.PRY_H / 2)
        cutters.append(fillet(cut.edges().filter_by(Axis.X), P.PRY_R))
    return cutters[0] + cutters[1]


def base():
    outer = rbox(X0, X1, Y0, Y1, Z_BOTTOM, Z_SPLIT, P.CORNER_R)
    pocket = rbox(IX0, IX1, IY0, IY1, Z_FLOOR_TOP, Z_SPLIT + P.TOOL_EXT, P.POCKET_R)
    b = outer - pocket
    # tongue: the top TONGUE_H of the wall steps in by SKIRT so the lid skirt sits flush outside
    step = rbox(X0, X1, Y0, Y1, Z_SPLIT - P.TONGUE_H, Z_SPLIT + P.TOOL_EXT, P.CORNER_R) \
        - rbox(X0 + TONGUE_INSET, X1 - TONGUE_INSET, Y0 + TONGUE_INSET, Y1 - TONGUE_INSET, Z_SPLIT - P.TONGUE_H - P.TOOL_EXT, Z_SPLIT + 2 * P.TOOL_EXT,
               P.CORNER_R - TONGUE_INSET)
    b -= step
    # snap bumps on the tongue's outer face, two per long side. Wedge: flat catch face
    # at the bottom, ramp on top so the lid skirt rides over it going down.
    zlo, zhi = P.SNAP_Z - P.SNAP_BUMP_T / 2, P.SNAP_Z + P.SNAP_BUMP_T / 2
    xl, xr = X0 + TONGUE_INSET, X1 - TONGUE_INSET
    for yb in (CY - P.L1 / 4, CY + P.L1 / 4):
        y0, y1 = yb - P.SNAP_LEN / 2, yb + P.SNAP_LEN / 2
        b += wedge_x([(xl + P.SNAP_ROOT_OVERLAP, zlo), (xl - P.SNAP_H, zlo), (xl, zhi), (xl + P.SNAP_ROOT_OVERLAP, zhi)], y0, y1)
        b += wedge_x([(xr - P.SNAP_ROOT_OVERLAP, zlo), (xr + P.SNAP_H, zlo), (xr, zhi), (xr - P.SNAP_ROOT_OVERLAP, zhi)], y0, y1)
    # ledge the LCD PCB rests on: the wall itself (pocket is the PCB outline + CLEAR), so the
    # PCB sits on the socket-clearance shelf. Shelf: fill the pocket back in below the LCD PCB
    # except where the sockets and the Pico live.
    # 45-degree underside grows inward gradually as the base prints upright.
    top = Z_LCD_BACK - P.SHELF_GAP
    left = PICO_CX - P.P2 / 2 - P.CLEAR
    right = PICO_CX + P.P2 / 2 + P.CLEAR
    b += wedge_x([(IX0 - P.EPS, top), (left, top),
                  (left, top - P.SHELF_T),
                  (IX0 - P.EPS, top - P.SHELF_T - (left - IX0))], IY0, IY1)
    b += wedge_x([(right, top), (IX1 + P.EPS, top),
                  (IX1 + P.EPS, top - P.SHELF_T - (IX1 - right)),
                  (right, top - P.SHELF_T)], IY0, IY1)
    # D5-USB aperture selects A1's higher position after V1 photo feedback.
    ywall0, ywall1 = (IY1 - P.TOOL_EXT, Y1 + P.TOOL_EXT) if USB_SIGN > 0 else (Y0 - P.TOOL_EXT, IY0 + P.TOOL_EXT)
    # Open to the rim for straight-down insertion of the already connected stack.
    b -= box(PICO_CX - USB_HALF_W, PICO_CX + USB_HALF_W,
             ywall0, ywall1, USB_Z0, Z_SPLIT + P.TOOL_EXT)
    b -= plug_recess()
    access = Pos(*ACCESS_C, (Z_BOTTOM + Z_FLOOR_TOP) / 2) * Cylinder(
        P.ACCESS_D / 2, P.FLOOR + 2 * P.TOOL_EXT)
    return b - pry_notches() - access


def lid():
    outer = rbox(X0, X1, Y0, Y1, Z_SPLIT - P.TONGUE_H, Z_LID_TOP, P.CORNER_R)
    # skirt cavity: over the tongue
    cav = rbox(X0 + P.SKIRT, X1 - P.SKIRT, Y0 + P.SKIRT, Y1 - P.SKIRT, Z_SPLIT - P.TONGUE_H - P.TOOL_EXT, Z_SPLIT,
               P.CORNER_R - P.SKIRT)
    # ceiling cavity: over the PCB, up to the glass clearance
    cav2 = rbox(IX0, IX1, IY0, IY1, Z_SPLIT - P.TOOL_EXT, P.S3 + P.GLASS_CLEAR, P.CAVITY_R)
    l = outer - cav - cav2
    # Raised retaining roof: the ball passes through, the wider lip cannot.
    jx, jy = JOY_C
    l += Pos(jx, jy, (Z_LID_TOP - P.EPS + Z_COLLAR_TOP) / 2) * Cylinder(
        P.JOY_COLLAR_D / 2, Z_COLLAR_TOP - Z_LID_TOP + P.EPS)
    # Four contacts above the supporting side shelves. Bare PCB needs bench confirmation.
    for px in (P.LID_PAD_INSET, P.L2 - P.LID_PAD_INSET - P.LID_PAD):
        for py in (P.LID_PAD_INSET, P.L1 - P.LID_PAD_INSET - P.LID_PAD):
            l += box(px, px + P.LID_PAD, py, py + P.LID_PAD, P.LID_PAD_GAP, P.S3 + P.GLASS_CLEAR + P.EPS)
    # Lid fin fills the assembly channel, leaving USB clearance below it.
    fy0, fy1 = (IY1, Y1) if USB_SIGN > 0 else (Y0, IY0)
    l += box(PICO_CX - USB_HALF_W + P.USB_FIN_CLEAR,
             PICO_CX + USB_HALF_W - P.USB_FIN_CLEAR, fy0, fy1,
             USB_Z1, P.S3 + P.GLASS_CLEAR)
    l -= plug_recess()
    # snap windows: through the skirt where the bumps are (the old blind notches were cut on
    # the cavity side and removed nothing). A window also lets a fingernail push a bump in to open.
    zlo = P.SNAP_Z - P.SNAP_BUMP_T / 2 - P.SNAP_WIN_CLEAR
    zhi = P.SNAP_Z + P.SNAP_BUMP_T / 2 + P.SNAP_WIN_CLEAR
    for yb in (CY - P.L1 / 4, CY + P.L1 / 4):
        y0, y1 = yb - P.SNAP_LEN / 2 - P.SNAP_END_CLEAR, yb + P.SNAP_LEN / 2 + P.SNAP_END_CLEAR
        l -= box(X0 - P.TOOL_EXT, X0 + P.SKIRT + P.EPS, y0, y1, zlo, zhi)
        l -= box(X1 - P.SKIRT - P.EPS, X1 + P.TOOL_EXT, y0, y1, zlo, zhi)
        # Flexible bands anchored at both ends. Inverted printing bridges the
        # slit; a free-ended horizontal cantilever would begin in mid-air.
        end = yb + P.ARM_LEN / 2
        start = yb - P.ARM_LEN / 2
        for xa, xb in ((X0 - P.TOOL_EXT, X0 + P.SKIRT + P.EPS),
                       (X1 - P.SKIRT - P.EPS, X1 + P.TOOL_EXT)):
            l -= box(xa, xb, start, end,
                     P.ARM_ROOF, P.ARM_ROOF + P.ARM_SLOT)
    # screen window
    gx, gy = GLASS_C
    w = P.WINDOW_CLEAR
    l -= rbox(gx - P.S2 / 2 - w, gx + P.S2 / 2 + w, gy - P.S1 / 2 - w, gy + P.S1 / 2 + w, -P.TOOL_EXT, Z_COLLAR_TOP + P.TOOL_EXT, P.WINDOW_R)
    # button pocket: the caps' flanges live under the plate, above the plungers
    pocket_top = P.B5 + P.CAP_FLANGE_T + P.CAP_POCKET_CLEAR
    bx0 = min(b[0] for b in BUTTONS) - P.CAP_FLANGE_W / 2 - P.POCKET_MARGIN
    bx1 = max(b[0] for b in BUTTONS) + P.CAP_FLANGE_W / 2 + P.POCKET_MARGIN
    by0 = min(b[1] for b in BUTTONS) - P.CAP_FLANGE_D / 2 - P.POCKET_MARGIN
    by1 = max(b[1] for b in BUTTONS) + P.CAP_FLANGE_D / 2 + P.POCKET_MARGIN
    l -= rbox(bx0, bx1, by0, by1, -P.TOOL_EXT, pocket_top, P.WINDOW_R)
    # Rectangular button holes key the caps against 90-degree insertion.
    hw = P.CAP_W + 2 * P.CAP_HOLE_CLEAR
    hd = P.CAP_D + 2 * P.CAP_HOLE_CLEAR
    for bx, by in BUTTONS:
        l -= rbox(bx - hw / 2, bx + hw / 2, by - hd / 2, by + hd / 2, pocket_top - P.TOOL_EXT, Z_LID_TOP + P.TOOL_EXT, P.CAP_R + P.CAP_HOLE_CLEAR)
    # Large underside pocket clears silver body and moving flange. Smaller
    # throat above it admits the ball during assembly and captures the lip.
    jx, jy = JOY_C
    l -= Pos(jx, jy, (P.JOY_POCKET_TOP - P.TOOL_EXT) / 2) * Cylinder(
        P.JOY_POCKET_D / 2, P.JOY_POCKET_TOP + P.TOOL_EXT)
    l -= Pos(jx, jy, Z_COLLAR_TOP / 2) * Cylinder(P.JOY_HOLE_D / 2, Z_COLLAR_TOP + 2 * P.TOOL_EXT)
    return l - pry_notches()


def button_caps():
    """A cap per button: a rectangular post through the lid hole, a flange underneath
    that rests on the plunger and stops the cap coming out the top."""
    caps = None
    for bx, by in BUTTONS:
        c = rbox(bx - P.CAP_FLANGE_W / 2, bx + P.CAP_FLANGE_W / 2, by - P.CAP_FLANGE_D / 2, by + P.CAP_FLANGE_D / 2,
                 P.B5, P.B5 + P.CAP_FLANGE_T, P.CAP_R)
        c += rbox(bx - P.CAP_W / 2, bx + P.CAP_W / 2, by - P.CAP_D / 2, by + P.CAP_D / 2,
                  P.B5 + P.CAP_FLANGE_T - P.EPS, Z_LID_TOP + P.CAP_PROUD, P.CAP_R)
        caps = c if caps is None else caps + c
    return caps


def joystick_cap(socket_clear=None):
    jx, jy = JOY_C
    bot = P.J6 - P.JOY_ENGAGE
    cap = Pos(jx, jy, (bot + P.JOY_BALL_Z) / 2) * Cylinder(
        P.JOY_NECK_D / 2, P.JOY_BALL_Z - bot)
    cap += Pos(jx, jy, P.JOY_FLANGE_Z + P.JOY_FLANGE_T / 2) * Cylinder(
        P.JOY_FLANGE_D / 2, P.JOY_FLANGE_T)
    cap += Pos(jx, jy, P.JOY_BALL_Z) * Sphere(P.JOY_BALL_D / 2)
    s = (P.J4 + (P.JOY_SOCKET_CLEAR if socket_clear is None else socket_clear)) / 2
    socket = box(jx - s, jx + s, jy - s, jy + s, bot - P.TOOL_EXT, P.J6 + P.JOY_SOCKET_TIP_CLEAR)
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
