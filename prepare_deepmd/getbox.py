#!/usr/bin/python

from ase.io import read,write
import numpy as np
import argparse
import os
import sys

def read_traj(nametrajfile):
    try:
        frame=read(nametrajfile,":")
        #for fr in frame:
        #    fr.pbc=True
    except:
        print("Error!!! Something is wrong while opening the file.")    

    return frame

def get_cells(nametrajfile):
    frame=read_traj(nametrajfile)
    # if reading the centroid pdb, the coordinates are already in angstrom
    return np.vstack([np.hstack(fr.cell[:]) for fr in frame])

# from bohrradius to angstrom
pos_atu2ang=0.52917721

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
    parser.add_argument("filename", help="NAME of the trajectory file (will read xc.pdb)")
    parser.add_argument("-o",type=str,default="box.raw",help="Name of the output files")
    parser.add_argument("-pt",type=int,default=0,help="Number of PT replicas (<1: single file, >1: N replicas)")
    args = parser.parse_args()

    ofile=args.o
    name=args.filename

    if args.pt<1:
        # Single traj

        # Generate a file box.raw from a trajectory with K frames.
        # In box.raw, the 9 components of the box vectors should be provided on each line.
        
        cells=get_cells(name+".xc.pdb")
    else:
        # PT replicas
        cells=np.vstack([get_cells(str(i)+"_"+name+".xc.pdb") for i in range(args.pt)])

    # save on a single file and convert to angstrom
    np.savetxt(ofile, cells, fmt='%.5e', delimiter=' ')

