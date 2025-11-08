#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, csv, struct, math, subprocess, time, random
import numpy as np
from collections import namedtuple
from copy import deepcopy

scene_dir = r""
txt_file = r""
csv_file = r""

distorted_sparse = os.path.join(scene_dir, "distorted", "sparse", "0")
images_bin = os.path.join(distorted_sparse, "images.bin")
cameras_bin = os.path.join(distorted_sparse, "cameras.bin")
points3D_bin = os.path.join(distorted_sparse, "points3D.bin")

out_sparse = os.path.join(scene_dir, "sparse", "0")
colmap_bin = r""

if csv_file and (not os.path.exists(csv_file)):
    print("metadata.csv not found. Converting from txt ...")
    with open(txt_file, "r", encoding="utf-8") as f_in, open(csv_file, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["timestamp_ms", "filename", "theta_deg", "phi_deg", "Rrel9"])
        for line in f_in:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue
            timestamp, filename, theta, phi, Rvals = parts[0], parts[1], parts[2], parts[3], ",".join(parts[4].split(" "))
            writer.writerow([timestamp, filename, theta, phi, Rvals])
    print(f"Saved metadata.csv to: {csv_file}")
else:
    print("metadata.csv exists. Skipping conversion")

def read_next_bytes(fid, num_bytes, fmt, endian="<"):
    return struct.unpack(endian + fmt, fid.read(num_bytes))

def write_next_bytes(fid, data, fmt, endian="<"):
    if isinstance(data, (list, tuple)):
        fid.write(struct.pack(endian + fmt, *data))
    else:
        fid.write(struct.pack(endian + fmt, data))

def qvec2rotmat(q):
    qw, qx, qy, qz = q
    return np.array([
        [1 - 2*qy*qy - 2*qz*qz, 2*qx*qy - 2*qw*qz, 2*qx*qz + 2*qw*qy],
        [2*qx*qy + 2*qw*qz, 1 - 2*qx*qx - 2*qz*qz, 2*qy*qz - 2*qw*qx],
        [2*qx*qz - 2*qw*qy, 2*qy*qz + 2*qw*qx, 1 - 2*qx*qx - 2*qy*qy]
    ], dtype=float)

def rotmat2qvec(R):
    R = np.asarray(R, dtype=float)
    tr = np.trace(R)
    if tr > 0:
        S = math.sqrt(tr + 1.0) * 2.0
        qw = 0.25 * S
        qx = (R[2,1] - R[1,2]) / S
        qy = (R[0,2] - R[2,0]) / S
        qz = (R[1,0] - R[0,1]) / S
    elif (R[0,0] > R[1,1]) and (R[0,0] > R[2,2]):
        S = math.sqrt(1.0 + R[0,0] - R[1,1] - R[2,2]) * 2.0
        qw = (R[2,1] - R[1,2]) / S
        qx = 0.25 * S
        qy = (R[0,1] + R[1,0]) / S
        qz = (R[0,2] + R[2,0]) / S
    elif R[1,1] > R[2,2]:
        S = math.sqrt(1.0 + R[1,1] - R[0,0] - R[2,2]) * 2.0
        qw = (R[0,2] - R[2,0]) / S
        qx = (R[0,1] + R[1,0]) / S
        qy = 0.25 * S
        qz = (R[1,2] + R[2,1]) / S
    else:
        S = math.sqrt(1.0 + R[2,2] - R[0,0] - R[1,1]) * 2.0
        qw = (R[1,0] - R[0,1]) / S
        qx = (R[0,2] + R[2,0]) / S
        qy = (R[1,2] + R[2,1]) / S
        qz = 0.25 * S
    q = np.array([qw, qx, qy, qz])
    q /= np.linalg.norm(q)
    return q

def rot_diff(RA, RB):
    R = RA.T @ RB
    tr = (np.trace(R) - 1) / 2.0
    tr = max(-1.0, min(1.0, tr))
    return math.degrees(math.acos(tr))

Image = namedtuple("Image", ["id","qvec","tvec","camera_id","name","xys","point3D_ids"])

