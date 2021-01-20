#!/usr/bin/env python
import sys
import os
import random
import numpy as np
import yaml


def point_camera(dx, dy, dz, roll=0.0):

  base = np.sqrt(np.sum(np.square([dx, dy])))
  # arctan2 is just arctan but takes two arguments
  yaw = np.arctan2(dy,dx)
  pitch = -1.0*np.arctan2(dz,base)
  #print(dz, base)
  return roll, pitch, yaw

      
output_file = "camera_poses.yml"

def main(args):
  num_of_pos = int(args[1])
  #print("generate ", n, "camera position")
  cam_poses = {}

  for i in range(num_of_pos):

    # point camera at
    point_at_x = 0.0
    point_at_y = 0.0
    point_at_z = 0.28

    # generate random value
    rand_roll = random.uniform(-0.3, 0.3)
    rand_theta = random.uniform(0, 2*3.14159)
    randr = random.uniform(0.7, 1.1)  # the distance between target and camera
    randz = random.uniform(0.3, 0.55) # camera height

    # xyr: xy-plane radius derivrd from r
    xyr = np.sqrt( np.square(randr) - np.square(randz-point_at_z) ) # minus the zoffset
    x = xyr*np.cos(rand_theta)
    y = xyr*np.sin(rand_theta)

    # points camera at (0.0, 0.0, 0.22)
    roll, pitch, yaw = point_camera( point_at_x-x, point_at_y-y, point_at_z-randz, rand_roll)
    pose = [x, y, randz, roll, pitch, yaw]
    cam_poses[i] = [round(float(num), 8) for num in pose]
    print(cam_poses[i])

  with open(output_file, 'w') as f:
    yaml.dump_all([cam_poses], f)


  	
if __name__ == '__main__':
    main(sys.argv)