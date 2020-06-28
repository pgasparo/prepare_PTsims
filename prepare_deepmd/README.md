# Prepare the raw input files for DeepMD

Here you find some scripts to post-process the output of an i-PI (PT)MD and prepare the raw files for DeepMD.

Get the coordinates from an xyz (.pos_0.xyz):

```bash
python ./getcoord.py -pt 56 pk129297_C33H240Au896
```

Get the force from an xyz (.for_0.xyz):

```bash
python ./getforce.py -pt 56 pk129297_C33H240Au896
```

Get the energy from the output (.out):

```bash
./getenergy.sh pk129297_C33H240Au896 4 56 > energy.raw
```

N.B.: if the number of replicas is not specified, the script will assume one trajectory output file as input

Get the box from the centroid (.xc.pdb):

```bash
python ./getbox.py -pt 56 pk129297_C33H240Au896
```

Get the atom types from one file.
IMPORTANT: We assume that the atom types do not change in all frames.

```bash
python ./gettype.py 0_pk129297_C33H240Au896.pos_0.xyz 
```

Now, all these scripts can be applyes to each sytem (frames with the same atom types, number and order).
One can use the tool provided by deepmp-kit to transform the raws in `numpy` binary data that are directly used by the training program. 
User can use the script `$deepmd_source_dir/data/raw/raw_to_set.sh` to convert the prepared raw files to data sets. For example, if we have a raw file that contains 6000 frames, 

```bash
$ cd pk129297_C33H240Au896 
$ python ./getcoord.py -pt 56 pk129297_C33H240Au896 ; python ./getforce.py -pt 56 pk129297_C33H240Au896 ; ./getenergy.sh pk129297_C33H240Au896 4 56 > energy.raw ; python ./getbox.py -pt 56 pk129297_C33H240Au896 ; python ./gettype.py 0_pk129297_C33H240Au896.pos_0.xyz ; mkdir deepmdsets/ ; mv *raw deepmdsets
$ cd deepmdsets
$ ls 
box.raw  coord.raw  energy.raw  force.raw  type.raw 
$ $deepmd_source_dir/data/raw/raw_to_set.sh 2000
nframe is 6000
nline per set is 2000
will make 3 sets
making set 0 ...
making set 1 ...
making set 2 ...
$ ls 
box.raw  coord.raw  energy.raw  force.raw  set.000  set.001  set.002  type.raw  
```

It generates three sets `set.000`, `set.001` and `set.002`, with each set contains 2000 frames. The last set (`set.002`) is used as testing set, while the rest sets (`set.000` and `set.001`) are used as training sets. One do not need to take care of the binary data files in each of the `set.*` directories. The path containing `set.*` and `type.raw` is called a *system*.

