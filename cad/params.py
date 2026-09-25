"""Every number the case uses. One line each, the MEASUREMENTS.md row in the
comment. Nothing in cad/ may hold a dimension that is not here.

Frame ("chosen corner" in MEASUREMENTS.md): looking at the screen, joystick
up. Origin = bottom-left corner of the LCD PCB. +x right, +y up toward the
joystick, +z out of the screen. z = 0 is the LCD PCB FRONT face (glass side).
The stack hangs below in -z.
"""

# ---- L. Waveshare Pico-LCD-1.3 board
L1 = 52.5     # L1 board length (y), cal
L2 = 26.44    # L2 board width (x), cal
L3 = 1.97     # L3 PCB thickness, cal
L7 = 8.69     # L7 female header socket height below the PCB back, cal
L4 = 1.5      # L4 PCB corner radius — NOT measured, a guess for the render; confirm cal

# ---- S. Screen (glass)
S1 = 26.48    # S1 glass length (y), scan01
S2 = 25.19    # S2 glass width (x), scan01
S3 = 2.05     # S3 glass top above PCB front, cal
S_DU = -0.29  # glass centre offset from board centre, y, scan01 (glass_centre_uv u)
S_DV = -0.14  # glass centre offset from board centre, x, scan01 (glass_centre_uv v)

# ---- B. Four tact switches, labels Y X B A left to right
B1 = 3.34     # B1 casing size in y, cal
B2 = 4.42     # B2 casing size in x, cal (4.30 second reading)
B3 = 1.81     # B3 casing top above PCB front, cal
B4X = 2.38    # B4 plunger oval, x, cal
B4Y = 3.00    # B4 plunger oval, y, cal
B5 = 2.61     # B5 plunger top above PCB front at rest, cal
B6 = 0.38     # B6 plunger travel, cal
B_DU = -22.27                          # button row offset from board centre, y, scan01 (mean of four)
B_DV = (-8.44, -2.72, 2.87, 8.57)      # button centres offset from board centre, x, scan01 (Y X B A)

# ---- J. Joystick
J_BASE_X = 7.22   # J1/J2 silver base plan size (fitted diamond, blurred), scan01
J_BASE_Y = 8.81
J3 = 3.0      # J3 body height above PCB — NOT measured; guess for the render, confirm cal
J4 = 1.86     # J4 stem, square across flats, cal
J4B = 2.94    # J4b lip at the stem base, cal
J6 = 5.00     # J6 stem tip above PCB front, centred, cal
J_DU = 19.88  # stem centre offset from board centre, y, scan01
J_DV = -0.05  # stem centre offset from board centre, x, scan01

# ---- PINK. USB-C RP2040 clone
P1 = 51.04    # PINK-P1 length, cal
P2 = 20.82    # PINK-P2 width, cal
P3 = 1.23     # PINK-P3 PCB thickness, cal
P11 = 2.47    # PINK-P11 USB-C shell overhang past the short edge, scan01
P12 = 8.87    # PINK-P12 USB-C shell width, cal
P13 = 3.08    # PINK-P13 USB-C shell height, cal
P15 = 3.25    # PINK-P15 tallest part above the PCB, component side (the shell), cal
P10 = 17.78   # P10 header row spacing (ds, 7 x 2.54), the clone matches the hat's sockets by construction

# ---- F. FPC tape at the LCD's right edge (seen in scan01; the case pocket must not pinch it)
F_OUT = 4.0   # how far the blue tape protrudes past the PCB edge, scan01 (soft) — UNRESOLVED, see report
F_Y0, F_Y1 = 22.0, 30.0   # its span along y, scan01 (soft)

# ---- A. Stack
A2 = 12.29    # A2 gap, LCD PCB back to Pico PCB top (the face toward the LCD), derived from cal

# Pico placement under the hat. ASSUMPTIONS until measured (rows A3 / L8):
PICO_CENTRED_X = True     # header rows symmetric about the hat's centreline
PICO_CENTRED_Y = True     # 51.04 board centred on the 52.5 hat
USB_END = "top"           # USB-C at the joystick end (+y). Austin, 2026-09-24, looking at the stack

