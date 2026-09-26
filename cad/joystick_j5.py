"""J5 (v1.4 joystick): J4's outside, with the stick socket narrowing 0.5 mm
sooner so the cap rides higher on the stick and leaves press-in travel.
Rows J5-* in MEASUREMENTS.
"""
import math
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4

LIFT=.3  # J5-LIFT: rides this much higher on the stick = press-in room.
# 0.5 limits tilt to ~6 deg in the J1-CHECK scenarios (flange rim meets the
# roof at the hole); 0.3 stays clear to ~9. Both are printed to compare.
VARIANTS=(.3,.5)  # J5-VARIANTS
SQUARE_DEPTH=J2.SQUARE_DEPTH  # unchanged 2.0 grip on the square stem

def cavity(lift):
    ROUND_DEPTH=J2.ROUND_DEPTH-lift  # round mouth shortens; the square starts sooner
    circle=J.cylinder(J2.ROUND_D,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+ROUND_DEPTH)
    half=J.SOCKET/2
    square=J.M.box(-half,half,-half,half,J.BOTTOM+ROUND_DEPTH-J.P.EPS,J.BOTTOM+ROUND_DEPTH+SQUARE_DEPTH)
    return circle+square

def cap(lift=None):
    lift=LIFT if lift is None else lift
    j4,_=J4.cap();_,blank=J2.cap();old,_=J2.cap()
    solid=j4+(blank-old)  # J4 with its (J2) socket filled back in
    return solid-cavity(lift),j4

def checks(lift=None):
    lift=LIFT if lift is None else lift
    ROUND_DEPTH=J2.ROUND_DEPTH-lift
    c,j4=cap(lift)
    def vol(s):return sum(x.volume for x in s.solids())
    sock=J.cylinder(J.NECK,J.BOTTOM,J.BOTTOM+J2.ROUND_DEPTH+J2.SQUARE_DEPTH+.5)  # from the cap's own bottom face
    expected=math.pi*(J2.ROUND_D/2)**2*ROUND_DEPTH+J.SOCKET**2*SQUARE_DEPTH
    outside=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM-J.P.TOOL_EXT,J.BALL_Z+J.BALL)-sock
    probe=J.M.box(-.5,.5,-.5,.5,J.BOTTOM+ROUND_DEPTH+SQUARE_DEPTH+.01,J.BOTTOM+ROUND_DEPTH+SQUARE_DEPTH+.02)
    return c,dict(
        joystick_valid_single_solid=c.is_valid and len(c.solids())==1,
        joystick_socket_volume_exact=abs(vol(sock-c)-expected)<1e-4,
        joystick_socket_shorter_by_lift_closed_above=vol(probe-c)<1e-6,
        joystick_outside_identical_to_J4=vol((c & outside)-(j4 & outside))<1e-5 and vol((j4 & outside)-(c & outside))<1e-5,
        joystick_lift_within_round_mouth=0<lift<J2.ROUND_DEPTH)
