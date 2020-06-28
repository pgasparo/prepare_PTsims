#!/bin/bash

#### USAGE :
#### 
#### ./get energy NAME Energy_Column Number_of_replicas
#### 
#### NAME=name of the file(s) , e.g. pk54345
#### Energy_Column=column containing the potential energy (OPTIANAL)
####               (default: 4)
#### Number_of_replicas=number of trajectories in the PTMD (OPTIONAL)
####                    (default: single trajctory (NO PTMD))


name=$1

if [[ -n $2 ]] 
then
   # set the column containing the potential energy
   ven=$2
else
   # Set the default energy column to 4
   ven=4
fi

if [[ -n $3 ]] 
then
   # PT MD
   for i in $(seq 0 $(($3-1))) 
   do
      awk -v Ne=$ven '!/#/{printf "%.9e\n",$Ne*27.211386}' ${i}_${name}".out"
   done 
else
   # Single traj
   awk -v Ne=$ven '!/#/{printf "%.9e\n",$Ne*27.211386}' ${name}".out"
fi
