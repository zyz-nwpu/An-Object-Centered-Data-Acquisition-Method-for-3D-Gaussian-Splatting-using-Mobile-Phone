# An Object-Centered Data Acquisition Method for 3D Gaussian Splatting using Mobile Phone

**Project page:** https://zyz-nwpu.github.io/3dgs-oc-capture/  
**Authors:** Yuezhe Zhang, Luqian Bai, Mengting Yu, Lei Wei, Shuai Wan  
**Affiliations:** Northwestern Polytechnical University; Xi’an International University  
**Contact:** yuezhezhang@mail.nwpu.edu.cn

## Overview
This repository accompanies the work “An Object-Centered Data Acquisition Method for 3D Gaussian Splatting using Mobile Phone.”  
The method enables object-centered, multi-view data capture on mobile devices. After a one-time calibration, device orientations are aligned to a baseline frame and mapped to an object-centered spherical grid. Real-time, area-weighted coverage feedback and stability-gated frame selection guide uniform viewpoint acquisition for off-device 3D Gaussian Splatting (3DGS) reconstruction.

## Key Contributions
- Mapping mobile IMU orientations to an object-centered spherical coordinate system.  
- Real-time feedback of area-weighted spherical coverage to improve angular uniformity and completeness.  
- A dual-mode stability gate based on smoothed linear acceleration and angular velocity so that only steady frames are used.

## System Outline
- **Calibration:** record a baseline orientation once and express subsequent orientations as relative rotations.  
- **Guided capture:** project the camera forward axis to a discretized spherical grid and update coverage online.  
- **Stability gating:** accept frames only under steady motion based on thresholds over smoothed IMU signals.  
- **Export:** captured images and poses are used for off-device 3DGS training.

## Results (summary)
In user studies, guided capture achieved 100% spherical coverage with a comparable or smaller number of images, and improved PSNR relative to unguided capture (e.g., +0.92 dB at 7k and +2.587 dB at 30k training steps). Using identical images and training settings, replacing COLMAP rotations with calibrated device orientations yielded additional PSNR gains (about +0.25 dB at 7k and +0.24 dB at 30k).

## Repository
- `docs/` — materials for the project page and demo (to be expanded).
- This README.

## Citation
If you find this work useful, please cite:
