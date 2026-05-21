# Raspberry Pi Robotic Arm Vision System

An OpenCV-powered computer vision system deployed on a Raspberry Pi to detect, classify, and sort **WHITE** and **GREY** cubes into designated drop zones using a 4+ DOF robotic arm.

---

## 📌 Project Overview

This project implements an overhead vision-guided robotic sorting system. Using a camera mounted above the workspace, the system identifies the color of incoming cubes, tracks unique face markings, and coordinates with a robotic arm to automate the sorting process.

### Features
* **Color Segmentation:** Dual-threshold detection optimized for distinguishing white and grey objects under varying light.
* **Marking Identification:** Recognizes 4 distinct face markings per cube (`X`, `Y`, `N`, `Chep`).
* **Automated Sorting:** Triggers robotic arm kinematics to move items from the Pick Zone to target drop zones. (WIP)

---

## 🛠️ Hardware Requirements

* **Compute Unit:** Raspberry Pi 
* **Vision:** USB Webcam OR Raspberry Pi Camera Module (V2 / HQ)
* **Actuation:** Robotic Arm with 4+ Degrees of Freedom (DOF)
* **Objects:** 
  * 1x WHITE cube (with X, Y, N, Chep face markings)
  * 1x GREY cube (with X, Y, N, Chep face markings)

---

## 📐 Workspace & Camera Layout

The overhead camera monitors a centralized pick zone, while the arm operates relative to a defined home position to route objects to the left or right.

```text
┌─────────────────────────────────────┐
│         CAMERA (overhead)           │
│                 │                   │
│    DROP-A     [ARM]    DROP-B       │
│   (white)     HOME     (grey)       │
│                                     │
│        ← PICK ZONE →                │
└─────────────────────────────────────┘
```
##   Output
<img width="790" height="627" alt="Output001" src="https://github.com/user-attachments/assets/6893012b-48d8-41d4-9df2-514c546a518b" />
