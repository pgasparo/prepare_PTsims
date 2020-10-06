# Prepare PT simulations

## Generate the input data for training a Schenet MLP

Enter in the right directory and assemble the i-pi files
into a unique extended XYZ:

```bash
cd example
tar xzvf example_ipitraj_NVT.tgz
python get_extended_xyz.py pk157415_C36H240Au896 
```

Convert the extended XYZ to an ASE DB:

```bash
python extxyz2ase_db.py pk157415_C36H240Au896.extxyz pk157415_C36H240Au896.db
```

You can test if the db works well by doing the in a python shell:

```python
import os 
import schnetpack as spk
from schnetpack.data import AtomsData

new_dataset = AtomsData("pk157415_C36H240Au896.db")

print('Number of reference calculations:', len(new_dataset))

atoms, properties = new_dataset.get_properties(0)

print('Loaded properties:\n', *['{:s}\n'.format(i) for i in properties.keys()])
```
