# 3DGS OC Capture
*A mobile, object-centered multi-view capture workflow for **3D Gaussian Splatting (3DGS)** with real-time guidance.*

[**Project Page**](https://zyz-nwpu.github.io/3dgs-oc-capture/) • [**Paper**](#-citation)

---

## 🧩 Overview / 项目概述

**3DGS OC Capture** 是一个基于手机的、面向“物体中心”的多视角数据采集方案。  
它通过一次性标定把设备姿态对齐到参考坐标后，将相机前向轴映射到**物体中心的球面网格**，并在采集中实时计算**面积加权的覆盖率**来引导运动；同时利用**稳定性门控**确保只记录稳定帧，从而以较少图像获得更完整与更均匀的视角分布，提升 3D Gaussian Splatting 的重建一致性与细节质量。

> TL;DR — 用手机“围着物体转”，界面会告诉你哪些方向还没拍够、什么时候相机稳定可以记录帧，最终得到覆盖均匀的数据包，利于 3DGS 训练。

---

## ✨ Features / 主要特性

- **Object-Centered Spherical Capture**：把手机 IMU 姿态映射到以目标为中心的球面坐标系，统一视角表达。
- **Real-Time Coverage Guidance**：采用**面积加权**的球面覆盖率，实时提示尚未覆盖的方向，避免两极区域被低估。
- **Stability-Gated Frames**：基于加速度与角速度的平滑门控，仅在手持稳定时采样，减少运动模糊与姿态抖动影响。
- **One-Time Calibration**：一次标定建立参考朝向，后续姿态以“相对旋转”形式表达，跨次实验可比。
- **Ready for 3DGS**：产出图像与位姿；可与 3DGS 训练脚本对接，减少无效视角、提升重建一致性。

---

## 🖥️ Demo / 演示

> 📌 **占位**：此处可插入截图/GIF/视频链接（待你后续补充）。
>
> - `docs/` 内放置网页资源（GitHub Pages）。
> - README 中使用相对路径嵌入图片：`![UI](docs/ui.png)`
> - 演示视频可放到 `docs/demo.mp4` 或外链到 B 站/YouTube。

---

## 📦 Installation / 安装

> 📌 **占位**：根据你发布的可执行包/平台（Android/iOS/Windows/…）完善本节。下面给出通用骨架：

```bash
# Android 示例（占位）
# 1) 下载 Release 中的 APK
# 2) 安装到手机并授予相机、传感器权限
