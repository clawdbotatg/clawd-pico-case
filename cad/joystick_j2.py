"""J2: exact user-requested stepped socket; unchanged J1 outside.
Dimensions from MEASUREMENTS J2-SOCKET/J2-OUTER. Cap only; no case changes.
"""
import hashlib
import json
import math
from pathlib import Path
from build123d import Pos, Sphere, export_step
import joystick_test as J

ROOT=J.ROOT
STL=ROOT/'stl/joystick-j2'
OUT=ROOT/'renders/joystick-j2'
ROUND_D,ROUND_DEPTH,SQUARE_DEPTH=3.0,1.0,2.0  # J2-SOCKET

def cap():
    blank=J.cylinder(J.NECK,J.BOTTOM,J.BALL_Z)+J.cylinder(J.FLANGE,J.BOTTOM,J.BOTTOM+J.FLANGE_T)
    blank+=Pos(0,0,J.BALL_Z)*Sphere(J.BALL/2)
    circle=J.cylinder(ROUND_D,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+ROUND_DEPTH)
    half=J.SOCKET/2
    square=J.M.box(-half,half,-half,half,J.BOTTOM+ROUND_DEPTH-J.P.EPS,J.BOTTOM+ROUND_DEPTH+SQUARE_DEPTH)
    return blank-(circle+square),blank

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    shape,blank=cap();old=J.cap()
    expected=math.pi*(ROUND_D/2)**2*ROUND_DEPTH+J.SOCKET**2*SQUARE_DEPTH
    removed=blank.volume-shape.volume
    checks={
        'one_valid_solid':shape.is_valid and len(shape.solids())==1,
        'exact_requested_cavity_volume':abs(removed-expected)<1e-5,
        'no_added_external_material':sum(s.volume for s in (shape-old).solids())<1e-5,
        'exterior_bounds_unchanged':all(abs(a-b)<1e-5 for a,b in zip(tuple(shape.bounding_box().size),tuple(old.bounding_box().size))),
        'round_contains_square_corners':ROUND_D>J.SOCKET*math.sqrt(2),
    }
    # Cross-section probes distinguish round mouth from deeper square socket.
    for depth,area in ((.5,math.pi*(ROUND_D/2)**2),(1.5,J.SOCKET**2),(2.9,J.SOCKET**2)):
        slab=J.cylinder(J.NECK,J.BOTTOM+depth-.005,J.BOTTOM+depth+.005)
        actual=sum(s.volume for s in (slab-shape).solids())/.01
        checks['section_at_depth_'+str(depth)]=abs(actual-area)<1e-5
    roof_probe=J.M.box(-.5,.5,-.5,.5,J.BOTTOM+3.01,J.BOTTOM+3.02)
    checks['closed_roof']=abs((roof_probe-shape).volume)<1e-5
    assert all(checks.values()),checks
    printed=Pos(0,0,-J.BOTTOM)*shape
    path=STL/'joystick-j2-stepped-socket.stl';J.export(printed,path)
    export_step(printed,str(OUT/'joystick.step'))
    report=dict(checks=checks,cavity_volume_mm3=removed,round_diameter_mm=ROUND_D,round_depth_mm=ROUND_DEPTH,square_width_mm=J.SOCKET,square_depth_mm=SQUARE_DEPTH,total_depth_mm=ROUND_DEPTH+SQUARE_DEPTH,
                print_orientation='flange down, socket opening at bed',
                limitations=['3.00mm is user-specified trial, not guaranteed clearance against unconfirmed3.32mm reading.','Possible1.10mm extra seating is not a hardware-fit result.','No lid lowering or hole shift yet; test cap first.','Physical seating/motion and slicer settings unverified.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    sources=[Path(__file__),ROOT/'cad/joystick_test.py',ROOT/'cad/model.py',ROOT/'cad/params.py']
    outputs=[path,OUT/'joystick.step',OUT/'validation.json']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='joystick-j2',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')
    print(json.dumps(report,indent=2));print('STL SHA256',hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':main()
