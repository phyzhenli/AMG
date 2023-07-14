
import yaml
import argparse
from os.path import abspath, expanduser
import os
import pandas as pd
import numpy as np

def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("-benchs_info_file", type=str, required=True, help=f"benchmarks infomation file, YAML format")
    parser.add_argument("-outputs_dir", type=str, required=True, help=f"outputs directory")
    parser.add_argument("-csv_filename", type=str, required=True, help=f"csv filename")
    return parser.parse_args()


def get_PDA(rpt_dir):
    area = delay = slack = power = np.nan
    with open(rpt_dir + '/' + 'post_route_util.rpt', 'r') as f:
        area_rpt = f.readlines()
        for line in area_rpt:
            if 'CLB LUTs' in line:
                area = float(line.split()[4])
    with open(rpt_dir + '/' + 'post_route_timing.rpt', 'r') as f:
        delay_rpt = f.readlines()
        for line in delay_rpt:
            if 'Data Path Delay' in line:
                delay = float(line.split()[3].replace('ns',''))
            if 'Slack (MET)' in line:
                slack = float(line.split()[3].replace('ns',''))
    with open(rpt_dir + '/' + 'post_route_power.rpt', 'r') as f:
        power_rpt = f.readlines()
        for line in power_rpt:
            if 'Total On-Chip Power' in line:
                power = float(line.split()[6])
    return area, delay, slack, power

if __name__ == '__main__':

    args = get_args()

    with open(args.benchs_info_file, 'r') as benchs_info_f:
        benchs_info = yaml.safe_load(benchs_info_f)

    outputs_dir = abspath(expanduser(args.outputs_dir))
    result_df = pd.DataFrame()

    not_finish = 0
    for bench_info in benchs_info:
        if 'comment' not in bench_info:
            work_dir = outputs_dir + '/../' + bench_info['out_dir'] + '/' + bench_info['top']
            print(work_dir)
            if (os.path.exists(work_dir + '/reports/' + 'post_route_util.rpt')):
                area, delay, slack, power = get_PDA(work_dir + '/reports/')
                # continue
            else:
                area = delay = slack = power = np.nan
                not_finish += 1
            index = bench_info['out_dir'] + '/' + bench_info['top']
            result_df.loc[index, 'CLB LUTs'] = area
            result_df.loc[index, 'Data Path Delay (ns)'] = delay
            result_df.loc[index, 'Slack (ns)'] = slack
            result_df.loc[index, 'Total On-Chip Power (W)'] = power
            # exit()
    print(result_df)
    print("N/A number: ", not_finish)
    result_df.to_csv(args.csv_filename)