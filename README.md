# Pele_scripts
Group of small scripts to perform pele analysis.

# Pele's PipeLine
-------------------------------
1) [Protein Preparation for Pele](https://github.com/Jelisa/mut-prep4pele)
2) [PlopRotTemp_SCHR2017](https://github.com/miniaoshi/PlopRotTemp_S_2017)
3) [Adaptive PELE](https://github.com/AdaptivePELE/AdaptivePELE)
4) [PELE(comercial software)](https://pele.bsc.es/pele.wt)
5) [Analysis Tools](https://github.com/miniaoshi/Pele_scripts)

# Analysis Tools
-------------------
- best_structs.py
    - **Description:** Parse all the reports found under 'path' and sort them all by the chosen criteria and output the n best structures.
    - **Requested arguments:**
    `$python best_structs.py <path not to the folder where you have the reports, the previous one (in case you have several epochs)!>`
    e.g. python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/
    - **Optional arguments:**
    **-c** "SASA" (report's column you want to order the structures by) --> default: Binding Energy
    **-s** "max or min" ( max to oreder from higher to lower values, min from lower to higher) --> Default: min
    **-f** frequency the Pele's controlfile save the output --> Default:1
    **-n** Strutures to be outputted --> Default:10
    - **command adaptive :**
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Adaptive/PadaI/PadaI_FULL4/`
    - **command pele:**
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/ -f 4`
    - **full command pele** (output 20 strutures sorted by sasa from higher to lower values taking into account PELE save the output every 4 steps):
    `$ python /home/dsoler/best_structs.py PELE++_Examples/Global/PadaI/   -c sasaLig -s max -n 20 -f 4`
    - **Output:**
The script will create a folder {criteria}_Structs (where criteria is Binding Energy by default) and inside you will have the structures named as: traj_{criteriaValue}_{epoch}.{report}.{step}.pdb