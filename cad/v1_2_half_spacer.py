"""V1.2: v1.1 with the USB-end spacer halved, 1.0 -> 0.5 mm (V1.2-SPACER).
Austin: v1.1 lid spacer is in the right place but too big; the screen board
no longer sits flush.
"""
import v1_1_spacer as W

if __name__=='__main__':
    W.configure('v1.2',.5)  # V1.2-SPACER
    W.main()
