from hyperopt import hp, space_eval, STATUS_OK, STATUS_FAIL
from hyperopt.mongoexp import MongoTrials
from opt import gen_space, connect_string, get_rval
import pandas as pd
import yaml
import argparse
import copy
from os.path import abspath, expanduser, basename
import subprocess
from cgp2verilog import gen_verilog


def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("-cgp_yaml", type=str, required=True, help="cgp yaml file")
    parser.add_argument("-opt_percent", type=float, required=True, help="HA percentage that will be optimized, range: (0,1]")
    parser.add_argument("-verilogs_dir", type=str, required=True, help="output verilog files directory")
    return parser.parse_args()

if __name__ == '__main__':

    args = get_args()
    cgp_yaml = args.cgp_yaml
    opt_percent = args.opt_percent
    verilogs_dir = args.verilogs_dir

    with open(cgp_yaml, 'r') as f:
        cgp = yaml.safe_load(f)

    ha_weights = []
    for cell in cgp['circuit']:
        if cell['type'] == '$ha':
            ha_weights.append(cell['weight'])
    sorted_ha_weights = sorted(ha_weights)
    bound_weight = sorted_ha_weights[round(len(ha_weights)*opt_percent)-1]

    trials = MongoTrials(connect_string)

    print('=== trials number: ', len(trials))
    print('=== best trial: ', trials.best_trial)
    # print(trials.trials[0]["result"]["loss"])
    
    candidates = [
        t
        for t in trials.trials
        if t["result"]["status"] == STATUS_OK
    ]
    print('=== candidates number: ', len(candidates))
    # exit()
    candidates.sort(key=lambda t: t["result"]["loss"])

    # find Pareto points
    pareto_set = []
    candidates.sort(key=lambda t: t["result"]["mae"]*t["result"]["mse"])
    while len(pareto_set) < 200:
        sub_set = []
        for c in candidates:
            c_PDA = c['result']['area']*c['result']['delay']*c['result']['power']
            append = True
            for p in sub_set:
                if c_PDA > p['result']['area']*p['result']['delay']*p['result']['power']:
                    append = False
                    break
            if append:
                sub_set.append(c)
                candidates.remove(c)
        pareto_set.extend(sub_set)

    print('=== pareto number: ', len(pareto_set))
    # exit()

    mae = pd.DataFrame()
    mse = pd.DataFrame()
    vivado_results = pd.DataFrame()
    topN = min(2000, len(pareto_set))
    for i in range(topN):
        name = 'unsigned_mul_8x8_vivado_opt_'+str(opt_percent).replace('.','p')+'_log_2_pareto_' + str(i).zfill(len(str(topN)))
        mae.loc[name, 'MAE'] = pareto_set[i]['result']['mae']
        mse.loc[name, 'MSE'] = pareto_set[i]['result']['mse']
        vivado_results.loc[name, 'CLB LUTs'] = pareto_set[i]['result']['area']
        vivado_results.loc[name, 'Data Path Delay (ns)'] = pareto_set[i]['result']['delay']
        vivado_results.loc[name, 'Slack (ns)'] = pareto_set[i]['result']['slack']
        vivado_results.loc[name, 'Total On-Chip Power (W)'] = pareto_set[i]['result']['power']

        params = space_eval(gen_space(cgp, bound_weight), get_rval(pareto_set[i]))
        cgp_deepcopy = copy.deepcopy(cgp)
        for cell in cgp_deepcopy['circuit']:
            if cell['type'] == '$ha':
                key = str(cell['outputs'][1])
                if key in params:
                    value = params[key]
                    # cell['comment'] = value
                    if value == 'eliminate':
                        cell['type'] = 'eliminate'
                        # cell['dangling_wires'] = cell['outputs']
                    if value == 'only OR sum':
                        cell['type'] = 'only OR sum'
                        # cell['dangling_wires'] = [ cell['outputs'][0] ]
                        # cell['outputs'].remove(cell['outputs'][0])
                    if value == 'only A carry':
                        cell['type'] = 'only A carry'
                        # cell['inputs'].remove(cell['inputs'][1])
                        # cell['dangling_wires'] = [ cell['outputs'][1] ]
                        # cell['outputs'].remove(cell['outputs'][1])
                    if value == 'exact':
                        pass
        cgp_deepcopy['top'] = name
        gen_verilog(cgp_deepcopy, verilogs_dir+'/'+name+'.v')
        subprocess.run(["sed -i '1i\\\\' " + verilogs_dir+'/'+name+'.v'], shell=True, stdout=subprocess.DEVNULL)
        subprocess.run(["sed -i '1i\\// MAE: " + str(pareto_set[i]['result']['mae']) + "' " + verilogs_dir+'/'+name+'.v'], shell=True, stdout=subprocess.DEVNULL)
        subprocess.run(["sed -i '1i\\// MSE: " + str(pareto_set[i]['result']['mse']) + "' " + verilogs_dir+'/'+name+'.v'], shell=True, stdout=subprocess.DEVNULL)
    mae.to_csv('MAE.csv')
    mse.to_csv('MSE.csv')
    vivado_results.to_csv('ours.csv')
