"""J4 (v1.4 joystick): J2 with the top of the ball cut flat so the joystick's
press-in click is easy to hit. Socket, neck, flange and ball centre unchanged.
Rows J4-* in MEASUREMENTS.
"""
import math
from build123d import Axis, fillet
import joystick_test as J
import joystick_j2 as J2

FLAT_D=5.0  # J4-FLAT: thumb pad diameter
RIM_R=.6  # J4-RIM: softened edge between pad and ball
FLAT_Z=J.BALL_Z+math.sqrt((J.BALL/2)**2-(FLAT_D/2)**2)  # pad height, cap coords

def cap():
    old,_=J2.cap()
    c=old-J.M.box(-J.BALL,J.BALL,-J.BALL,J.BALL,FLAT_Z,J.BALL_Z+J.BALL)
    rim=[e for e in c.edges() if abs(e.bounding_box().min.Z-FLAT_Z)<1e-6 and abs(e.bounding_box().max.Z-FLAT_Z)<1e-6]
    return fillet(rim,RIM_R),old

def checks():
    c,old=cap()
    below=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM-J.P.TOOL_EXT,FLAT_Z-RIM_R-J.P.EPS)
    def vol(s):return sum(x.volume for x in s.solids())
    top=[f for f in c.faces() if abs(f.center().Z-FLAT_Z)<1e-6 and f.normal_at().Z>.9]
    return c,dict(
        joystick_valid_single_solid=c.is_valid and len(c.solids())==1,
        joystick_only_removes_material=vol(c-old)<1e-5,
        joystick_unchanged_below_pad=vol((c & below)-(old & below))<1e-5 and vol((old & below)-(c & below))<1e-5,
        joystick_has_flat_pad=len(top)==1 and top[0].area>math.pi*((FLAT_D/2-RIM_R)**2)*.95,
        joystick_height_drop_mm_is=round(J.BALL_Z+J.BALL/2-FLAT_Z,3)>0)
