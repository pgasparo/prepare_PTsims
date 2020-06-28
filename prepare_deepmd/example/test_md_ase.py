from ase import Atoms
from ase.io import read,write

from deepmd.calculator import DP



bromo = Atoms('C28H16Br2',

              positions=[
                          (26.8908 , 21.3879 , 41.1526 ),
                          (26.6092 , 19.9102 , 43.2596 ),
                          (24.1639 , 19.2185 , 44.1742 ),
                          (24.729  , 22.1873 , 39.7882 ),
                          (22.3498 , 21.4238 , 40.4912 ),
                          (21.9511 , 19.982  , 42.7324 ),
                          (19.4982 , 19.3943 , 43.6073 ),
                          (23.7917 , 17.8674 , 46.4325 ),
                          (21.3728 , 17.376  , 47.4265 ),
                          (20.9665 , 16.1269 , 49.7829 ),
                          (18.5798 , 15.7509 , 50.7221 ),
                          (19.1902 , 18.2    , 45.9903 ),
                          (16.7449 , 17.7956 , 47.0693 ),
                          (16.4406 , 16.6164 , 49.3596 ),
                          (16.605  , 26.9645 , 42.0181 ),
                          (17.514  , 24.5853 , 42.5207 ),
                          (16.1288 , 22.3706 , 41.8423 ),
                          (14.1862 , 27.2801 , 40.9069 ),
                          (12.6952 , 25.2108 , 40.4061 ),
                          (13.5928 , 22.7069 , 40.8483 ),
                          (12.1415 , 20.5243 , 40.3986 ),
                          (17.153  , 19.912  , 42.1163 ),
                          (15.7792 , 17.8031 , 41.1979 ),
                          (16.8866 , 15.3446 , 41.0902 ),
                          (15.4995 , 13.2489 , 40.4288 ),
                          (13.1582 , 18.0733 , 40.4515 ),
                          (11.7579 , 15.8435 , 39.8468 ),
                          (12.8898 , 13.4945 , 39.8713 ),
                          (28.259  , 19.2884 , 44.3141 ),
                          (20.719  , 22.0266 , 39.3857 ),
                          (22.6049 , 15.4882 , 50.8469 ),
                          (15.0914 , 18.4645 , 46.0507 ),
                          (28.7654 , 21.9548 , 40.5157 ),
                          (24.9557 , 23.4798 , 38.197  ),
                          (18.3285 , 14.8022 , 52.5325 ),
                          (14.5528 , 16.3518 , 50.1344 ),
                          (19.3659 , 24.3567 , 43.3843 ),
                          (10.7998 , 25.4735 , 39.6483 ),
                          (18.8821 , 15.1537 , 41.5475 ),
                          ( 9.74721, 16.0041 , 39.4424 ),
                          (17.7426 , 28.618  , 42.4697 ),
                          (13.4889 , 29.1679 , 40.4685 ),
                          (16.3953 , 11.3988 , 40.34   ),
                          (11.7673 , 11.8221 , 39.4348 ),
                          (26.6999 , 16.7071 , 48.2749 ),
                          ( 8.61148, 20.9193 , 39.6087 )  ] , 

              cell=[100, 100, 100],

              calculator=DP(model="graph.pb"))

#print(water.get_potential_energy())

#print(water.get_forces())


# from ase.optimize import BFGS
# dyn = BFGS(bromo, trajectory='bromotest.traj')
# dyn.run(fmax=1e-2)



# Set the momenta corresponding to T=100K
from ase.atoms import Atoms
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from ase.io.trajectory import Trajectory
import ase.io
from ase import units
hareV=27.211399
MaxwellBoltzmannDistribution(bromo, 100 * units.kB)
# We want to run MD with constant energy using the VelocityVerlet algorithm.
dyn = VelocityVerlet(bromo, 1 * units.fs)  # 1 fs time step.

def printenergy(a):
    """Function to print the potential, kinetic and total energy"""
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
          'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))


traj = Trajectory('bromotest.traj', 'w', bromo)
dyn.attach(traj.write, interval=1)


# Now run the dynamics

printenergy(bromo)

for i in range(3):
    dyn.run(10)
    printenergy(bromo)

