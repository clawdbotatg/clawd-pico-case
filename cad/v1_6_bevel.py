"""V1.6: v1.5 with a print-friendly top edge. Printed face down, the 3 mm top
fillet starts flat at the bed and its first layers droop (Austin: a rough
line where the flat top meets the curve). A 45 deg band tangent to the
fillet fills in that flat start (material added under it). Everything else is v1.5. Rows V1.6-*.
Run: .venv/bin/python cad/v1_6_bevel.py
"""
import base64
import hashlib
import json
import math
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, export_step
import v1_5_tall as T5
R,W,V,T,S,M,P,J,L1=T5.R,T5.W,T5.V,T5.T,T5.S,T5.M,T5.P,T5.J,T5.L1
ROOT=T5.ROOT
REV='v1.6'
OUT=ROOT/'renders'/REV
STL=ROOT/'stl'/REV

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    W.shorten()
    v15,_=T5.lid()
    R.TOP_BEVEL=True
    l,_=T5.lid()
    b,*_=V.base();caps=T.buttons()
    placed=Pos(*M.JOY_C,L1.LIP_TOP+T5.J9_LIFT-J.BOTTOM-J.FLANGE_T)*T5.J9.cap()
    def vol(s):return sum(x.volume for x in s.solids())
    top=S.TOP+T5.RAISE;leg=R.TOP_R*(2-2**.5)
    checks={}
    def check(n,ok):checks[n]=bool(ok)
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    band=T5.everything(top-R.TOP_R-.01,top+1)-M.rbox(S.X0+R.TOP_R+.01,S.X1-R.TOP_R-.01,S.Y0+R.TOP_R+.01,S.Y1-R.TOP_R-.01,top-5,top+2,max(S.R-R.TOP_R,.5))
    added=l-v15
    check('only_fills_top_perimeter',vol(v15-l)<1e-5 and vol(added)>.5 and vol(added & band)>vol(added)-1e-4)
    check('same_height',abs(l.bounding_box().max.Z-v15.bounding_box().max.Z)<1e-6)
    # Face down, "down" is +z in model space: no outer face near the top
    # perimeter may face up more than 45 deg except the flat top itself.
    steep=[]
    for f in (l & band).faces():  # sample each face, not just its centre
        for u in (.02,.25,.5,.75,.98):
            for w in (.02,.25,.5,.75,.98):
                try:pt=f.position_at(u,w);n=f.normal_at(pt)
                except Exception:continue
                if abs(pt.Z-top)>1e-3 and n.Z>math.cos(math.radians(45))+1e-2:steep.append((round(pt.Z,2),round(n.Z,3)))
    check('outer_top_edge_max_45deg_overhang',not steep)
    check('fits_same_base',J.overlap(b,l-R.ribs())<1e-5)
    check('joystick_clear',J.overlap(placed,l)<1e-5)
    check('buttons_clear',J.overlap(caps,l)<1e-5)
    report=dict(revision=REV,checks=checks,passed=all(checks.values()),bevel_leg_mm=round(leg,3),steep_faces=steep,
        print=dict(orientation='face down',supports=False,raft=False,elephant_foot_compensation_mm=.15),
        notes=['v1.5 lid with a 45 deg tangent band at the top edge; nothing else changed.','Ask the slicer for 0.15 elephant-foot compensation.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(V.origin(Rot(180,0,0)*l),STL/'lid-face-down.stl')
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps;view['joystick_cap']=placed
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit=REV+' smooth top edge',case_mm=[round(S.X1-S.X0,2),round(S.Y1-S.Y0,2),round(top-M.Z_BOTTOM,2)],split_z=S.SEAM,assumptions=['v1.5 lid.','45 deg band starts the top curve (prints clean face down).','Base, J9, buttons unchanged.','No supports, no raft.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.6 · SMOOTH TOP EDGE').replace('V3 Case Review — Not Approved for Print','V1.6 smooth top edge')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_5_tall.py','v1_4_rounded.py','joystick_j9.py','v1_3_short_end.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision=REV,supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
