#!/bin/sh

rm -r data/0001/rgb/*
rm -r data/0001/depth/*

mkdir -p data/0001/rgb
mkdir -p data/0001/depth
mkdir -p data/0001/mask
mkdir -p data/0001/info

cp camera_poses.yml data/0001/info/camera_poses.yml
cp object_poses.yml data/0001/info/object_poses.yml
cp object_color.yml data/0001/info/object_color.yml

python camera_mover.py &
python image_saver.py

