"""V1.8 TEST (not current): v1.7 lid with more room under it for the joystick
flange, plus two caps with a stronger flange.
Austin, 2026-10-01: J22 sometimes double-clicks on diagonal pushes (the tab
behind the push rises into the lid), and a hard pull takes the cap out (the
tabs barely hold). The flange needs to be bigger, so the lid needs more room.
Lids: v1.7 stretched 0.3 / 0.5 taller in the same prismatic band as V1.5
(z 1.0 above the LCD PCB front): everything that holds the board, the seam,
catches and pocket stay; roof, window and openings rise. Base unchanged, so
the 24 printed v1.7 bases fit.
Caps (J23, dice dots): 1 = J22 with tabs 2.0x J16 (was 1.55x), 0.24 thick;
2 = same tabs at full 0.4 thickness (stiffer against pull-out).
Rows V1.8-* in MEASUREMENTS. Run: .venv/bin/python cad/v1_8_test.py
Outputs go to stl/test/v1.8/, never stl/current.
"""
import hashlib
import itertools
import json
from build123d import Pos, Rot, Compound
import v1_7_lock as L7
import v1_5_tall as T5
import joystick_test as J
import joystick_j4 as J4
import joystick_j8 as J8
import joystick_j15 as J15
import joystick_j16 as J16
import joystick_j17 as J17
import joystick_j20 as J20
import joystick_j22 as J22
import j10_tilt as TILT
V,M,S=T5.V,T5.M,T5.S

ROOT=T5.ROOT
STL=ROOT/'stl/test/v1.8'
OUT=ROOT/'renders/test/v1.8'
RAISES={'0.3':.3,'0.5':.5}  # V1.8-RAISE (test pair)
TAB_SCALE=2.0               # V1.8-TAB
CAPS={'1':.24,'2':J.FLANGE_T}  # V1.8-TAB: tab thickness past the hole edge


def lid(raise_):
    l,_=L7.lid()
    return T5.stretch(l,T5.STRETCH_Z,raise_),l

def cap(t,n):
    w,tip=J17.tab(TAB_SCALE)
    c=J15.cap()+(J8.cavity(J20.SQUARE,J16.LIFT) & J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))
    fl=None
    for f in J16.flares(w,tip):fl=f if fl is None else fl+f
    if t<J.FLANGE_T:fl-=J16.thin(t)
    c=c+fl-J20.cavity(J22.DEPTH)
    for p in J17.pips(n):c-=p
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    L7.W.shorten()
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};lids={};caps={}
    l17,_=L7.lid()
    sec=lambda shape,z:vol(shape & M.box(S.X0-5,S.X1+5,S.Y0-5,S.Y1+5,z-.005,z+.005))
    checks['band_prismatic']=abs(sec(l17,.3)-sec(l17,1.1))<1e-3
    for name,r in RAISES.items():
        l,_=lid(r)
        checks['lid_'+name+'_valid_single_solid']=l.is_valid and len(l.solids())==1
        checks['lid_'+name+'_taller_by_'+name]=abs(l.bounding_box().size.Z-l17.bounding_box().size.Z-r)<1e-4
        below=M.box(S.X0-5,S.X1+5,S.Y0-5,S.Y1+5,-100,T5.STRETCH_Z-.01)
        checks['lid_'+name+'_board_hold_unchanged']=vol((l&below)-(l17&below))<1e-3 and vol((l17&below)-(l&below))<1e-3
        lids[name]=l
        J.export(V.origin(Rot(180,0,0)*l),STL/('lid-'+name+'-taller-face-down.stl'))
    j22=J22.cap()
    for name,t in CAPS.items():
        c=cap(t,int(name))
        checks['cap_'+name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks['cap_'+name+'_tabs_bigger_than_J22']=J17.tab(TAB_SCALE)[1]>J17.tab(J20.TAB_SCALE)[1]
        caps['J23-'+name]=(c,J16.LIFT)
        J.export(Pos(0,0,-J.BOTTOM)*c,STL/('joystick-j23-'+name+'.stl'))
    tilt={}
    for name,l in [('v1.7',l17),*lids.items()]:
        tilt[name]=TILT.tilt({'J22':(j22,J16.LIFT),**caps},l)['caps']
        for cn in caps:
            if name!='v1.7':checks[cn+'_clear_of_lid_'+name+'_at_rest']=not tilt[name][cn]['touches_at_rest']
    # one plate: two lids face down, two caps flange down
    parts=[V.origin(Rot(180,0,0)*lids[n]) for n in RAISES]
    lb=parts[0].bounding_box().size;GAP=8.
    placed=[parts[0],Pos(lb.X+GAP,0,0)*parts[1]]
    for i,n in enumerate(CAPS):
        c=Pos(0,0,-J.BOTTOM)*caps['J23-'+n][0];r=J17.tab(TAB_SCALE)[1]
        placed.append(Pos(2*lb.X+2*GAP+r,r+i*(2*r+GAP),0)*c)
    checks['plate_separate']=all(J.overlap(a,b)<1e-6 for a,b in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'v1.8-test-plate.stl')
    summ={l:{c:(lambda a:dict(push=min(a[f'p3_az{z}'] for z in (0,90,180,270)),diagonal=min(a[f'p3_az{z}'] for z in (45,135,225,315))))(v['angles']) for c,v in caps_.items()} for l,caps_ in tilt.items()}
    report=dict(status='TEST, not current',checks=checks,passed=all(checks.values()),raises=RAISES,tab_scale=TAB_SCALE,caps=CAPS,tilt_summary=summ,
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed'],tilt=summ),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
