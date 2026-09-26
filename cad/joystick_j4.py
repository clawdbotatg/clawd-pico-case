"""J4 (v1.4 joystick): a bigger ball than J2, cut flat at its widest point
(a half ball), so the joystick's press-in click is easy to hit. The ball just
passes the lid's 8 mm hole. Socket, neck, flange and ball centre unchanged.
Rows J4-* in MEASUREMENTS.
"""
import math
from build123d import Pos, Sphere, fillet
import joystick_test as J
import joystick_j2 as J2

FLAT_Z=J.BALL_Z  # J4-HALF: flat top through the ball centre, full 7 mm across
BALL_D=J.HOLE-2*.3  # J4-BALL: 7.4, 0.3 mm each side in the 8 mm lid hole; 7.5/7.6 graze the hole at 10 deg tilt
RIM_R=.3  # J4-RIM: edge break only, flat runs nearly to the edge

def cap():
    old,_=J2.cap()
    c=(old+Pos(0,0,J.BALL_Z)*Sphere(BALL_D/2))-J.M.box(-BALL_D,BALL_D,-BALL_D,BALL_D,FLAT_Z,J.BALL_Z+BALL_D)
    rim=[e for e in c.edges() if abs(e.bounding_box().min.Z-FLAT_Z)<1e-6 and abs(e.bounding_box().max.Z-FLAT_Z)<1e-6]
    return fillet(rim,RIM_R),old

def checks():
    c,old=cap()
    # Below the ball (neck, flange, socket) must match J2 exactly.
    below=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM-J.P.TOOL_EXT,J.BALL_Z-BALL_D/2-J.P.EPS)
    def vol(s):return sum(x.volume for x in s.solids())
    pad=[f for f in c.faces() if abs(f.center().Z-FLAT_Z)<1e-6 and f.normal_at().Z>.9]
    return c,dict(
        joystick_valid_single_solid=c.is_valid and len(c.solids())==1,
        joystick_unchanged_below_ball=vol((c & below)-(old & below))<1e-5 and vol((old & below)-(c & below))<1e-5,
        joystick_flat_top_near_full_ball=len(pad)==1 and pad[0].area>math.pi*((BALL_D/2-RIM_R)**2)*.95,
        joystick_ball_passes_lid_hole=abs((c & J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BALL_Z-BALL_D/2,J.BALL_Z+1)).bounding_box().size.X-BALL_D+.05)<.05 and BALL_D<J.HOLE,  # 0.3 rim trims the equator slightly
        joystick_top_at_ball_centre=abs(c.bounding_box().max.Z-J.BALL_Z)<1e-6)
