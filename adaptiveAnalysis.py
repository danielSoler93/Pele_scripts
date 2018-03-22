import argparse
import os
import glob
from Analysis_tools import numberOfClusters, writeClusteringStructures, \
    box, bestStructs, bactrackAdaptiveTrajectory, plotSpawningClusters
import Utilities.utils as ut

ANALYSIS_FOLDER = "analysis"
OUTPUT_CLUSTER = os.path.join(ANALYSIS_FOLDER, "clustering")
SPAWNING_FILENAME = os.path.join(OUTPUT_CLUSTER, "spawning")
CLUSTER_FILENAME = "clustersNumber"
OUTPUT_CLUSTER_STRUCTS = os.path.join(OUTPUT_CLUSTER, "clusterStructs/cluster.pdb")
BOX_FILE = os.path.join(ANALYSIS_FOLDER, "box.pdb")
METRICS_FOLDER = os.path.join(ANALYSIS_FOLDER, "metrics")


def parse_args():
    parser = argparse.ArgumentParser(description='Run PELE analysis')
    parser.add_argument('control_file', type=str, help='Control_file from the job to analyze. Use -a flag if it is an adaptive job.')
    parser.add_argument('--adaptive', "-a", action='store_true', help='Analyze Adaptive PELE')
    args = parser.parse_args()

    return args.control_file, args.adaptive


def main(control_file, adaptive=False):

    path, metrics, step_column, cluster_object, center, radius = ut.parse(control_file, adaptive=adaptive)
    with ut.cd(path):
        if adaptive:
            numberOfClusters.main(CLUSTER_FILENAME, OUTPUT_CLUSTER)
            plotSpawningClusters.main(SPAWNING_FILENAME)
            try:
                writeClusteringStructures.main(cluster_object, None, None, OUTPUT_CLUSTER_STRUCTS)
            except IOError:
                epochs_folder = glob.glob("*/")
                numerical_folder = [int(os.path.basename(os.path.normpath(folder))) for folder in epochs_folder if os.path.basename(os.path.normpath(folder)).isdigit()]
                last_epoch = str(max(numerical_folder))
                cluster_object = os.path.abspath(os.path.join(last_epoch, "clustering/object.pkl"))
                try:
                    writeClusteringStructures.main(cluster_object, None, None, OUTPUT_CLUSTER_STRUCTS)
                except IOError:
                    raise IOError("Non clustering file found in last epoch. Adaptive did not finish properly")
        if center and radius:
            box.build_box(center, radius, file=BOX_FILE)
        for metric in metrics:
            print("Extracting best {} structures".format(metric))
            metric_folder = os.path.join(METRICS_FOLDER, metric.replace(" ", ""))
            if adaptive:
                files, epochs, trajs, steps = bestStructs.main(metric, path=os.getcwd(), output=metric_folder, steps=step_column, numfolders=True)
                for _, epoch, traj, step in zip(files, epochs, trajs, steps):
                    traj_name = "epoch{}_traj{}_pathway.pdb".format(epoch, traj)
                    bactrackAdaptiveTrajectory.main(int(traj), int(step), epoch, metric_folder, traj_name)
            else:
                files, epochs, trajs, steps = bestStructs.main(metric, path=os.getcwd(), output=metric_folder, steps=step_column, numfolders=False)

if __name__ == "__main__":
    control_file, is_adaptive = parse_args()
    main(control_file, is_adaptive)
