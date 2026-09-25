"""J1 isolated fit experiment; does not modify or export the whole case.
All dimensions: MEASUREMENTS J1-CAP/J1-LID/J1-CHECK and D6-SOCKET.
Run: .venv/bin/python cad/joystick_test.py
"""
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import math
from build123d import Pos, Rot, Cylinder, Sphere, Axis, Compound, export_stl
import model as M
import params as P

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders/joystick-j1'
STL = ROOT / 'stl/joystick-j1'
BOTTOM, ROOF, NECK = 3.4, 5.3, 5.0  # J1-CAP / D6-SOCKET
SOCKET, FLANGE, FLANGE_T, BALL, BALL_Z = 2.01, 10.4, .4, 7., 8.5  # J1-CAP
HOLE, OUTER, UNDER, THICK = 8., 20., 4.4, .7  # J1-LID
FOOT_X, FOOT_W, FOOT_L = 9., 2., 6.  # J1-LID

def cylinder(d, z0, z1):
    return Pos(0, 0, (z0+z1)/2)*Cylinder(d/2, z1-z0)

def cap():
    shape = cylinder(NECK, BOTTOM, BALL_Z) + cylinder(FLANGE, BOTTOM, BOTTOM+FLANGE_T)
    shape += Pos(0,0,BALL_Z)*Sphere(BALL/2)
    return shape - M.box(-SOCKET/2, SOCKET/2, -SOCKET/2, SOCKET/2, BOTTOM-P.TOOL_EXT, ROOF)

def gauge():
    shape = cylinder(OUTER, UNDER, UNDER+THICK)
    for x in (-FOOT_X, FOOT_X):
        shape += M.box(x-FOOT_W/2,x+FOOT_W/2,-FOOT_L/2,FOOT_L/2,0,UNDER+THICK)
    return shape-cylinder(HOLE,-P.TOOL_EXT,UNDER+THICK+P.TOOL_EXT)

def export(shape, path):
    assert shape.is_valid
    export_stl(shape, str(path), tolerance=.02, angular_tolerance=.1)
    data=path.read_bytes(); records=[]; edges=Counter()
    for i in range(struct.unpack_from('<I',data,80)[0]):
        rec=data[84+50*i:134+50*i]; vals=struct.unpack('<12fH',rec)
        # Weld float32 seam noise at 0.00001 mm, far below mesh tolerance.
        vs=[tuple(round(v,5) for v in vals[j:j+3]) for j in (3,6,9)]
        if len(set(vs))<3: continue
        rec=struct.pack('<12fH',*vals[:3],*(v for vertex in vs for v in vertex),vals[-1])
        records.append(rec)
        for j in range(3): edges[tuple(sorted((vs[j],vs[(j+1)%3])))]+=1
    assert all(n==2 for n in edges.values()), str(path)
    path.write_bytes(data[:80]+struct.pack('<I',len(records))+b''.join(records))

def overlap(a,b):
    return sum(s.volume for s in (a & b).solids())

def main():
    OUT.mkdir(parents=True,exist_ok=True); STL.mkdir(parents=True,exist_ok=True)
    c,g=cap(),gauge()
    assert len(c.solids())==len(g.solids())==1
    assert overlap(c,g)<1e-6
    assert BALL < HOLE < FLANGE
    assert overlap(Pos(0,0,UNDER-(BOTTOM+FLANGE_T)+.1)*c,g)>0
    # Original lower interface is reconstructed independently, compared below lip.
    baseline=cylinder(NECK,BOTTOM,ROOF)-M.box(-SOCKET/2,SOCKET/2,-SOCKET/2,SOCKET/2,BOTTOM-1,ROOF)
    region=cylinder(NECK,BOTTOM,ROOF)
    assert abs((c & region).volume-baseline.volume)<1e-6
    # Keep all motion results, including failed hypotheses.
    checks=[]
    for pivot in (0.,3.):
        for angle in (0,5,10):
            for az in range(0,360,45):
                for press in (0.,.3):
                    axis=Axis((0,0,pivot),(math.cos(math.radians(az)),math.sin(math.radians(az)),0))
                    moved=Pos(0,0,-press)*c.rotate(axis,angle)
                    checks.append(dict(pivot=pivot,angle=angle,azimuth=az,press=press,lid_overlap_mm3=round(overlap(moved,g),6)))
    # Upright cap: flat flange down. Gauge inverted: flat lid top down, feet up.
    cp=Pos(0,0,-BOTTOM)*c
    gp=Rot(180,0,0)*g; gp=Pos(0,0,-gp.bounding_box().min.Z)*gp
    export(cp,STL/'joystick-cap.stl'); export(gp,STL/'lid-gauge.stl')
    plate=Compound(children=[cp,Pos((FLANGE+OUTER)/2+5,0,0)*gp])
    export(plate,STL/'two-part-test.stl')
    # Hardware context cropped from own measured-board proxy; never exported for print.
    jx,jy=M.JOY_C
    hardware=Pos(-jx,-jy,0)*M.hat()
    hardware=hardware & M.box(-P.L2/2,P.L2/2,-7,7,-P.L3,P.J6)
    parts=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,shape,color in [('hat',hardware,'#286778'),('lid',g,'#ddd6c5'),('joystick_cap',c,'#efa332')]:
            path=Path(tmp)/(name+'.stl'); export(shape,path); bb=shape.bounding_box()
            parts.append(dict(name=name,color=color,stl=base64.b64encode(path.read_bytes()).decode(),bbox=[bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z]))
    info=dict(commit='J1-fit-test',case_mm=[OUTER,OUTER,12],assumptions=[
        'FIT TEST ONLY — not sent to printer; review before slicing.',
        'Round hole 8 mm; ball 7 mm; captive lip 10.4 mm.',
        'Original 2.01 mm socket, roof5.3 and bottom3.4 preserved.',
        'Gauge top5.1: LOCAL surface3.05 mm above glass, not a full raised lid.',
        'Feet rest on bare PCB; hold gauge down by hand. Not a snap-fit lid.',
        'Actual joystick travel, metal-body height, printed fit and strength unverified.',
        f'{sum(x["lid_overlap_mm3"]>0 for x in checks)} sampled cap/gauge motion collisions; see validation.json.',
        'Print cap flange-down; gauge face-down. No supports or raft requested; slicing unverified.' ])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(parts)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';')
    html=html.replace("PARTS.find(p=>p.name==='base')","PARTS.find(p=>p.name==='lid')").replace("['base','lid']","['lid']").replace('dist=150','dist=70').replace('V3 Case Review — Not Approved for Print','J1 joystick fit test').replace('V3 review · NOT APPROVED FOR PRINT','J1 joystick · REVIEW BEFORE PRINT').replace('case ${','test ${')
    (OUT/'viewer.html').write_text(html)
    result=dict(static_cap_gauge_clear=True,mesh_closed=True,cap_hardware_static_overlap_mm3=overlap(c,hardware),gauge_hardware_static_overlap_mm3=overlap(g,hardware),motion=checks,limitations=['Hardware body height and pivot are guesses.','No slicer or physical tests yet.','Foot seating on actual PCB requires inspection.'])
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    manifest=dict(revision='joystick-j1',submitted=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'cad/model.py',ROOT/'cad/params.py',ROOT/'cad/viewer_template.html']},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*STL.glob('*.stl'),OUT/'viewer.html',OUT/'validation.json']})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='motion'},indent=2))
    print('motion collisions',sum(x['lid_overlap_mm3']>0 for x in checks),'/',len(checks))

if __name__=='__main__': main()