def read_images_binary(path):
    images = {}
    with open(path, "rb") as f:
        num_images = read_next_bytes(f, 8, "Q")[0]
        for _ in range(num_images):
            data = read_next_bytes(f, 64, "idddddddi")
            img_id = data[0]
            q = np.array(data[1:5])
            t = np.array(data[5:8])
            cam_id = data[8]
            name = ""
            c = read_next_bytes(f, 1, "c")[0]
            while c != b"\x00":
                name += c.decode("utf-8")
                c = read_next_bytes(f, 1, "c")[0]
            num_pts = read_next_bytes(f, 8, "Q")[0]
            if num_pts > 0:
                xyz = read_next_bytes(f, 24 * num_pts, "ddq" * num_pts)
                xs = xyz[0::3]; ys = xyz[1::3]; ids = xyz[2::3]
                xys = np.column_stack([xs, ys])
                ids = np.array(ids)
            else:
                xys = np.zeros((0,2)); ids = np.zeros((0,))
            images[img_id] = Image(img_id, q, t, cam_id, name, xys, ids)
    return images

def write_images_binary(images, path):
    with open(path, "wb") as f:
        write_next_bytes(f, len(images), "Q")
        for img in images.values():
            write_next_bytes(f, [img.id, *img.qvec, *img.tvec, img.camera_id], "idddddddi")
            for ch in img.name:
                write_next_bytes(f, ch.encode("utf-8"), "c")
            write_next_bytes(f, b"\x00", "c")
            write_next_bytes(f, len(img.point3D_ids), "Q")
            for (xy, pid) in zip(img.xys, img.point3D_ids):
                write_next_bytes(f, [float(xy[0]), float(xy[1]), int(pid)], "ddq")

print("\n=== Replace camera poses ===")
images = read_images_binary(images_bin)
print(f"Loaded {len(images)} image poses")

R_map = {}
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        Rvals = [float(x) for x in row["Rrel9"].split(",") if x]
        if len(Rvals) == 9:
            R_map[os.path.basename(row["filename"])] = np.array(Rvals).reshape(3,3)

new_images = deepcopy(images)
diag_path = os.path.join(scene_dir, "replace_diagnostic.csv")
rows = []
rot_diffs, center_diffs = [], []
changed = 0

for img_id, img in images.items():
    base = os.path.basename(img.name)
    if base not in R_map:
        continue
    R_old = qvec2rotmat(img.qvec)
    t_old = img.tvec
    R_new = R_map[base]
    t_new = R_new @ R_old.T @ t_old
    q_new = rotmat2qvec(R_new)
    new_images[img_id] = Image(img.id, q_new, t_new, img.camera_id, img.name, img.xys, img.point3D_ids)
    changed += 1

    rot_err = rot_diff(R_old, R_new)
    C_old = -R_old.T @ t_old
    C_new = -R_new.T @ t_new
    center_err = np.linalg.norm(C_old - C_new)
    rot_diffs.append(rot_err)
    center_diffs.append(center_err)
    rows.append([img_id, base, rot_err, center_err])

print(f"Replaced rotations for {changed} images and adjusted translation to keep camera centers fixed.")

with open(diag_path, "w", newline="", encoding="utf-8") as cf:
    writer = csv.writer(cf)
    writer.writerow(["img_id", "filename", "rot_err_deg", "center_err_m"])
    writer.writerows(rows)
print(f"Wrote diagnostic log: {diag_path}")

if rot_diffs:
    print("Rotation diff (deg): min={:.3f}, mean={:.3f}, median={:.3f}, max={:.3f}".format(
        np.min(rot_diffs), np.mean(rot_diffs), np.median(rot_diffs), np.max(rot_diffs)
    ))
if center_diffs:
    print("Center diff (m): min={:.6f}, mean={:.6f}, median={:.6f}, max={:.6f}".format(
        np.min(center_diffs), np.mean(center_diffs), np.median(center_diffs), np.max(center_diffs)
    ))

backup_path = images_bin + ".bak"
if not os.path.exists(backup_path):
    os.rename(images_bin, backup_path)
    print("Backed up original images.bin to:", backup_path)
write_images_binary(new_images, images_bin)
print("Wrote new images.bin")

print("\n=== Run COLMAP image_undistorter ===")
cmd = [
    colmap_bin, "image_undistorter",
    "--image_path", os.path.join(scene_dir, "input"),
    "--input_path", os.path.join(scene_dir, "distorted", "sparse", "0"),
    "--output_path", os.path.join(scene_dir, "sparse"),
    "--output_type", "COLMAP"
]
print("Command:", " ".join(cmd))
try:
    subprocess.check_call(cmd)
    print("Undistortion finished. Output:", out_sparse)
except Exception as e:
    print("Undistortion failed:", e)

print("\nDone.")
print("See replace_diagnostic.csv for rotation and center differences.")
