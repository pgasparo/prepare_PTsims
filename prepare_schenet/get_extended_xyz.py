from ase.io import read,write
import numpy as np
import argparse
import os
import sys

from ase.io.extxyz import read_xyz
import tempfile
import argparse

import warnings
warnings.filterwarnings('ignore')

# from bohrradius to angstrom
pos_atu2ang=0.52917721
# from hartree to eV
en_atu2eV=27.211386245988
# from hartree/bohrradius to eV/angstrom
for_atu2eV_ang=51.42208619083232


def read_traj(nametrajfile):
    try:
        frame=read(nametrajfile,":")
    except:
        print("Error!!! Something is wrong while opening the file.")    

    return frame

def ipixyz2coords_A(nametrajfile):
    frame=read_traj(nametrajfile)
    # convert to the coordinates from bohrradius to angstrom
    return np.asarray([fr.positions*pos_atu2ang for fr in frame],dtype=np.float32)

def ipiforce2force_ev_A(nametrajfile):
    frame=read_traj(nametrajfile)
    # convert the forces from hartree/bohrradius to eV/angstrom
    return np.asarray([fr.positions*for_atu2eV_ang for fr in frame],dtype=np.float32)

def ipixyz2types(nametrajfile):
    frame=read_traj(nametrajfile)
    # convert to the coordinates from bohrradius to angstrom
    return np.asarray([fr.get_chemical_symbols() for fr in frame])

def get_total_energy_fromlogs(logsfile,idcolumn=3):
    r"""
    Gets the total energy from an i-pi .out file 

    Args:
        logsfile (str): path to .out i-pi file
        idcolumn(int): column containing the potential energy
    """
    
    # Load the logs, discards the comment lines
    return np.loadtxt(logsfile,comments=['#', '$', '@'])[:,idcolumn]*en_atu2eV


def ipixc2cells_A(nametrajfile):
    frame=read_traj(nametrajfile)
    # if reading the centroid pdb, the coordinates are already in angstrom
    return np.vstack([np.hstack(fr.cell[:]) for fr in frame])

def assemble_extxyz(
    extxyz_path,
    types,
    coords,
    forces,
    energies,
    cells,
):
    """
    Assemble an extxyz containing positions and forces + energy and PBC

    Args:
        xyz_path (str): path to the xyz file
        extxyz_path (str): path to extxyz-file
        atomic_properties (str): property-string
        molecular_properties (list): molecular properties contained in the
            comment line
    """
    new_file = open(extxyz_path, "w")
    
    atomic_properties="Properties=species:S:1:pos:R:3:forces:R:3"
    
    for i,v in enumerate(cells):
        natoms=len(coords[i])
        new_file.writelines(str(natoms) + "\n")
        
        comment = (" ".join([
                    "{}={}".format(prop, val)
                    for prop, val in zip(["energy","Lattice","pbc"], [energies[i],v,"\"T T T\""])
                ])).replace('[','\"').replace(']','\"')
        
        new_file.writelines(" ".join([atomic_properties, comment]) + "\n")
            
        for r in range(natoms):
            crdsline=" ".join('%0.4f' % item for item in coords[i,r])
            frcsline=" ".join('%0.15f' % item for item in forces[i,r])
            row="{} {} {}\n".format(types[i,r],crdsline,frcsline)
            new_file.writelines(row)
    new_file.close()

def ipi2xyz(filename):
    energies=get_total_energy_fromlogs(filename+".out")

    coords=ipixyz2coords_A(filename+".pos_0.xyz")
    types=ipixyz2types(filename+".pos_0.xyz")
    assert len(energies) == len(coords), (
                    "The number of total energies and frames do not match!"
                )
    
    forces=ipiforce2force_ev_A(filename+".for_0.xyz")
    assert len(energies) == len(forces), (
                    "The number of total energies and forces do not match!"
                )
    
    cells=ipixc2cells_A(filename+".xc.pdb")
    assert len(energies) == len(cells), (
                    "The number of total energies and cell lines do not match!"
                )
    

    # WRITE OUT THE FILE
    assemble_extxyz(
        filename+".extxyz",
        types,
        coords,
        forces,
        energies,
        cells,
    )






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="i-pi to extended XYZ")
    parser.add_argument("filename", help="NAME of the trajectory file (typically NAME.pos_0.xyz for MDs or X_NAME.pos_0.xyz for PTMDs)")
    parser.add_argument("-pt",type=int,default=0,help="Number of PT replicas (<1: single file, >1: N replicas)")
    args = parser.parse_args()

    name=args.filename

    if args.pt<1:
        # Single traj
        ipi2xyz(name)
    else:
        # PT replicas
        for i in range(args.pt):
            ipi2xyz(str(i)+"_"+name)
        bashcommand="".join(["{}_{}.extxyz ".format(i,name) for i in range(args.pt)])
        #os.system("cat "+bashcommand+" > {}.extxyz".format(name))
        os.system(f"cat {bashcommand} > {name}.extxyz")
        os.system("rm "+bashcommand)


        # fr_coords=np.vstack([xyz_to_coord(str(i)+"_"+name+".pos_0.xyz") for i in range(args.pt)])

    # save on a single file and convert to angstrom
    # np.savetxt(ofile, fr_coords, fmt='%.5e', delimiter=' ')

