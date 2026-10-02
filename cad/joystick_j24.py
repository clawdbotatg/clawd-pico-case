"""J24: J24-FIT-2's hole (Austin, 2026-10-02: the best; centre press clicks only
centre) with a bigger round flange, no tabs, to stop it ripping out.
Austin wants these tried first in the +0.3 lid he has (V1.9, the underwear
lid) before making the lid taller. Two caps, printed separately:
  A  10.0 disc, J22's thin edge: 0.4 inside r 3.4, 0.24 from the hole edge out
  B  10.0 disc, 0.4 full (stiffer against pull-out, but 0.16 closer to the lid)
Tilt check in PCB coordinates (Codex review item 4): the cap placed by its
measured seat, rotated about pivots we don't know (PCB to body top).
Rows J24-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j24.py
"""
import hashlib
import json
import math
from build123d import Pos, Axis
import joystick_test as J
import joystick_j4 as J4
import joystick_j13 as J13
import joystick_j20 as J20
import joystick_j22 as J22
import joystick_j24_fit as F
import v1_9_test as T9
M,V=T9.M,T9.V

ROOT=J.ROOT
STL=ROOT/'stl/test/j24'
OUT=ROOT/'renders/test/j24'
FLANGE_D=10.0              # J24-FLANGE: 1.0 past the 8.0 hole (J1-LID)
VARIANTS={'A':True,'B':False}  # thinned edge (J13-THIN) or full 0.4
SEAT=3.34                  # M1: J22 cap bottom above the PCB (derived)
SEATS=(3.22,3.46)          # M1 +-0.12
PIVOTS=(0.,1.5,2.8)        # PCB to the body top (J3-PHOTO); not measured
SPLIT=4.5                  # cap-local z inside the solid neck

def cap(thin=True,neck_add=0.):
    c=J22.cap()+(J20.cavity(J22.DEPTH)&J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # J22, socket filled
    c=c-(J.cylinder(14,J.BOTTOM-1,J.BOTTOM+J.FLANGE_T+.01)-J.cylinder(J.NECK,J.BOTTOM-2,J.BOTTOM+1))  # no flange, no tabs
    if neck_add:
        big=lambda z0,z1:M.box(-9,9,-9,9,z0,z1)
        c=(c&big(J.BOTTOM-1,SPLIT))+J.cylinder(J.NECK,SPLIT-.01,SPLIT+neck_add+.01)+Pos(0,0,neck_add)*(c&big(SPLIT,20))
    c=c+J.cylinder(FLANGE_D,J.BOTTOM,J.BOTTOM+J.FLANGE_T)
    if thin:c=c-J13.thin_cut()
    cav,_=F.cavity(*F.OPEN['2'])
    return c-cav

def sweep(c,lid,seats=SEATS,pivots=PIVOTS):
    """Smallest tilt that touches the lid, per seat / pivot / direction."""
    def vol(s):return sum(x.volume for x in s.solids())
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    local=lid & M.box(hx-9,hx+9,hy-9,hy+9,-5,30)
    def hits(seat,angle,az,pivot,dz=0.):
        ax=Axis((hx,hy,pivot),(math.cos(math.radians(az)),math.sin(math.radians(az)),0))
        return vol(Pos(0,0,dz)*(Pos(hx,hy,seat-J.BOTTOM)*c).rotate(ax,angle) & local)>1e-5
    out={}
    for s in seats:
        for pv in pivots:
            for az in range(0,360,45):
                lo,hi=0.,25.
                if hits(s,0,az,pv):out[f'{s}/{pv}/{az}']=0.;continue
                if not hits(s,hi,az,pv):out[f'{s}/{pv}/{az}']=25.;continue
                for _ in range(8):
                    mid=(lo+hi)/2
                    if hits(s,mid,az,pv):hi=mid
                    else:lo=mid
                out[f'{s}/{pv}/{az}']=round(lo,1)
    return out,hits

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    lid,_,_,under,_=T9.build()  # the V1.9 (+0.3, underwear) lid Austin has
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    joy_under=(lid & M.box(hx+4.3,hx+4.7,hy-.2,hy+.2,-5,30)).bounding_box().min.Z
    checks={};res={}
    j22=J22.cap()
    jt,_=sweep(j22,lid,seats=(SEAT,))
    for name,thin in VARIANTS.items():
        c=cap(thin);bb=c.bounding_box()
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_same_height_as_J22']=abs(bb.max.Z-j22.bounding_box().max.Z)<1e-6 and abs(bb.min.Z-J.BOTTOM)<1e-6
        checks[name+'_no_flat_overhang_in_socket']=not F.J7.overhangs(c)
        t,hits=sweep(c,lid)
        checks[name+'_clear_at_rest']=all(v>0 for v in t.values())
        edge_top=J.BOTTOM+(J13.EDGE_T if thin else J.FLANGE_T)-J.BOTTOM
        checks[name+'_caught_on_pull']=all(hits(s,0,0,0,joy_under-(s+edge_top)+.05) for s in SEATS)
        res[name]=dict(edge_thickness=round(edge_top,2),gap_at_seat=round(joy_under-(SEAT+edge_top),3),
                       min_tilt=min(t.values()),tilt=t)
        J.export(Pos(0,0,-J.BOTTOM)*c,STL/f'joystick-j24-{name}.stl')
        print(name,res[name]['gap_at_seat'],res[name]['min_tilt'],flush=True)
    report=dict(status='TEST, not current',lid='V1.9 (+0.3)',checks=checks,passed=all(checks.values()),
        j22_min_tilt_same_lid=min(jt.values()),j22_tilt=jt,caps=res,
        notes=['Estimated real tilt ~8 deg (J7), not measured; the sweep covers seats 3.22-3.46 and pivots 0-2.8.'],
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed'],j22=report['j22_min_tilt_same_lid'],
        caps={k:{kk:vv for kk,vv in v.items() if kk!='tilt'} for k,v in res.items()}),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
