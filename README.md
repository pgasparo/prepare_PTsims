# Prepare PT simulations

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

After having collected enough statistics we can proceed training the potential.

```bash
cd prepare_deepmd
```
Inside the directory you will find more information about the preparation of training sets.
