# An Object-Centered Data Acquisition Method for 3D Gaussian Splatting using Mobile Phone

---

## 🔎 Overview
This repository accompanies a method for mobile, object-centered multiview data acquisition tailored to 3D Gaussian Splatting (3DGS). The workflow establishes an object-centered spherical coordinate framework for capture on smartphones. After a one-time calibration, device orientations are aligned to a baseline reference and the camera forward direction is mapped to a discretized spherical grid for viewpoint indexing. To counter polar sampling bias, area-weighted spherical coverage is computed in real time to guide motion. A stability gate, based on smoothed inertial measurements, admits only steady-motion frames. The collected images and poses are intended for off-device 3DGS reconstruction.

---

## 🧭 Key Contributions
- Mapping mobile IMU-based orientations to an object-centered spherical coordinate system.  
- Real-time, area-weighted spherical coverage feedback that encourages angular uniformity and completeness.  
- A dual-mode stability gate using smoothed linear acceleration and angular velocity so that only steady frames are recorded.

---

## 🧩 System Outline
- **Calibration.** Record a baseline device orientation once; subsequent orientations are referenced relatively to ensure consistency across trials.  
- **Pose sensing.** During capture, the device logs orientation (quaternion), linear acceleration, and angular velocity.  
- **Stability gating.** Exponential moving averages of the acceleration and angular velocity magnitudes are compared with thresholds over a holding window; frames outside steady conditions are discarded.  
- **Spherical mapping.** The camera’s forward direction is projected onto a longitude–latitude grid; normalized angles are quantized to grid indices for online coverage bookkeeping.  
- **Area-weighted coverage.** Coverage accumulation uses spherical surface-area weighting to avoid overestimation near the poles; morphological refinements (adaptive pole dilation and hole filling) improve local consistency without altering the area-weighted measure.

---

## 🧪 Experimental Setting (brief)
Mobile capture was conducted on a **Redmi K70 Pro** with angle logging and stability gating enabled. Off-device reconstruction employed **3D Gaussian Splatting (3DGS)** on a workstation equipped with an **NVIDIA RTX 5090D**. Evaluation used a tabletop object for analysis and visualization.

---

## 🎬 Demo & Showcase

### 📱 Capture (phone screen recording)
<video controls playsinline width="720"
  src="https://ghproxy.net/https://github.com/zyz-nwpu/An-Object-Centered-Data-Acquisition-Method-for-3D-Gaussian-Splatting-using-Mobile-Phone/releases/download/v1/capturing.mp4">
</video>

### 🧱 Reconstruction result
<video controls playsinline width="720"
  src="https://ghproxy.net/https://github.com/zyz-nwpu/An-Object-Centered-Data-Acquisition-Method-for-3D-Gaussian-Splatting-using-Mobile-Phone/releases/download/v1/reconstruction_result.mp4">
</video>


