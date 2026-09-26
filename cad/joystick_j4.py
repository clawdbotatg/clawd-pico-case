"""J4 (v1.4 joystick): J2's ball topped with a flat "hat" so the joystick's
press-in click is easy to hit. The ball narrows to a waist near its top, a
45 degree flare comes back out to a flat disc, then a flat top. Socket, neck,
flange and ball centre unchanged. Rows J4-* in MEASUREMENTS.
"""
import math
from build123d import Pos, Cone, fillet
import joystick_test as J
import joystick_j2 as J2

WAIST_D=5.5  # J4-WAIST: ball cut where it has narrowed to this diameter
HAT_D=7.0  # J4-HAT: disc diameter = ball diameter
RIM_T=.6  # J4-HAT: disc edge height above the flare
TOP_R=.5  # J4-RIM: rounded top edge; flat pad ~ HAT_D - 2*TOP_R
WAIST_Z=J.BALL_Z+math.sqrt((J.BALL/2)**2-(WAIST_D/2)**2)
FLARE_H=(HAT_D-WAIST_D)/2  # 45 degrees: prints flange-down without support
TOP_Z=WAIST_Z+FLARE_H+RIM_T

def cap():
    old,_=J2.cap()
    c=old-J.M.box(-J.BALL,J.BALL,-J.BALL,J.BALL,WAIST_Z,J.BALL_Z+J.BALL)
    c+=Pos(0,0,WAIST_Z+FLARE_H/2-J.P.EPS/2)*Cone(WAIST_D/2,HAT_D/2,FLARE_H+J.P.EPS)
    c+=J.cylinder(HAT_D,WAIST_Z+FLARE_H-J.P.EPS,TOP_Z)
    top=[e for e in c.edges() if abs(e.bounding_box().min.Z-TOP_Z)<1e-6 and abs(e.bounding_box().max.Z-TOP_Z)<1e-6]
    return fillet(top,TOP_R),old

def checks():
    c,old=cap()
    below=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM-J.P.TOOL_EXT,WAIST_Z-J.P.EPS)
    def vol(s):return sum(x.volume for x in s.solids())
    pad=[f for f in c.faces() if abs(f.center().Z-TOP_Z)<1e-6 and f.normal_at().Z>.9]
    bb,ob=c.bounding_box(),old.bounding_box()
    return c,dict(
        joystick_valid_single_solid=c.is_valid and len(c.solids())==1,
        joystick_unchanged_below_waist=vol((c & below)-(old & below))<1e-5 and vol((old & below)-(c & below))<1e-5,
        joystick_flat_pad_about_6mm=len(pad)==1 and pad[0].area>math.pi*((HAT_D/2-TOP_R)**2)*.95,
        joystick_height_same_as_J2=abs(bb.max.Z-ob.max.Z)<.05,
        joystick_hat_no_wider_than_ball=all(v<=J.BALL+1e-6 for v in tuple((c & J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,WAIST_Z,TOP_Z+1)).bounding_box().size)[:2]),
        joystick_hat_passes_lid_hole=HAT_D<J.HOLE)
