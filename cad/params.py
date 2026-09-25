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
S_DU = -0.2905  # SC1, scan01
S_DV = -0.1393  # SC1, scan01

# ---- B. Four tact switches, labels Y X B A left to right
B1 = 3.34     # B1 casing size in y, cal
B2 = 4.42     # B2 casing size in x, cal (4.30 second reading)
B3 = 1.81     # B3 casing top above PCB front, cal
B4X = 2.38    # B4 plunger oval, x, cal
B4Y = 3.00    # B4 plunger oval, y, cal
B5 = 2.61     # B5 plunger top above PCB front at rest, cal
B6 = 0.38     # B6 plunger travel, cal
B_OFFSETS = ((-8.4400, -22.1949), (-2.7159, -22.3382),
             (2.8723, -22.3153), (8.5746, -22.2187))  # BC1 x,y

# ---- J. Joystick
J_BASE_X = 7.22   # J1/J2 silver base plan size (fitted diamond, blurred), scan01
J_BASE_Y = 8.81
J3 = 3.0      # J3 body height above PCB — NOT measured; guess for the render, confirm cal
J4 = 1.86     # J4 stem, square across flats, cal
J4B = 2.94    # J4b lip at the stem base, cal
J6 = 5.00     # J6 stem tip above PCB front, centred, cal
J_DU = 19.8792  # JC1
J_DV = -0.0529  # JC1
J_BASE_DU, J_BASE_DV = 19.4936, 0.2730  # JC2; not concentric with stem
J_BASE_ANGLE = 45  # H3, render assumption
HEADER_W, HEADER_L = 2.54, 50.8  # H1, provisional render envelope
PICO_R, USB_IN = 1.0, 7.0  # H2, render assumptions
FLAG_T, FLAG_IN = 0.3, 1.0  # H5, illustrative envelope

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
PICO_OFFSET_X = 0.0       # A3/L8 assumption: centred, not measured
PICO_OFFSET_Y = 0.0       # A3/L8 assumption: centred, not measured
USB_END = "top"           # USB-C at the joystick end (+y). Austin, 2026-09-24, looking at the stack

