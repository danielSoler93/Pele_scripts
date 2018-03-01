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

   For any problem do not hesitate to contact us through the email address written below.

"""

__author__ = "Daniel Soler Viladrich"
__email__ = "daniel.soler@nostrumbiodiscovery.com"

# DEFAULT VALUES
ORDER = "min"
CRITERIA = "Binding Energy"
OUTPUT = "Structure_{}.pdb"
N_STRUCTS = 10
FREQ = 1
REPORT = "report"
TRAJ = "trajectory"
ACCEPTED_STEPS = 'numberOfAcceptedPeleSteps'
PATH = 'path'


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, help="Minimum Value", required=True)
    parser.add_argument("--max", type=int, help="Maximum Value", required=True)
    parser.add_argument("path", type=str, help="Path to Pele's results root folder (Adaptive: path=/Pele/results/ Pele: path=/Pele/)")
    parser.add_argument("--crit", "-c", type=str, help="Criteria we want to rank and output the strutures for", default= CRITERIA)
    parser.add_argument("--nst", "-n", type=int, help="Number of produced structures", default=N_STRUCTS)
    parser.add_argument("--ofreq", "-f", type=int, help="Every how many steps the trajectory were outputted on PELE", default=FREQ)
    parser.add_argument("--out", "-o", type=str, help="Output Path", default=CRITERIA.replace(" ", ""))
    args = parser.parse_args()

    return args.min, args.max, args.path, args.crit, args.nst, args.ofreq, args.out


def main(min, max, path, criteria="sasaLig", n_structs=500, out_freq=FREQ, output=CRITERIA.replace(" ", "")):
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

        f_out: Name of the n outpu
    """

    # Get Files
    all_reports = glob.glob(os.path.join(path, "*/*report*"))
    reports = [report for report in all_reports if(os.path.basename(os.path.dirname(report)).isdigit())]

    # Data Mining
    min_values = parse_values(reports, n_structs, criteria, min, max)
    values = min_values[criteria].tolist()
    paths = min_values[PATH].tolist()
    epochs = [os.path.basename(os.path.normpath(os.path.dirname(Path))) for Path in paths]
    reports_indexes = min_values.report.tolist()
    step_indexes = min_values[ACCEPTED_STEPS].tolist()
    files_in = ["trajectory_{}.pdb".format(index) for index in reports_indexes]
    files_out = ["epoch{}_trajectory_{}.{}_{}{}.pdb".format(epoch, report, int(step), criteria.replace(" ",""), value) \
       for epoch, step, report, value in zip(epochs, step_indexes, reports_indexes, values)]
    for f_in, f_out, step, path in zip(files_in, files_out, step_indexes, paths):
        
        #Read Trajetory fro PELE's output
        with open(os.path.join(os.path.dirname(path), f_in), 'r') as input_file:
            file_content = input_file.read()
        trajectory_selected = re.search('MODEL\s+%d(.*?)ENDMDL' %int((step+1)/out_freq), file_content,re.DOTALL)
       
        #Output Trajectory
        try:
            os.mkdir(output)
        except OSError:
            pass
        
        try:
            traj = []
            with open(os.path.join(output,f_out),'w') as f:
                traj.append("MODEL     %d" %int((step+1)/out_freq))
                traj.append(trajectory_selected.group(1))
                traj.append("ENDMDL\n")
                f.write("\n".join(traj))
            print("MODEL {} has been selected".format(f_out))
        except AttributeError:
            raise AttributeError("MODEL {} not found".format(f_out))

    return files_out


def parse_values(reports, n_structs, criteria, min_value, max_value):
    """

       Description: Parse the 'reports' and create a sorted array
       of size n_structs following the criteria chosen by the user.

    """

    INITIAL_DATA = [(PATH, []),
                    (REPORT, []),
                    (ACCEPTED_STEPS, []),
                    (criteria, [])
                    ]

    values = pd.DataFrame.from_items(INITIAL_DATA)
    for file in reports:
        report_number = os.path.basename(file).split("_")[-1]
        data = pd.read_csv(file, sep='    ', engine='python')
        report_values = data.loc[:, [ACCEPTED_STEPS, criteria]]
        report_values.insert(0, PATH, [file]*report_values[criteria].size)
        report_values.insert(1, REPORT, [report_number]*report_values[criteria].size)
        report_values = report_values[report_values[criteria].between(min_value, max_value, inclusive=True)]
        try:
            values = pd.concat([values, report_values])
        except ValueError:
            values = report_values
    values.sort_values(criteria, ascending=False)
    print(values)
    return values




if __name__ == "__main__":
    min, max, path, criteria, interval, out_freq, output = parse_args()
    main(min, max, path, criteria, interval, out_freq, output)
