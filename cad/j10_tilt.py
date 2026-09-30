"""How far each joystick cap tips before it touches the v1.7 lid (J10 vs J9).
The cap sits centred under the lid's joystick hole (the hole was moved to the
real stem by fit, L3/L4/V1-JOY), at the v1.7 height. Pivots 0 and 3 in the
cap frame and the 10 deg reference follow J1-CHECK; the true tilt (J7) and
the cap's true seating height (J3-LIP) are not measured, so read the angles
as a comparison between caps, not as a promise.
Run: .venv/bin/python cad/j10_tilt.py  (writes renders/v1.4/joystick-j10/tilt.json)
"""
import json
import math
from build123d import Pos, Axis
import v1_7_lock as L7
import joystick_j9 as J9
import joystick_j10 as X
M,J,L1,V,T5=L7.M,L7.J,L7.L1,L7.V,L7.T5

def tilt(caps):
    """caps: {name: (cap, lift)} -> per-cap contact angles (also used by J11)."""
    L7.W.shorten()
    lid,_=L7.lid()
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    local=lid & M.box(hx-9,hx+9,hy-9,hy+9,-5,20)
    out={}
    for name,(c,lift) in caps.items():
        dz=L1.LIP_TOP+lift-J.BOTTOM-J.FLANGE_T
        def touches(angle,az,pivot):
            axis=Axis((0,0,pivot),(math.cos(math.radians(az)),math.sin(math.radians(az)),0))
            return J.overlap(Pos(hx,hy,dz)*c.rotate(axis,angle),local)>1e-5
        rest=touches(0,0,0)
        res={}
        for pivot in (0.,3.):
            for az in range(0,360,45):
                lo,hi=0.,25.
                if not touches(hi,az,pivot):res[f'p{pivot:g}_az{az}']='>25';continue
                for _ in range(9):
                    mid=(lo+hi)/2
                    if touches(mid,az,pivot):hi=mid
                    else:lo=mid
                res[f'p{pivot:g}_az{az}']=round(lo,1)
        num=[a for a in res.values() if a!='>25']
        cardinal=[res[f'p{p:g}_az{a}'] for p in (0.,3.) for a in (0,90,180,270)]
        out[name]=dict(touches_at_rest=rest,worst_any=min(num) if num else '>25',
            worst_push=min(a for a in cardinal if a!='>25') if any(a!='>25' for a in cardinal) else '>25',angles=res)
        print(name,out[name]['worst_push'],out[name]['worst_any'],flush=True)
    return dict(note=__doc__.strip().splitlines()[0],hole_centre=[hx,hy],caps=out)

def main():
    caps={'J9':(J9.cap(),.3)}
    for n,v in X.VARIANTS.items():caps[n]=(X.cap(v['tabs'],v['lift'],n),v['lift'])
    (X.OUT/'tilt.json').write_text(json.dumps(tilt(caps),indent=2)+'\n')

if __name__=='__main__':main()
