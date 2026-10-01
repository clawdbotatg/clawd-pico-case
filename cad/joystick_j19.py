"""J19: J18 continued shallower. Austin, 2026-09-30: "not even six [1.7] is
shallow enough". Hole depth 1.6 / 1.5 / 1.4 / 1.3 / 1.2, J17-B tabs, dice
dots 1-5. Below ~1.45 the straight grip under the 0.25 mouth chamfer is
short (1.2 depth: 0.95 of grip).
Row J19 in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j19.py
"""
import joystick_j18 as J18
ROOT=J18.ROOT
DEPTHS=[1.6,1.5,1.4,1.3,1.2]  # J19-DEPTH, dots 1..5

if __name__=='__main__':J18.main(DEPTHS,ROOT/'stl/v1.4/joystick-j19',ROOT/'renders/v1.4/joystick-j19','J19')
