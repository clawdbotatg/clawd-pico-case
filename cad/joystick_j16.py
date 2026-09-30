"""J16: J15 with a square-only socket and four diagonal flares on the flange.
Austin, 2026-09-30, after printing 12 J15:
 1. Push hard and the cap's round mouth (3.0) slides down over the stem's
    2.94 base lip; then the centre press stops working. Make the hole the
    1.90 square all the way down, so the lip is a hard stop.
 2. Pull hard and the cap comes out through the lid: the 8.6 disc overlaps
    the 8 mm hole by only 0.3. Keep the round flange (no see-through gap) and
    add flares at NE, NW, SE, SW.
The stem's flats face up/down/left/right (J11-III, square in line with the
socket, was the one that cleaned up the directions), so the socket diagonals
are the board diagonals.
Row J16-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j16.py
"""
import hashlib
import json
from pathlib import Path
from build123d import Pos, Rot
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j13 as J13
import joystick_j14 as J14
import joystick_j15 as J15
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j16'
OUT=ROOT/'renders/v1.4/joystick-j16'
SQUARE=J15.SQUARE  # 1.90 grip, unchanged
LIFT=J14.LIFT      # 0.6: the square roof stays where J15's is, so the cap rides the same
MOUTH_CH=.25       # J16-SOCKET: 45 deg chamfer at the bed face against elephant foot; 2.40 < 2.94 lip
FLARE_W,FLARE_TIP,FLARE_T=1.2,4.8,.24  # J16-FLARE: width, tip radius (0.8 past the hole), thickness past the hole edge;
# model lid room at VII height = VI's 17.6 deg (tested clean); wider/longer/thicker flares lose it

def cavity():
    z0=J.BOTTOM+J2.ROUND_DEPTH-LIFT;roof=z0+J2.SQUARE_DEPTH;h=SQUARE/2  # J15's grip and roof
    return (J.M.box(-h,h,-h,h,J.BOTTOM-J.P.TOOL_EXT,roof)+J7.frustum(SQUARE,0,roof,roof+SQUARE/2)
            +J7.frustum(SQUARE+2*MOUTH_CH,SQUARE,J.BOTTOM,J.BOTTOM+MOUTH_CH)
            +J.M.box(-h-MOUTH_CH,h+MOUTH_CH,-h-MOUTH_CH,h+MOUTH_CH,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.P.EPS))

def flares(w=None,tip=None):
    w=w or FLARE_W;tip=tip or FLARE_TIP
    out=[]
    for a in (45,135,225,315):
        out.append(Rot(0,0,a)*J.M.box(J.NECK/2-.2,tip,-w/2,w/2,J.BOTTOM,J.BOTTOM+J.FLANGE_T)
                   & J.cylinder(2*tip,J.BOTTOM-1,J.BOTTOM+1))  # rounded tips
    return out

def thin(t):
    """Everything of the flange above thickness t outside the 8 mm hole (J13-THIN's
    taper from r 3.4), so the flares sit as low as the disc edge under the lid."""
    z0,z1=J.BOTTOM+t,J.BOTTOM+J.FLANGE_T;r0,r1=J13.TAPER
    from build123d import Cone
    keep=Pos(0,0,(z0+z1)/2)*Cone(r1,r0,z1-z0)
    return J.cylinder(14,z0,z1+J.P.EPS)-keep-J.cylinder(J.NECK,z0-1,z1+1)

def cap(w=None,tip=None,t=None):
    c=J15.cap()+(J8.cavity(SQUARE,LIFT) & J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # refill J15's socket
    fl=None
    for f in flares(w,tip):fl=f if fl is None else fl+f
    fl-=thin(t or FLARE_T)
    return c+fl-cavity()

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    def diff(a,b):return vol(a-b) if a.solids() else 0.
    c=cap();j15=J15.cap()
    z0=J.BOTTOM+J2.ROUND_DEPTH-LIFT;roof=z0+J2.SQUARE_DEPTH
    lip_band=J.cylinder(2.94,J.BOTTOM+MOUTH_CH+.01,roof)  # where the 2.94 lip could ride up
    upper=J.M.box(-6,6,-6,6,J.BOTTOM+J.FLANGE_T+.01,20)
    core=J.cylinder(3.2,J.BOTTOM-1,roof+2)  # the socket, changed on purpose
    checks=dict(
        valid_single_solid=c.is_valid and len(c.solids())==1,
        socket_square_all_the_way=diff(J.M.box(-SQUARE/2,SQUARE/2,-SQUARE/2,SQUARE/2,J.BOTTOM,roof),J.M.box(-6,6,-6,6,-9,20)-c)<1e-6
            and vol(c & J.M.box(-SQUARE/2,SQUARE/2,-SQUARE/2,SQUARE/2,J.BOTTOM,roof))<1e-6,
        lip_cannot_enter=vol(lip_band-c-J.M.box(-SQUARE/2,SQUARE/2,-SQUARE/2,SQUARE/2,J.BOTTOM,roof+2))<1e-6,
        mouth_chamfer_under_lip=SQUARE+2*MOUTH_CH<2.94,
        roof_where_J15_has_it=diff(J.M.box(-SQUARE/2,SQUARE/2,-SQUARE/2,SQUARE/2,roof-.3,roof),J.M.box(-6,6,-6,6,-9,20)-j15)<1e-6,
        same_as_J15_outside_socket_above_flange=diff((c&upper)-core,j15&upper)<1e-4 and diff((j15&upper)-core,c&upper)<1e-4,  # outside the socket
        stem_fits=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z0,roof),c)<1e-6,
        no_flat_overhang_in_socket=not J7.overhangs(c),
        flares_past_hole=FLARE_TIP-J.HOLE/2>=.8-1e-9,
        flat_on_bed=abs(c.bounding_box().min.Z-J.BOTTOM)<1e-6)
    path=STL/'joystick-j16.stl';J.export(Pos(0,0,-J.BOTTOM)*c,path)
    tilt=TILT.tilt({'J15':(j15,LIFT),'J16':(c,LIFT)})
    checks['clear_of_lid_at_rest']=not tilt['caps']['J16']['touches_at_rest']
    report=dict(checks=checks,passed=all(checks.values()),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),tilt=tilt)
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed'],sha256=report['sha256']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
