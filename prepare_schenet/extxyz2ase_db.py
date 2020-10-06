import os
from ase.db import connect
from ase.io.extxyz import read_xyz
from tqdm import tqdm
import tempfile
import argparse


def extxyz_to_db(extxyz_path, db_path):    
    r"""
    Convertes en extxyz-file to an ase database

    Args:
        extxyz_path (str): path to extxyz-file
        db_path(str): path to sqlite database
    """

    with connect(db_path, use_lock_file=False) as conn:
        with open(extxyz_path) as f:
            for at in tqdm(read_xyz(f, index=slice(None)), "creating ase db"):
                data = {}
                if at.has("forces"):
                    data["forces"] = at.get_forces()
                data.update(at.info)
                conn.write(at, data=data)



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to extxyz-file with molecular data.",
    )
    parser.add_argument("db_path", type=str, help="Path to output database.")
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing database file."
    )

    return parser


def main(args):
    if args.overwrite and os.path.exists(args.db_path):
        os.remove(args.db_path)

    extxyz_to_db( args.file_path, args.db_path)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
