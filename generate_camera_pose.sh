#!/bin/sh

echo "Script name: $0"
echo "Argument 1: $1"

mkdir -p data/0001/rgb
mkdir -p data/0001/depth
mkdir -p data/0001/mask
mkdir -p data/0001/info

python camera_pose_generator.py $1

cp camera_poses.yml data/0001/info/camera_poses.yml
cp object_poses.yml data/0001/info/object_poses.yml
cp object_color.yml data/0001/info/object_color.yml

