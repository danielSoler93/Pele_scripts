import os
import argparse
import pandas as pd
import glob
import re
import sys

"""

   Description: Parse all the reports found under 'path' and sort them all
   by the chosen critera outputting the desired value range. Be carefull to specify
   the frequency your pele control file writes a structure through the -ofreq param
   (1 by default).

   Command: python range.py min_value max_value report_column
   Command: python range.py -50 0 Binding Energy

   For any problem do not hesitate to contact us through the email address written below.

"""

__author__ = "Daniel Soler Viladrich"
__email__ = "daniel.soler@nostrumbiodiscovery.com"

# DEFAULT VALUES
ORDER = "min"
CRITERIA = ["Binding", "Energy"]
FREQ = 1
REPORT = "report"
ACCEPTED_STEPS = 'numberOfAcceptedPeleSteps'
PATH = os.path.abspath(os.getcwd())
STEPS = 3
OUTPUT_FOLDER = 'RangeValues'

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("min", type=float, help="Minimum Value Range i.e: -50")
    parser.add_argument("max", type=float, help="Maximum ValueRange i.e: 0")
    parser.add_argument("criteria", type=str, nargs='+', help="Criteria we want to rank and output the strutures for. Must be a column of the report. i.e: Binding Energy")
    parser.add_argument("--ofreq", "-f", type=int, help="Every how many steps the trajectory were outputted on PELE i.e: 4", default=FREQ)
    parser.add_argument("--out", "-o", type=str, help="Output Path i.e: BE_apo", default=OUTPUT_FOLDER)
    parser.add_argument("--numfolders", "-nm", action="store_true", help="Not to parse non numerical folders")
    args = parser.parse_args()
    return args.min, args.max, " ".join(args.criteria), args.ofreq, args.out, args.numfolders


def main(min, max, criteria, out_freq=FREQ, output="".join(CRITERIA),  numfolders=False):
    """

      Description: Get a range of values from a desire metric

      Input:

        min: minimum value range

        max: maximum value range

        Criteria: Criteria to sort the structures.
        Needs to be the name of one of the Pele's report file column.

        out_freq: Output frequency of our Pele control file

        output: Name of the output folder where to save the trajectories

        steps: Name of the accepted steps column in your report

    """

    reports = glob.glob(os.path.join(PATH, "*/*report*"))
    reports = glob.glob(os.path.join(PATH, "*report*")) if not reports else reports
    reports = filter_non_numerical_folders(reports, numfolders)
    try:
        reports[0]
    except IndexError:
        raise IndexError("Not report file found. Check you are in adaptive's or Pele root folder")

    if criteria.isdigit():
        steps, criteria = get_column_names(reports, STEPS, criteria)
    else:
        steps = get_column_names(reports, STEPS, criteria)


    # Data Mining
    min_values = parse_values(reports, criteria, min, max, steps)
    values = min_values[criteria].tolist()
    paths = min_values[PATH].tolist()
    epochs = [os.path.basename(os.path.normpath(os.path.dirname(Path))) for Path in paths]
    file_ids = min_values.report.tolist()
    step_indexes = min_values[steps].tolist()
    try:
        files_out = ["epoch{}_trajectory_{}.{}_{}{}.pdb".format(epoch, report, int(step), criteria.replace(" ",""), value) \
            for epoch, step, report, value in zip(epochs, step_indexes, file_ids, values)]
    except ValueError:
        raise ValueError("The accepted step column of the report is different than {}. Run the command againd with the option -as <name of your acceptedsteps column>".format(ACCEPTED_STEPS))
    for f_id, f_out, step, path in zip(file_ids, files_out, step_indexes, paths):

        # Read Trajetory from PELE's output
        f_in = glob.glob(os.path.join(os.path.dirname(path), "*trajectory*_{}.pdb".format(f_id)))
        if len(f_in) == 0:
            sys.exit("Trajectory {} not found. Be aware that PELE trajectories must contain the label \'trajectory\' in their file name to be detected".format("*trajectory*_{}".format(f_id)))
        f_in = f_in[0]
        with open(f_in, 'r') as input_file:
            file_content = input_file.read()
        trajectory_selected = re.search('MODEL\s+%d(.*?)ENDMDL' %int((step)/out_freq+1), file_content,re.DOTALL)

        # Output Trajectory
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


def parse_values(reports, criteria, min_value, max_value, steps):
    """

       Description: Parse the 'reports' and create a sorted array
       following the criteria chosen by the user.

    """

    INITIAL_DATA = [(PATH, []),
                    (REPORT, []),
                    (steps, []),
                    (criteria, [])
                    ]

    values = pd.DataFrame.from_items(INITIAL_DATA)
    for file in reports:
        report_number = os.path.basename(file).split("_")[-1]
        data = pd.read_csv(file, sep='    ', engine='python')
        report_values = data.loc[:, [steps, criteria]]
        report_values.insert(0, PATH, [file]*report_values[criteria].size)
        report_values.insert(1, REPORT, [report_number]*report_values[criteria].size)
        report_values = report_values[report_values[criteria].between(min_value, max_value, inclusive=True)]
        try:
            values = pd.concat([values, report_values])
        except ValueError:
            values = report_values
    values.sort_values(criteria, ascending=False)
    return values

def filter_non_numerical_folders(reports, numfolders):
    """
    Filter non numerical folders among
    the folders to parse
    """
    if(numfolders):
        new_reports = [report for report in reports if(os.path.basename(os.path.dirname(report)).isdigit())]
        return new_reports
    else:
        return reports

def get_column_names(reports, steps, criteria):
    data = pd.read_csv(reports[0], sep='    ', engine='python')
    data = list(data)
    if criteria.isdigit():
        return data[int(steps)-1], data[int(criteria)-1]
    else:
        return data[int(steps)-1]


if __name__ == "__main__":
    min, max, criteria, out_freq, output, numfolders = parse_args()
    main(min, max, criteria, out_freq, output, numfolders)
