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

def xyz_to_coord(nametrajfile):
    frame=read_traj(nametrajfile)
    # convert to the proper force unit (eV/A)
    return np.vstack([np.hstack(fr.positions)*for_atu2ev_ang for fr in frame])


# from bohrradius to angstrom
pos_atu2ang=0.52917721
# from hartree/bohrradius to eV/bohrradius
for_atu2ev_ang=51.422067

labels = {
  "Au": 0,
  "H": 1,
  "C": 2,
  "Br": 3,
  "N": 4,
  "O": 5
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="XYZ to force.raw")
    parser.add_argument("filename", help="NAME of the trajectory file (typically NAME.xyz for MDs or X_NAME.for_0.xyz for PTMDs)")
    parser.add_argument("-o",type=str,default="force.raw",help="Name of the output files")
    parser.add_argument("-pt",type=int,default=0,help="Number of PT replicas (<1: single file, >1: N replicas)")
    args = parser.parse_args()

    ofile=args.o
    name=args.filename

    if args.pt<1:
        # Single traj

        # Generate a file coord.raw containing K frames with each frame having the positions of N atoms.
        # E.g, 3 frames and 2 atoms: the file coord.raw will have 3 lines and 6 columns. 
        # Each line provides all the 3 positions components of 2 atoms in 1 frame (unit is Angstrom). 
        # The first three numbers are the 3 positions components of the first atom, 
        # while the second three numbers are the 3 positiom components of the second atom. 
        
        fr_coords=xyz_to_coord(name+".xyz")
    else:
        # PT replicas
        fr_coords=np.vstack([xyz_to_coord(str(i)+"_"+name+".for_0.xyz") for i in range(args.pt)])

    # save on a single file and convert to angstrom
    np.savetxt(ofile, fr_coords, fmt='%.5e', delimiter=' ')

