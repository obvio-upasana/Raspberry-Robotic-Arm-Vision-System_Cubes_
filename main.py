"""
=============================================================================
Raspberry Pi Robotic Arm Vision System
=============================================================================
Detects WHITE and GREY cubes via a USB/Pi camera using OpenCV, then
directs a robotic arm to sort them into two drop zones.
 
Hardware:
  - Raspberry Pi
  - USB webcam OR Raspberry Pi Camera Module (V2 / HQ)
  - Robotic arm with 4+ DOF 
  - Two cubes: one WHITE, one GREY-ish (each with 4 distinct face markings{ X, Y, N, Chep})
 
Camera / Workspace Layout (top view)(tentative):
  ┌─────────────────────────────────────┐
  │         CAMERA (overhead)           │
  │                 │                   │
  │    DROP-A    [ARM]    DROP-B         │
  │   (white)   HOME    (grey)          │
  │                                     │
  │        ← PICK ZONE →               │
  └─────────────────────────────────────┘
 
Required packages:
  >>>>>>>>>>>> pip install opencv-python numpy
 
Author:  <Upasana Singh>
Date:    2026-05-09
Version: 1.0.0
=============================================================================
"""
