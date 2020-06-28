#!/usr/bin/python

from ase.io import read,write
import numpy as np
import argparse
import os
import sys

def read_traj(nametrajfile):
    try:
        frame=read(nametrajfile,":")
    except:
        print("Error!!! Something is wrong while opening the file.")    

    return frame

labels = {
  "Au": 0,
  "H": 1,
  "C": 2,
  "Br": 3,
  "N": 4,
  "O": 5
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="XYZ to coord.raw")
    parser.add_argument("filename", help="NAME of the trajectory file (typically NAME.xyz for MDs or X_NAME.pos_0.xyz for PTMDs)")
    parser.add_argument("-o",type=str,default="type.raw",help="Name of the output files")
    args = parser.parse_args()

    ofile=args.o
    name=args.filename

    # Get the file  
    frames=read_traj(name)

    atomtypes=np.asarray([labels[i] for i in frames[0].symbols])
    

    # save on a single file and convert to angstrom
    np.savetxt(ofile, [atomtypes], fmt='%d',delimiter=' ')

