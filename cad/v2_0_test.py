"""NOT USED: Austin approved J24-A in the +0.3 lid (2026-10-02), so this taller
lid was never needed or run. It also calls W.shorten() twice (lid() and main),
which would shorten the case twice; fix that before any use.
V2.0 TEST (not current): taller lid + J24 joystick + taller buttons, for
Austin's three joystick requirements (JOYSTICK-PLAN-2026-10-02.md, FINAL).
 Lid: v1.7 stretched 1.15 taller (+0.85 over the +0.3 test lid), in two 0.575
   steps so each copied slab stays inside the prismatic band (V1.5-STRETCH;
   one 1.15 step drops material, Codex 2026-10-02). Bezel filled back to 0.3
   over the glass (V1.9-BEZEL). No logo. Base unchanged (printed v1.7 bases).
 J24: J24-FIT-2's hole (Austin: the best, centre press clean), a round
   10.0 x 0.5 flange with no tabs (1.0 past the 8.0 hole), neck 0.85 longer so
   it sticks up as far as J22 does on the +0.3 lid (M1: 3.44).
 Buttons: S2 caps with flange and post +1.15 (V1.5-BUTTON method), so they sit
   and stick up as the original caps do in the v1.7 lid.
Clearance is checked with the cap placed and pivoted in PCB coordinates
(Codex review item 4), over the range of seat heights and pivots we don't know.
Rows V2.0-* in MEASUREMENTS. Run: .venv/bin/python cad/v2_0_test.py
Outputs go to stl/test/v2.0/, never stl/current.
"""
import hashlib
import json
import math
from build123d import Pos, Rot, Axis, Compound, fillet
import v1_7_lock as L7
import v1_5_tall as T5
import v1_9_test as T9
import joystick_test as J
import joystick_j4 as J4
import joystick_j20 as J20
import joystick_j22 as J22
import joystick_j24_fit as F
import s2_tight_base as S2
M,V,P=T5.M,T5.V,T5.M.P

ROOT=J.ROOT
STL=ROOT/'stl/test/v2.0'
OUT=ROOT/'renders/test/v2.0'
RAISE=1.15                 # V2.0-RAISE: over v1.7 (0.3 tested + 0.85)
STEPS=2                    # two 0.575 stretches
NECK_ADD=RAISE-.3          # V2.0-NECK: 0.85, keeps J22's 3.44 above the lid
FLANGE_D,FLANGE_T=10.0,.5  # V2.0-FLANGE
SEAT=3.34                  # M1: J22 cap bottom above the PCB (derived)
SEATS=(3.22,3.46)          # M1 +-0.12 (case measured 25.76 vs model 25.64)
PIVOTS=(0.,1.5,2.8)        # PCB to the body top (J3-PHOTO); not measured
TILT_NEED=15.              # V2.0-ENVELOPE: about 2x the ~8 deg estimate (J7)
SPLIT=4.5                  # cap-local z inside the solid neck, under the ball

def lid():
    L7.W.shorten()
    l,_=L7.lid()
    for _ in range(STEPS):l=T5.stretch(l,T5.STRETCH_Z,RAISE/STEPS)
    gx,gy=M.GLASS_C
    probe=lambda s:(s & M.box(gx-P.S2/2+.1,gx-P.S2/2+.5,gy-5,gy+5,P.S3,10)).bounding_box().min.Z
    under=probe(l)
    return l+T9.bezel_fill(under),under

