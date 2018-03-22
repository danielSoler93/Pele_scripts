import os
import sys
import re
import pandas as pd
import AdaptivePELE.adaptiveSampling as ads
from AdaptivePELE.constants import blockNames


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def parse(control_file, pele_file, adaptive=False):
    """
    Parse control_file and retrieve fields
    """
    cluster_object = None
    # control_file_dir = os.path.dirname(control_file)
    if adaptive:
        generalParams, spawningBlock, simulationrunnerBlock, clusteringBlock = ads.loadParams(control_file)
        path = generalParams[blockNames.GeneralParams.outputPath]
        last_epoch = simulationrunnerBlock["params"][blockNames.SimulationParams.iterations]
        cluster_object = os.path.join(str(last_epoch), "clustering/object.pkl")
        pele_control_file = simulationrunnerBlock["params"][blockNames.SimulationParams.templetizedControlFile]
        try:
            _, report_name, center, radius = parse_pele(pele_control_file)
        except IOError:
            pele_control_file = pele_file
            _, report_name, center, radius = parse_pele(pele_control_file)
        report = os.path.join(path, "{}/{}_1".format(0, report_name))
        metrics, steps = parse_report(report)
        return path, metrics, steps, cluster_object, center, radius
    else:
        path, report_name, center, radius = parse_pele(control_file)
        report = os.path.join(path, "{}_1".format(report_name))
        metrics, steps = parse_report(report)
        return path, metrics, steps, cluster_object, center, radius


def parse_pele(control_file):
    with open(control_file, "r") as f:
        for line in f:
            try:
                if re.search('"radius"\s*:\s*(.*),', line):
                    result = re.search('"radius"\s*:\s*(.*),', line)
                    radius = float(result.group(1))
                elif re.search('"radius"\s*:\s*(.*)}', line):
                    result = re.search('"radius"\s*:\s*(.*)}', line)
                    radius = float(result.group(1))
                if re.search('"fixedCenter"\s*:\s*\[(.*)\]', line):
                    result = re.search('"fixedCenter"\s*:\s*\[(.*)\]', line)
                    center = [float(coord) for coord in result.group(1).split(",")]

            except ValueError:
                print("No Box defined setting equilibrium format")
                center = None
                radius = None
            if re.search('"reportPath"\s*:\s*"(.*)"', line):
                result = re.search('"reportPath"\s*:\s*"(.*)"', line)
                path, report_name = result.group(1).rsplit("/", 1)
        return path, report_name, center, radius


def parse_report(report):
    data = pd.read_csv(report, sep='    ', engine='python')
    metrics = list(data)
    return metrics[3:], metrics[2]


if __name__ == "__main__":
    parse(sys.argv[1], adaptive=True)
