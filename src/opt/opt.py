import yaml
import subprocess
import argparse
from os.path import abspath, expanduser, basename
from hyperopt import hp, fmin, tpe, mix, rand, atpe, anneal, STATUS_OK, STATUS_FAIL, space_eval
from hyperopt.mongoexp import MongoTrials, Trials
from functools import partial
import copy
import re
import math

from cgp2verilog import gen_verilog
from run_vivado import create_tcl
from get_results import get_PDA

connect_string = "mongo://localhost:1234/foo_db/jobs"

def get_rval(trial):
    vals = trial["misc"]["vals"]
    rval = {}
    for k, v in list(vals.items()):
        if v:
            rval[k] = v[0]
    return rval

def objective(params, space, cgp, verilog_file, verilog_top_file, vivado_exe, mae_testbench_file, mse_testbench_file, connect_string):

    tmp_trials = MongoTrials(connect_string)
    for t in tmp_trials:
        if t['result']['status'] == STATUS_OK:
            if params == space_eval(space, get_rval(t)):
                return {
                    'status': STATUS_FAIL
                }

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

    # with open('test.yaml', 'w') as f:
    #     yaml.dump(cgp_deepcopy, f, default_flow_style=None, sort_keys=False, width=2147483647)

    verilog_file = basename(verilog_file)
    gen_verilog(cgp_deepcopy, verilog_file)

    bench_info = {}
    bench_info['out_dir'] = './'
    bench_info['top'] = basename(verilog_top_file).replace('.v','')
    bench_info['file(s)'] = [verilog_file, verilog_top_file]
    bench_info['type'] = 'combinational'
    subprocess.run(['mkdir', '-p', bench_info['top']])
    create_tcl(bench_info)
    subprocess.run([vivado_exe, '-nolog', '-nojournal', '-mode', 'batch', '-source', abspath(expanduser(bench_info['out_dir'])) + '/' + bench_info['top'] + '/run_vivado.tcl'], stdout=subprocess.DEVNULL)
    area, delay, slack, power = get_PDA('reports/')

    mae_subp_log = subprocess.run(['vcs', '-R', mae_testbench_file, verilog_top_file, verilog_file], stdout=subprocess.PIPE, text=True)
    for line in mae_subp_log.stdout.split('\n'):
        if line.startswith('MAE: '):
            mae = round( float( line.strip().split(' ')[-1] ) )
    mse_subp_log = subprocess.run(['vcs', '-R', mse_testbench_file, verilog_top_file, verilog_file], stdout=subprocess.PIPE, text=True)
    for line in mse_subp_log.stdout.split('\n'):
        if line.startswith('MSE: '):
            mse = round( float( line.strip().split(' ')[-1] ) )

    return {
            'loss': area*delay*power*(math.log(mae*mse,2)),
            'status': STATUS_OK,
            'area': area,
            'delay': delay,
            'slack': slack,
            'power': power,
            'mae': mae,
            'mse': mse
            }
    # return 0

def gen_space(cgp, bound_weight):
    space = {}
    for cell in cgp['circuit']:
        if cell['type'] == '$ha' and cell['weight'] <= bound_weight:
            space[str(cell['outputs'][1])] = hp.choice(str(cell['outputs'][1]), ['eliminate', 'only OR sum', 'only A carry', 'exact'])
            # space[str(cell['outputs'][1])] = hp.choice(str(cell['outputs'][1]), ['only A carry', 'exact'])
    return space

def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("-cgp_yaml", type=str, required=True, help="cgp yaml file")
    parser.add_argument("-opt_percent", type=float, required=True, help="HA percentage that will be optimized, range: (0,1]")
    parser.add_argument("-verilog_file", type=str, required=True, help=f"output verilog file")
    parser.add_argument("-verilog_top_file", type=str, required=True, help=f"verilog top file")
    parser.add_argument("-vivado_exe", type=str, required=True, help=f"vivado executable file")
    parser.add_argument("-mae_testbench_file", type=str, required=True, help=f"mean absolue error testbench file")
    parser.add_argument("-mse_testbench_file", type=str, required=True, help=f"mean square error testbench file")
    parser.add_argument("-parallel_number", type=int, required=False, default=1, help=f"parallel number, {default}")
    parser.add_argument("-same_trial_limit", type=int, required=False, default=1, help=f"exact same trials limit, {default}")
    return parser.parse_args()

if __name__ == '__main__':

    args = get_args()
    cgp_yaml = abspath(expanduser(args.cgp_yaml))
    opt_percent = args.opt_percent
    verilog_file = abspath(expanduser(args.verilog_file))
    verilog_top_file = abspath(expanduser(args.verilog_top_file))
    vivado_exe = args.vivado_exe
    mae_testbench_file = abspath(expanduser(args.mae_testbench_file))
    mse_testbench_file = abspath(expanduser(args.mse_testbench_file))
    parallel_number = args.parallel_number
    same_trial_limit = args.same_trial_limit

    with open(cgp_yaml, 'r') as f:
        cgp = yaml.safe_load(f)

    ha_weights = []
    for cell in cgp['circuit']:
        if cell['type'] == '$ha':
            ha_weights.append(cell['weight'])
    sorted_ha_weights = sorted(ha_weights)
    
    bound_weight = sorted_ha_weights[round(len(ha_weights)*opt_percent)-1]
    print(cgp)
    print(sorted_ha_weights)
    print("size: ", len(ha_weights))
    print("bound weight: ", bound_weight)
    exit()
    space = gen_space(cgp, bound_weight)
    trials = MongoTrials(connect_string)
    # trials = Trials()

    fmin(
        partial(objective, space=space, cgp=cgp, verilog_file=verilog_file, verilog_top_file=verilog_top_file, vivado_exe=vivado_exe, mae_testbench_file=mae_testbench_file, mse_testbench_file=mse_testbench_file, connect_string=connect_string),
        space=space,
        # algo=tpe.suggest,
        algo=partial(mix.suggest, p_suggest=[(0.4, rand.suggest), (0.6, tpe.suggest)]),
        # max_evals=1,
        trials=trials,
        # verbose=False,
        # return_argmin=True,
        max_queue_len=parallel_number
    )