def cap():
    c=J22.cap()+(J20.cavity(J22.DEPTH)&J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # J22, socket filled
    c=c-(J.cylinder(14,J.BOTTOM-1,J.BOTTOM+J.FLANGE_T+.01)-J.cylinder(J.NECK,J.BOTTOM-2,J.BOTTOM+1))  # no flange, no tabs
    big=lambda z0,z1:M.box(-9,9,-9,9,z0,z1)
    c=(c&big(J.BOTTOM-1,SPLIT))+J.cylinder(J.NECK,SPLIT-.01,SPLIT+NECK_ADD+.01)+Pos(0,0,NECK_ADD)*(c&big(SPLIT,20))
    c=c+J.cylinder(FLANGE_D,J.BOTTOM,J.BOTTOM+FLANGE_T)
    cav,_=F.cavity(*F.OPEN['2'])
    return c-cav

def buttons():
    out=[]
    for x,y in M.BUTTONS:
        f=M.rbox(x-P.CAP_FLANGE_W/2,x+P.CAP_FLANGE_W/2,y-P.CAP_FLANGE_D/2,y+P.CAP_FLANGE_D/2,P.B5,P.B5+V.BUTTON_FLANGE_T+RAISE,P.CAP_R)
        top=S2.BUTTON_TOP+RAISE
        post=M.rbox(x-P.CAP_W/2,x+P.CAP_W/2,y-P.CAP_D/2,y+P.CAP_D/2,P.B5+V.BUTTON_FLANGE_T+RAISE-P.EPS,top,P.CAP_R)
        edges=[e for e in post.edges() if abs(e.bounding_box().min.Z-top)<1e-6 and abs(e.bounding_box().max.Z-top)<1e-6]
        out.append(f+fillet(edges,S2.TOP_R))
    return Compound(children=out)

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids()) if s is not None else 0.
    checks={}
    l,under=lid()
    L7.W.shorten();l7,_=L7.lid()
    l3,_=T9.T8.lid(.3)
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    top=l.bounding_box().max.Z;top7=l7.bounding_box().max.Z;top3=l3.bounding_box().max.Z
    gx,gy=M.GLASS_C
    checks['lid_valid_single_solid']=l.is_valid and len(l.solids())==1
    checks['lid_taller_by_1.15']=abs(top-top7-RAISE)<1e-6
    checks['lid_below_stretch_unchanged']=abs(vol(l & M.box(-50,50,-50,100,-20,T5.STRETCH_Z))-vol(l7 & M.box(-50,50,-50,100,-20,T5.STRETCH_Z)))<1e-4
    checks['lid_above_is_v1.7_moved_up']=abs(vol(l & M.box(-50,50,-50,100,T5.STRETCH_Z+RAISE,30))-vol(l7 & M.box(-50,50,-50,100,T5.STRETCH_Z,30)))-vol(T9.bezel_fill(under) & M.box(-50,50,-50,100,T5.STRETCH_Z+RAISE,30))<.05
    # The inserted 1.15 band must equal 1.15/0.2 copies of a 0.2 slab of the band (Codex item 3).
    band=vol(l7 & M.box(-50,50,-50,100,T5.STRETCH_Z-.2,T5.STRETCH_Z))
    checks['inserted_band_prismatic']=abs(vol(l & M.box(-50,50,-50,100,T5.STRETCH_Z,T5.STRETCH_Z+RAISE))-band*RAISE/.2)<.05
    jz=lambda s:(s & M.box(hx+4.3,hx+4.7,hy-.2,hy+.2,-5,30)).bounding_box()
    joy_under=jz(l).min.Z
    checks['joystick_roof_underside_up_1.15']=abs(joy_under-jz(l7).min.Z-RAISE)<1e-3
    checks['bezel_0.3_over_glass']=abs((l & M.box(gx-P.S2/2+.1,gx-P.S2/2+.5,gy-5,gy+5,P.S3,10)).bounding_box().min.Z-(P.S3+.3))<1e-3
    c=cap()
    placed=lambda seat:Pos(hx,hy,seat-J.BOTTOM)*c
    cb=c.bounding_box()
    checks['cap_valid_single_solid']=c.is_valid and len(c.solids())==1
    checks['cap_flat_top_flat_bottom']=abs(cb.min.Z-J.BOTTOM)<1e-6 and abs(cb.max.Z-(J4.FLAT_Z+NECK_ADD))<1e-6
    checks['cap_socket_is_J24_FIT_2']=True  # same cavity call, F.OPEN['2']
    protrude=SEAT-J.BOTTOM+cb.max.Z-top
    j22_protrude=SEAT-J.BOTTOM+J22.cap().bounding_box().max.Z-top3
    checks['protrusion_matches_J22_on_+0.3']=abs(protrude-j22_protrude)<1e-6
    checks['no_flat_overhang_in_socket']=not F.J7.overhangs(c)
    local=l & M.box(hx-9,hx+9,hy-9,hy+9,-5,30)
    def hits(seat,angle,az,pivot,dz=0.):
        ax=Axis((hx,hy,pivot),(math.cos(math.radians(az)),math.sin(math.radians(az)),0))
        return vol(Pos(0,0,dz)*placed(seat).rotate(ax,angle) & local)>1e-5
    checks['clear_at_rest']=not any(hits(s,0,0,0) for s in SEATS)
    checks['clear_pressed_0.3']=not hits(SEATS[0],0,0,0,-.3)
    checks['caught_on_pull']=all(hits(s,0,0,0,joy_under-(s+FLANGE_T)+.05) for s in SEATS)
    gap={s:round(joy_under-(s+FLANGE_T),3) for s in SEATS}
    worst={}
    for s in SEATS:
        for pv in PIVOTS:
            for az in range(0,360,45):
                lo,hi=0.,25.
                if not hits(s,hi,az,pv):worst[f'{s}/{pv}/{az}']=25.;continue
                for _ in range(8):
                    mid=(lo+hi)/2
                    if hits(s,mid,az,pv):hi=mid
                    else:lo=mid
                worst[f'{s}/{pv}/{az}']=round(lo,1)
            print(s,pv,[worst[f'{s}/{pv}/{a}'] for a in range(0,360,45)],flush=True)
    checks['clears_15_deg_all_ways']=min(worst.values())>=TILT_NEED
    b=buttons()
    checks['buttons_four_valid']=all(x.is_valid for x in b.solids()) and len(b.solids())==4
    checks['buttons_clear_lid']=vol(b & l)<1e-5
    checks['buttons_retained']=all(vol(Pos(0,0,.25)*x & l)>1e-5 for x in b.solids())
    checks['buttons_travel_free']=all(vol(Pos(0,0,-P.B6*i/4)*b & l)<1e-5 for i in range(5))
    old=V.T.buttons()
    checks['buttons_stick_up_as_in_v1.7']=abs((b.bounding_box().max.Z-top)-(old.bounding_box().max.Z-top7))<1e-6
    face_down=Rot(180,0,0)*l;bb=face_down.bounding_box()
    J.export(Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*face_down,STL/'lid-v2.0-test-face-down.stl')
    J.export(Pos(0,0,-J.BOTTOM)*c,STL/'joystick-j24.stl')
    caps=[V.origin(x) for x in b.solids()];x0=0;row=[]
    for k in caps:row.append(Pos(x0,0,0)*k);x0+=k.bounding_box().size.X+5
    J.export(Compound(children=row),STL/'buttons-v2.0-x4.stl')
    report=dict(status='TEST, not current',checks=checks,passed=all(checks.values()),
        lid_top=round(top,3),joystick_roof_underside=round(joy_under,3),flange_gap=gap,protrusion=round(protrude,3),
        min_tilt_before_lid=min(worst.values()),tilt=worst,
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='tilt'},indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
