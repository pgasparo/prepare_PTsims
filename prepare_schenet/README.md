# Prepare PT simulations

## Generate the input data for training a Schenet MLP

Enter in the right directory and assemble the i-pi files
into a unique extended xyz:

```bash
cd example
tar xzvf example_ipitraj_NVT.tgz
python get_extended_xyz.py pk157415_C36H240Au896 
```

