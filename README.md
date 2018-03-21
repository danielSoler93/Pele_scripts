# Pele_scripts
Group of small scripts to perform pele analysis.

# Main Pele's Software
-------------------------------
1) [Protein Preparation for Pele](https://github.com/Jelisa/mut-prep4pele)
2) [PlopRotTemp_SCHR2017](https://github.com/miniaoshi/PlopRotTemp_S_2017)
3) [Adaptive PELE](https://github.com/AdaptivePELE/AdaptivePELE)
4) [PELE(comercial software)](https://pele.bsc.es/pele.wt)
5) [Analysis Tools](https://github.com/miniaoshi/Pele_scripts)
6) [Ligand Growing](https://github.com/miniaoshi/Ligand_growing)

# Analysis Tools
-------------------
- bestSturcts.py
    - **Description:**  <br />
    Parse all the folders with reports found under the current directory and sort them all by the chosen criteria and output the n best structures.
    - **Requested arguments:** <br />
    $python best_structs.py <criteria> <br />
    e.g. python /home/dsoler/best_structs.py Binding Energy. <br />
    `Note: The criteria must be one of the report's column names.`
    - **Optional arguments:** <br />
    **-as** "Accepted steps report column name. --> Default: NumberAcceptedSteps. <br />
    i.e: -as AcceptedSteps <br />
    `Important in case your report column name is different than "NumberAcceptedSteps"`<br/>
    **-s** "max or min" ( max to order from higher to lower values, min from lower to higher) --> Default: min. <br />
    i.e: -s max<br />
    **-f** frequency the Pele's controlfile save the output --> Default:1. <br />
    i.e: -f 4 <br />
    `Important in case the output save frequency of your control file is >1` <br />
    **-n** Structures to be outputted --> Default:10. <br />
    i.e: -n 10<br />
    **-o** Output Folder --> Default Criteria's name <br />
    i.e: -o PRR_apo_Binding_energies
    **-nm** Non numerical folders --> Default: False <br />
    i.e: -nm

    - **command adaptive :** <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/
    - **command pele:** <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/ -f 4
    - **full command pele** (output 20 strutures sorted by sasa from higher to lower values taking into account PELE save the output every 4 steps): <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/   -c sasaLig -s max -n 20 -f 4
    - **Output:** <br />
    The script will create a folder called {criteria} or {output} if -o option. Inside that one, you will have the structures named as: traj_{epoch}.{report}.{step}_{cirteria}_{value}.pdb

- rangeOfValues.py
    - **Description:**  <br />
    Parse all the folders with reports found under the current directory and sort them all by the chosen criteria and output the value range from [users_minimum_value:users_max_value].
    - **Requested arguments:** <br />
    $python best_structs.py <min_value> <max_value> <criteria> <br />
    e.g. python /home/dsoler/best_structs.py -50 -40 Binding Energy. <br />
    `Note: The criteria must be one of the report's column names.`
    - **Optional arguments:** <br />
    **-as** "Accepted steps report column name. --> Default: NumberAcceptedSteps. <br />
    i.e: -as AcceptedSteps <br />
    `Important in case your report column name is different than "NumberAcceptedSteps"`<br/>
    **-f** frequency the Pele's controlfile save the output --> Default:1. <br />
    i.e: -f 4 <br />
    `Important in case the output save frequency of your control file is >1` <br />
    **-o** Output Folder --> Default Criteria's name <br />
    i.e: -o PRR_apo_Binding_energies
    **-nm** Non numerical folders --> Default: False <br />
    i.e: -nm


    - **command adaptive :** <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/ 0 0.3 SasaLig
    - **command pele:** <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/ 0 0.3 SasaLig -f 4
    - **full command pele** (output 20 strutures sorted by sasa from higher to lower values taking into account PELE save the output every 4 steps): <br />
    $ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/   0 0.3 SasaLig -as AcceptedSteps -f 4 -o apo_pocket
    - **Output:** <br />
    The script will create a folder called {criteria} or {output} if -o option. Inside that one, you will have the structures named as: traj_{epoch}.{report}.{step}_{cirteria}_{value}.pdb
	
- box.py
    - **Description:**  <br />
    Create box given a 3 cooridnates center an a radius.
    - **Requested arguments:** <br />
    `$python box.py center_x center_y center_z radius` <br />
    e.g. python box.py 23.12 45.34 28.12 21
    - **Optional arguments:** <br />
    **-f** "file" (Output file) --> default: ./box.pdb
	The script will create a box.pdb with a cubic box showing pele's conformational space.

- backtrackAdaptiveTrajectory.py
    - **Description:**  <br />
     Recreate the trajectory fragments to the led to the discovery of a snapshot, specified by the tuple (epoch, trajectory, snapshot) and write as a pdb file. Should be run from the adaptive simulation folders
    - **Requested arguments:** <br />
    `$python backtrackAdaptiveTrajectory.py epoch_number trajectory_number snapshot_number` <br />
    e.g. python /path/backtrackAdaptiveTrajectory.py 4 12 3
    - **Optional arguments:** <br />
    **-o** "output_folder" (name of the folder where to store the pdb file) --> default: "" (store in current folder) <br />
    **--name** Name of the file to store the trajectory --> Default: "pathway.pdb"
    - **Output:** <br />
	The script will create a folder (if asked via the -o option) and inside you will have the file containing the trajectory that lead to snapshot of interest. If the filename already exists, a number will be appended to distinguish it, i.e. pathway.pdb --> pathway_1.pdb
