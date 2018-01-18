import sys
import os
import argparse
import pandas as pd
import glob
import re


"""

   Description: Parse all the reports found under 'path' and sort them all
   by the chosen criteria (Binding Energy as default) having into account the
   frequency our pele control file writes a structure through the -ofreq param
   (1 by default). To sort from higher to lower value use -f "max" otherwise
   will rank the structures from lower to higher criteria's values. The number 
   of structures will be ranked is controlled by -i 'nstruct' (default 10).

   For any problem do not hesitate to write to the email address written below.

"""

__author__ = "Daniel Soler Viladrich"
__email__ = "daniel.soler@nostrumbiodiscovery.com"

ORDER = "min"
CRITERIA = "Binding Energy"
OUTPUT = "Structure_{}.pdb"
N_STRUCTS = 10
FREQ=1
REPORT = "report"
N_ACCEPTED_STEPS = 'numberOfAcceptedPeleSteps'


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to Pele's results root folder (Adaptive: path=/Pele/results/ Pele: path=/Pele/)")
    parser.add_argument("--crit", "-c", type=str, help="Criteria we want to rank and output the strutures for", default= CRITERIA)
    parser.add_argument("--int", "-i", type=int, help="Number of produced structures" , default=N_STRUCTS)
    parser.add_argument("--sort", "-s", type=str, help="Look for minimum or maximum value --> Options: [min/max]", default=ORDER)
    parser.add_argument("--ofreq", "-f", type=int, help="Every how many steps the trajectory were outputted on PELE", default=FREQ)
    args = parser.parse_args()

    
    return args.path, args.crit, args.int, args.sort, args.ofreq



def main(path, criteria, n_structs, sort_order, out_freq):
    """

      Description: Rank the traj found in the report files under path
      by the chosen criteria. Finally, output the best n_structs.

      Input:

         Path: Path to look for *report* files in all its subfolders.
         
         Criteria: Criteria to sort the structures. 
         Needs to be the name of one of the Pele's report file column.
         (Default= "Binding Energy")

         n_structs: Numbers of structures to create.

         sort_order: "min" if sorting from lower to higher "max" from high to low.

         out_freq: "Output frequency of our Pele control file"

     Output:

        f_out: Name of the n outputted structs.

    """ 

    #Initial Values
    reports = glob.glob(os.path.join(path,"*/*report*")) 
        
    #Data Mining
    min_values, f_in_dir = parse_values(reports, n_structs, criteria)

    reports_indexes = min_values.loc[:,REPORT].tolist()
    step_indexes = min_values.loc[:, N_ACCEPTED_STEPS].tolist()
    files_in = ["trajectory_{}.pdb".format(index) for index in reports_indexes]
    files_out = ["trajectory_{}.{}_{}{}.pdb".format(report,step, criteria.replace(" ",""), rank) for rank, (step, report) in enumerate(zip(step_indexes, reports_indexes))]
    for f_in, f_out, step in zip(files_in, files_out, step_indexes):
        
        #Read Trajetory fro PELE's output
        with open(os.path.join(f_in_dir, f_in), 'r') as input_file:
            file_content = input_file.read()
        trajectory_selected = re.search('MODEL\s+%d(.*?)ENDMDL' %int(step/out_freq), file_content,re.DOTALL)
       
        #Output Trajectory
        output = "{}_Structs".format(criteria.replace(" ",""))
        try:
            os.mkdir(output)
        except FileExistsError:
            pass

        traj = []
        with open(os.path.join(output,f_out),'w') as f:
            traj.append("MODEL     %d" %int(step/out_freq))
            traj.append(trajectory_selected.group(1))
            traj.append("ENDMDL\n")
            f.write("\n".join(traj))
        print("MODEL {} has been selected".format(f_out))
    return files_out


def parse_values(reports, n_structs, criteria):
    """
      
       Description: Parse the 'reports' and create a sorted array
       of size n_structs following the criteria chosen by the user.

    """    
    min_values = pd.DataFrame.from_items([(REPORT, [None]*n_structs),('numberOfAcceptedPeleSteps', [None]*n_structs),(criteria, [None]*n_structs)])
    
    for file in reports:
        report_number = os.path.basename(file).split("_")[-1]
        f_in_dir = os.path.abspath(os.path.dirname(file))
        data = pd.read_csv(file, sep='    ',engine='python')
        #Select only the columns correspondent to the numberOfAcceptedPeleSteps(if you sum 1 to this number you can obtain the step in the trajectory) and the criteria
        selected_data = data.loc[:, [N_ACCEPTED_STEPS,criteria]]
        if sort_order == "min":
                report_values =  selected_data.nsmallest(n_structs, criteria)
                report_values.insert(0, REPORT, [report_number]*n_structs)
                mixed_values = pd.concat([min_values, report_values])
                min_values = mixed_values.nsmallest(n_structs, criteria)

        else:
                report_values =  selected_data.nsmallest(n_structs, criteria)
                mixed_values = pd.concat([min_values, report_values])
                min_values = mixed_values.nsmallest(n_structs, criteria)
    return min_values, f_in_dir

if __name__ == "__main__":
    path, criteria, interval, sort_order, out_freq = parse_args()
    main(path, criteria, interval, sort_order, out_freq)
