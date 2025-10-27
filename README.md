# An Object-Centered Data Acquisition Method for 3D Gaussian Splatting using Mobile Phone

> Mobile, object-centered multi-view capture with on-device guidance and native sensor signals for off-device 3D Gaussian Splatting (3DGS) reconstruction. :contentReference[oaicite:0]{index=0}

---

## 🔎 Overview
This repository accompanies the method that establishes an **object-centered spherical coordinate framework** for mobile capture. After a **one-time calibration**, device orientations are aligned to a baseline frame to obtain relative poses, and the camera optical axis is mapped to a **discretized spherical grid** for viewpoint indexing. To mitigate polar sampling bias, **area-weighted spherical coverage** is computed in real time to guide motion; a **stability gate** ensures only steady-motion frames are used. :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

---

## 🧭 Key Contributions
- Mapping mobile IMU-based orientations to an **object-centered spherical coordinate system**. :contentReference[oaicite:4]{index=4}  
- **Real-time area-weighted** spherical coverage feedback to improve angular **uniformity** and **completeness**. :contentReference[oaicite:5]{index=5}  
- A **dual-mode stability gate** using smoothed linear acceleration and angular velocity so that only **steady** frames are accepted. :contentReference[oaicite:6]{index=6}

---

## 🧩 System Outline
- **Calibration.** Record a baseline orientation \(R_0\); subsequent orientations are used as **relative rotations** \(R_{\text{rel}}(t)=R_0^\top R(t)\) for consistent reference across trials. :contentReference[oaicite:7]{index=7}  
- **Pose sensing.** The device logs **quaternion** \(q(t)\), **linear acceleration** \(a(t)\), and **angular velocity** \(\omega(t)\). :contentReference[oaicite:8]{index=8}  
- **Stability gating.** Exponential moving averages of \(\|a\|\) and \(\|\omega\|\) are thresholded within a holding window to suppress high-frequency disturbances prior to accepting frames. :contentReference[oaicite:9]{index=9}  
- **Spherical mapping.** The camera forward vector is projected onto a **longitude–latitude grid**; normalized angles are wrapped/saturated and quantized to grid indices for online coverage bookkeeping. :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}  
- **Area-weighted coverage.** Coverage uses spherical surface-area weights to avoid overestimation near the poles; morphological refinements (adaptive pole dilation, hole filling) improve local consistency **without** changing area-weighted coverage. :contentReference[oaicite:12]{index=12} :contentReference[oaicite:13]{index=13} :contentReference[oaicite:14]{index=14}

---

## 🧪 Experimental Setting (brief)
Mobile capture was conducted on a **Redmi K70 Pro** with angle logging and IMU-based stability gating; off-device reconstruction used **3DGS** on a workstation with an **NVIDIA RTX 5090D**. The evaluation target included a tabletop object (“Coinbank”). :contentReference[oaicite:15]{index=15}

---

## 🎬 Demo & Showcase (placeholders)

- **Interface & workflow screenshots**  
  *Add PNG/JPG assets under `docs/` and reference them here.*  
  `![Capture UI](docs/ui.png)`  
  `![Spherical Grid](docs/grid.png)`

- **Short clip / live capture**  
  *Optional MP4/GIF under `docs/` or an external link.*  
  `[Demo video](docs/demo.mp4)`

- **Reconstruction views**  
  *Side-by-side renderings at matched viewpoints as in the paper.* :contentReference[oaicite:16]{index=16}

---

## 🗺️ Repository Notes
- `docs/` — assets for the demo/showcase and GitHub Pages (to be populated).  
- Additional source or scripts can be added in future updates, consistent with the manuscript.