# ---- Case. Our choices (DESIGN.md), not measurements
CLEAR = 0.30       # gap between any PCB edge and a wall
WALL = 2.00        # side walls; minus SKIRT leaves a 1.2 tongue at the top (0.4 would be one perimeter — found 2026-09-24)
FLOOR = 1.60       # base floor
LID_TOP = 2.25     # lid plate over the glass (thick enough that the button pocket leaves 1.1 above the flanges)
GLASS_CLEAR = 0.30 # air above the glass
CORNER_R = 3.0     # outside vertical corner radius
SNAP_H = 0.50      # snap bump height
SNAP_LEN = 8.0     # snap bump length along the wall
SNAP_Z = -1.2      # snap bump centre height (tongue spans -3..0); leaves a 1.2 rim of skirt below the window
SNAP_BUMP_T = 1.0  # bump height in z: flat catch face below, ramp above so the lid slides on
SNAP_WIN_CLEAR = 0.1  # window in the skirt past the bump, each side (z); 0.3 each end (y)
TONGUE_H = 3.0     # how far the lid skirt overlaps the base
SKIRT = 0.80       # lid skirt thickness (the base wall steps in by this much)
WINDOW_CLEAR = 0.40  # screen window past the glass, each side
CAP_W = 4.2        # button cap, square, through the lid hole (pitch is 5.70, B8p)
CAP_R = 0.8        # cap corner radius
CAP_HOLE_CLEAR = 0.25   # hole = CAP_W + 2 x this -> 4.70, leaving a 1.0 web between holes
CAP_FLANGE_W = 5.3 # flange under the lid so the cap cannot come out the top; 0.4 gap to its neighbour
CAP_FLANGE_T = 0.8 # flange thickness; rests on the plunger top (B5)
CAP_PROUD = 1.0    # how far the cap stands above the lid
CAP_POCKET_CLEAR = 0.15  # air above the flange inside the lid
POCKET_R = 0.8     # inside corner radius of the PCB pocket; with CLEAR 0.3 it clears even a sharp PCB corner by 0.09 (L4 unmeasured)
SHELF_T = 2.0      # ledge under the LCD PCB edges, beside the Pico
# Joystick cap, v3: a thin neck on the stem through the hole, a disc above the lid.
# The neck stays clear of the silver base; the disc sits high enough to tilt.
JOY_NECK_D = 5.0   # neck diameter
JOY_ENGAGE = 1.6   # how far the neck's square socket goes down the stem from the tip (J6)
JOY_DISC_D = 12.8  # top disc; covers the 12.0 hole, stays clear of the screen window
JOY_DISC_T = 1.5   # top disc thickness
JOY_DISC_GAP = 1.2 # disc underside above the lid top: ~10 deg tilt before the rim touches (J7 unmeasured)
JOY_SOCKET_CLEAR = 0.15    # square socket over the 1.86 stem, total
JOY_SOCKET_TIP_CLEAR = 0.3 # socket roof above the stem tip (J6)
JOY_HOLE_D = 12.0  # joystick opening. Clears the scan's silver-base diamond (8.81 x 7.22 turned, reaches r 5.70) by 0.3, whatever J3 is
USB_CLEAR = 0.50   # USB-C cutout past the shell, each side
A1_USB, A1_PCB = 19.95, 17.54  # A1 glass to USB-C shell / to Pico PCB back. Disagrees with P15 by 0.84; the slot covers both
PLUG_W = 12.5      # cable plug overmould width  — GUESS until measured (report ask 4)
PLUG_H = 7.0       # cable plug overmould height — GUESS until measured
PLUG_RECESS = 1.0  # recess in the end wall's outer face so the overmould reaches the shell face
LID_PAD = 3.0      # square pads under the lid that hold the LCD PCB down, top two corners (bare PCB in scan01)
LID_PAD_INSET = 0.8  # pad edge in from the PCB edges
LID_PAD_GAP = 0.05   # pad face above the PCB front
