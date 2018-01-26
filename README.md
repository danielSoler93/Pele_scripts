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
- best_structs.py
    - **Description:**  <br />
    Parse all the reports found under 'path' and sort them all by the chosen criteria and output the n best structures.
    - **Requested arguments:** <br />
    `$python best_structs.py <path not to the folder where you have the reports, the previous one (in case you have several epochs)!>` <br />
    e.g. python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/
    - **Optional arguments:** <br />
    **-c** "SASA" (report's column you want to order the structures by) --> default: Binding Energy <br />
    **-s** "max or min" ( max to oreder from higher to lower values, min from lower to higher) --> Default: min <br />
    **-f** frequency the Pele's controlfile save the output --> Default:1 <br />
    **-n** Strutures to be outputted --> Default:10
    - **command adaptive :** <br />
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/`
    - **command pele:** <br />
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/ -f 4`
    - **full command pele** (output 20 strutures sorted by sasa from higher to lower values taking into account PELE save the output every 4 steps): <br />
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/   -c sasaLig -s max -n 20 -f 4`
    - **Output:** <br />
	The script will create a folder {criteria}_Structs (where criteria is Binding Energy by default) and inside you will have the structures named as: traj_{criteriaValue}_{epoch}.{report}.{step}.pdb
	
- box.py
    - **Description:**  <br />
    Create box given a 3 cooridnates center an a radius.
    - **Requested arguments:** <br />
    `$python box.py center_x center_y center_z radius` <br />
    e.g. python box.py 23 45 28 21
    - **Optional arguments:** <br />
    **-f** "file" (Output file) --> default: ./box.pdb
	The script will create a box.pdb with a cubic box showing pele's conformational space.