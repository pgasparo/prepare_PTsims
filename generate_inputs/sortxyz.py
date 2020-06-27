#!/usr/bin/python

from ase.io import read,write
import numpy as np
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("filename", help="Name of the input structure file (.xyz or .pdb)")
    parser.add_argument("-o",type=str,default="init",help="Name of the output files")
    parser.add_argument("-dir",type=str,default="",help="Prefix for the output directory")
    args = parser.parse_args()

    name=os.path.splitext(args.filename)[0]
    ex=""
    try:
        ex=os.path.splitext(args.filename)[1]
    except:
        print("Something is wrong with the filename.")    

    ofile=args.o

    if args.dir=="" :
        odir=name


    frame=read(name+".xyz")
    frame.pbc=True
    
    # os.getcwd()
    try:
        os.mkdir(odir)
    except OSError as error:
        print(error)

    # sort atoms
    write(odir+"/"+ofile+".pdb",frame[np.argsort(frame.positions[:,2])])
    write(odir+"/"+ofile+".xyz",frame[np.argsort(frame.positions[:,2])])
    
    # print out the indeces of the bottom layers
    st=np.sort(list(set(list(map(int,frame.positions[:,2])))))+1
    # assuming we have H<Au<Au<Au<Au<Molecule
    zpos=st[1]
    print(list(np.where(frame[np.argsort(frame.positions[:,2])].positions[:,2]<zpos)[0]))
    
