#!/usr/bin/env python
import sys
import os
import random
import numpy as np



def point_camera(dx, dy, dz, roll=0.0):

  base = np.sqrt(np.sum(np.square([dx, dy])))
  # arctan2 is just arctan but takes two arguments
  yaw = np.arctan2(dy,dx)
  pitch = -1.0*np.arctan2(dz,base)
  #print(dz, base)
  return roll, pitch, yaw

      


def main(args):
  num_of_pos = int(args[1])
  #print("generate ", n, "camera position")
  f = open("camera_script.txt", mode='w')

  for i in range(num_of_pos):

    # generate random value
    rand_roll = random.uniform(-0.3, 0.3)
    rand_theta = random.uniform(0, 2*3.14159)
    randr = random.uniform(0.7, 1.1)  # the distance between target and camera
    randz = random.uniform(0.25, 0.5) # camera height

    # xyr: xy-plane radius derivrd from r
    xyr = np.sqrt(np.square(randr) - np.square(randz-0.21)) #
    x = xyr*np.cos(rand_theta)
    y = xyr*np.sin(rand_theta)

    # points camera at (0.0, 0.0, 0.22)
    roll, pitch, yaw = point_camera(0.0-x, 0.0-y, 0.22-randz, rand_roll)

    out = "{},{},{},{},{},{}\n".format(x, y, randz, roll, pitch, yaw)
    print(out)
    f.write(out)
  f.close()
  	
if __name__ == '__main__':
    main(sys.argv)