# ---- Case. Our choices (DESIGN.md), not measurements
CLEAR = 0.30       # gap between any PCB edge and a wall
WALL = 2.20        # D4-FIT: skirt + mating gap + 1.2 tongue
MATE_CLEAR = 0.20  # D4-FIT: radial gap, not zero-contact geometry
FLOOR = 1.60       # base floor
LID_TOP = 6.25     # D6-LID: uniform flat surface z8.6, no local collar
GLASS_CLEAR = 0.30 # air above the glass
CORNER_R = 3.0     # outside vertical corner radius
SNAP_H = 0.45      # D4-FIT, requires 0.25 outward skirt flex
SNAP_LEN = 4.0     # D4-FIT, fits near the end of each flexible arm
SNAP_Z = -1.2      # snap bump centre height (tongue spans -3..0); leaves a 1.2 rim of skirt below the window
SNAP_BUMP_T = 1.0  # bump height in z: flat catch face below, ramp above so the lid slides on
SNAP_WIN_CLEAR = 0.1  # window in the skirt past the bump, each side (z); 0.3 each end (y)
TONGUE_H = 3.0     # how far the lid skirt overlaps the base
SKIRT = 0.80       # lid skirt thickness (the base wall steps in by this much)
WINDOW_CLEAR = 0.40  # screen window past the glass, each side
CAP_W = 4.2        # button cap, square, through the lid hole (pitch is 5.70, B8p)
CAP_D = 5.4        # D5-BUTTON, width perpendicular to the button row
CAP_R = 0.8        # cap corner radius
CAP_HOLE_CLEAR = 0.25   # hole = CAP_W + 2 x this -> 4.70, leaving a 1.0 web between holes
CAP_FLANGE_W = 4.85 # D5-BUTTON, smaller row-axis lips
CAP_FLANGE_D = 6.3  # D5-BUTTON, long-axis retaining flange
CAP_FLANGE_T = 0.8 # flange thickness; rests on the plunger top (B5)
CAP_PROUD = 1.8    # D5-BUTTON, more exposed height
CAP_POCKET_CLEAR = 0.15  # air above the flange inside the lid
POCKET_R = 0.5     # D4-SUPPORT: sharp PCB clears even at ±0.1 XY displacement
SHELF_T = 0.80     # D4-SUPPORT: bearing strip over sloped underside
SHELF_GAP = 0.0    # D4-SUPPORT: board rests at its modelled z datum
ARM_LEN = 14.0    # D4-FIT
ARM_ROOF = -0.30  # D4-FIT
ARM_SLOT = 0.60   # D4-FIT
# R5: cap installs on the board FIRST; lid passes over ball and retains lip.
JOY_NECK_D = 5.0   # D6-SOCKET: restore full-case4010773 lower interface
JOY_ENGAGE = 1.6   # D6-SOCKET
JOY_FLANGE_D = 10.4  # D6-JOY, captive lower lip
JOY_FLANGE_Z = 5.0   # D5-JOY
JOY_FLANGE_T = 0.6   # D6-JOY, upper taper avoids inverted-print overhang
JOY_BALL_D = 7.0     # D5-JOY, smaller than throat for lid installation
JOY_BALL_Z = 11.4    # D5-JOY, centre height
JOY_POCKET_D = 13.0  # D6-LID
JOY_POCKET_TOP = 7.4 # D6-LID, hidden underside relief
JOY_BALL_FLAT = 0.8  # D6-JOY, small planar top for inverted printing
JOY_ROOF_T = 1.2     # D5-JOY
JOY_SOCKET_CLEAR = 0.15  # D6-SOCKET, restore earlier2.01 socket
JOY_SOCKET_SAMPLES = (0.0, 0.10, 0.20)  # D4-JOY, labelled by print filenames
JOY_SOCKET_TIP_CLEAR = 0.3  # D6-SOCKET, restore earlier socket roof
JOY_HOLE_D = 9.6    # D6-LID: ball < throat < flange
JOY_SCREEN_WEB = 0.4 # D6-LID, retain wall between pocket and screen opening
USB_CLEAR = 0.35   # D5-USB, cutout past shell each side
USB_STAND = 2.41   # D5-USB, selects A1 reading; P15 retained for floor
A1_USB, A1_PCB = 19.95, 17.54  # A1 glass to USB-C shell / to Pico PCB back. Disagrees with P15 by 0.84; the slot covers both
PLUG_W = 12.5      # cable plug overmould width  — GUESS until measured (report ask 4)
PLUG_H = 6.0       # D5-USB, cable recess trial; verify real plug
PLUG_RECESS = 1.0  # recess in the end wall's outer face so the overmould reaches the shell face
LID_PAD = 1.60     # D4-SUPPORT: four small corner contacts above side shelves
LID_PAD_INSET = 0.50  # D4-SUPPORT
LID_PAD_GAP = 0.05   # pad face above the PCB front
USB_FIN_CLEAR = 0.25  # D4-USB
EPS = 0.01           # D4-CAD, boolean overlap only
TOOL_EXT = 1.0       # D4-CAD, cutter extension only
SNAP_ROOT_OVERLAP = 0.20  # D4-CAD
SNAP_END_CLEAR = 0.30     # D4-CAD
POCKET_MARGIN = 0.30     # D4-CAD
CAVITY_R = 0.50          # D4-CAD
WINDOW_R = 0.80          # D4-CAD
PLUG_R = 1.0             # D4-CAD
PRY_W = 6.0              # D5-PRY
PRY_H = 1.6              # D5-PRY
PRY_DEPTH = 1.0          # D5-PRY
PRY_R = 0.5              # D5-PRY
ACCESS_DX = 3.2868       # PINK-BTN-SCAN, opposite-face reflection
ACCESS_DY = 13.4370      # PINK-BTN-SCAN, toward USB
ACCESS_D = 4.0          # D5-ACCESS
BOARD_BUTTON_D = 2.4    # D5-ACCESS, illustrative proxy
BOARD_BUTTON_H = 1.8    # D5-ACCESS, unmeasured height assumption
