# Prepare PT sims

## Generate simulation files

First enter in the right directory

```bash
cd generate_inputs
```

Here you'll find just a bunch of scripts useful to prepare i-PI + CP2K MD simulations from template files.

The template-pt directory contains files for creating a PTMD simulations, while the template-nvt contains files to generate a standard NVT MD simulation.

Usage:


```bash
ln -s template-pt template
./prepare_sim pk160171_C100H258Au896.xyz
```
N.B.: you might want the change the submission script according to your needs

## Prepare DeepMD training files from simulation outputs

```bash
cd prepare_deepmd
```

Here you find some script to format the raw i-PI output files to a raw format which is deepmd-ready 

```bash
commands
```

