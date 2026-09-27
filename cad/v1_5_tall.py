"""V1.5: v1.4 (ribbed lid, J9 joystick) with the lid 0.5 mm taller inside, so
the joystick flange can tip without the roof pushing it into a centre click.
The lid is stretched at z STRETCH_Z, inside a band where its section is a
plain prism (0.2-1.2 above the LCD PCB front). Everything that holds the
board (below) stays; roof, window bezel, joystick and button openings (above)
rise together. Button caps get a 0.5 thicker flange so they sit the same.
Base unchanged. Rows V1.5-* in MEASUREMENTS.
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, export_step, fillet
import v1_4_rounded as R
import joystick_j9 as J9
W,V,T,S,M,P,J,L1=R.W,R.V,R.T,R.S,R.M,R.P,R.J,R.L1
L4=V.L4
ROOT=R.ROOT
REV='v1.5'
OUT=ROOT/'renders'/REV
STL=ROOT/'stl'/REV
RAISE=.5  # V1.5-RAISE
STRETCH_Z=1.0  # V1.5-STRETCH: prismatic band 0.2..1.2, checked below
J9_LIFT=.3  # J9 rides 0.3 higher on the stick (J5-LIFT)

def everything(z0,z1):
    return M.box(S.X0-5,S.X1+5,S.Y0-5,S.Y1+5,z0,z1)

def stretch(shape,z,dz,band=None):
    """Insert dz at height z by repeating the prismatic slab just below z."""
    lo,hi=-100,100
    below=shape & everything(lo,z)
    slab=shape & everything(z-dz,z) if band is None else band
    above=shape & everything(z,hi)
    out=below+Pos(0,0,dz)*slab+Pos(0,0,dz)*above
    return out

JOY_EDGE_R=.6  # V1.5-JOY-EDGE: round the joystick hole top edge; the J9 ball grazed it at 10 deg

def lid():
    l,_=R.lid()
    t=stretch(l,STRETCH_Z,RAISE)
    top=max((f for f in t.faces() if abs(f.center().Z-S.TOP-RAISE)<1e-6 and f.normal_at().Z>.9),key=lambda f:f.area)
    hx,hy=M.JOY_C[0]+L4.DX,M.JOY_C[1]+L4.DY+V.JOY_DY
    hole=min(top.inner_wires(),key=lambda w:(w.bounding_box().center().X-hx)**2+(w.bounding_box().center().Y-hy)**2)
    return fillet(hole.edges(),JOY_EDGE_R),l

def button(c):
    # Thicker flange: repeat the flange section up by RAISE; the post rises.
    z=P.B5+T.V.BUTTON_FLANGE_T  # s2 buttons: v3_fit flange thickness
    return stretch(c,z,RAISE)

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    W.shorten()
    tall,old=lid();b,*_=V.base()
    caps=Compound(children=[button(c) for c in T.buttons().solids()]);oldcaps=T.buttons()
    j9=J9.cap();placed=Pos(*M.JOY_C,L1.LIP_TOP+J9_LIFT-J.BOTTOM-J.FLANGE_T)*j9
    def vol(s):return sum(x.volume for x in s.solids())
    def same(a,c):return vol(a-c)<1e-4 and vol(c-a)<1e-4
    checks={}
    def check(n,ok):checks[n]=bool(ok)
    lo,hi=everything(-100,STRETCH_Z),everything(STRETCH_Z+RAISE,100)
    prism=lambda z:old & everything(z,z+.25)
    check('stretch_band_is_prismatic',same(prism(.3),Pos(0,0,-.5)*prism(.8)))
    check('lid_valid_single_solid',tall.is_valid and len(tall.solids())==1)
    check('lid_0_5_taller',abs(tall.bounding_box().max.Z-old.bounding_box().max.Z-RAISE)<1e-6)
    check('lid_below_stretch_unchanged',same(tall & lo,old & lo))
    unrounded=stretch(old,STRETCH_Z,RAISE)
    check('lid_above_stretch_raised_intact',same(unrounded & hi,Pos(0,0,RAISE)*(old & everything(STRETCH_Z,100))))
    check('joystick_edge_rounding_only_removes',vol(tall-unrounded)<1e-5 and 0<vol(unrounded-tall)<5)
    check('fits_same_base',J.overlap(b,tall-R.ribs())<1e-5)
    check('ribs_still_grip',J.overlap(b,R.ribs())>1)
    check('catches_hold',J.overlap(b,Pos(0,0,T.FREE_PLAY+.02)*tall)>1e-5)
    check('hardware_clear_at_board_hold_down',J.overlap(tall & everything(-100,STRETCH_Z),Pos(0,M.IY1-P.L1-.02,0)*M.hat())<1e-5)
    # Joystick: J9 at its real seat, tilted as J1-CHECK; the whole point.
    x,y=M.JOY_C;worst=0
    for pz in (0,3):
        for tilt in (5,8,10):
            for a in range(0,360,45):
                worst=max(worst,J.overlap(Pos(x,y,pz)*Rot(0,0,a)*Rot(tilt,0,0)*Rot(0,0,-a)*Pos(-x,-y,-pz)*placed,tall))
    check('joystick_tilts_10deg_clear_of_roof',worst<1e-5)
    check('joystick_clear_at_rest',J.overlap(placed,tall)<1e-5)
    check('joystick_retained_on_pull',J.overlap(Pos(0,0,L1.UNDER+RAISE-L1.LIP_TOP-J9_LIFT+.1)*placed,tall)>1e-5)
    # Buttons: same protrusion and retention as v1.4.
    check('buttons_valid',all(c.is_valid for c in caps.solids()) and len(caps.solids())==4)
    check('buttons_0_5_taller',abs(caps.bounding_box().max.Z-oldcaps.bounding_box().max.Z-RAISE)<1e-6)
    check('buttons_clear_lid',J.overlap(caps,tall)<1e-5)
    for i,c in enumerate(caps.solids()):check('button_retained_'+str(i),J.overlap(Pos(0,0,.25)*c,tall)>1e-5)
    for i in range(0,9,2):check('button_travel_'+str(i),J.overlap(Pos(0,0,-P.B6*i/8)*caps,tall)<1e-5)
    report=dict(revision=REV,checks=checks,passed=all(checks.values()),raise_mm=RAISE,stretch_z=STRETCH_Z,joystick='J9 unchanged',worst_tilt_contact_mm3=round(worst,4),
        case_mm=[S.X1-S.X0,S.Y1-S.Y0,S.TOP+RAISE-M.Z_BOTTOM],physical_fit_confirmed=False,
        notes=['Lid 0.5 taller inside above the board hold-down; base unchanged.','New button caps (flange +0.5) must be used with this lid.','Joystick sits 0.5 lower relative to the lid top.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(V.origin(Rot(180,0,0)*tall),STL/'lid-face-down.stl')
    J.export(V.origin(list(caps.solids())[0]),STL/'button.stl')
    J.export(Pos(0,0,-J.BOTTOM)*j9,STL/'joystick-j9.stl')
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=tall;view['button_caps']=caps;view['joystick_cap']=placed
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit=REV+' taller lid',case_mm=[round(v,2) for v in report['case_mm']],split_z=S.SEAM,assumptions=['v1.4 lid + ribs, 0.5mm taller inside.','Joystick J9 has room to tip.','Buttons: flange 0.5mm thicker.','Joystick hole top edge rounded 0.6mm.','Base unchanged. Not printed.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.5 · TALLER LID').replace('V3 Case Review — Not Approved for Print','V1.5 taller lid')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_4_rounded.py','joystick_j9.py','joystick_j8.py','joystick_j7.py','v1_3_short_end.py','v1_production.py','s2_tight_base.py','s1_strong_shell.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision=REV,supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
