from hyperopt import hp, space_eval, STATUS_OK, STATUS_FAIL
from hyperopt.mongoexp import MongoTrials
from opt import gen_space, connect_string
import pandas as pd

if __name__ == '__main__':

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
        name = 'unsigned_mul_8x8_vivado_opt_0p5_' + str(i).zfill(len(str(topN)))
        mae.loc[name, 'MAE'] = pareto_set[i]['result']['mae']
        mse.loc[name, 'MSE'] = pareto_set[i]['result']['mse']
        vivado_results.loc[name, 'CLB LUTs'] = pareto_set[i]['result']['area']
        vivado_results.loc[name, 'Data Path Delay (ns)'] = pareto_set[i]['result']['delay']
        vivado_results.loc[name, 'Slack (ns)'] = pareto_set[i]['result']['slack']
        vivado_results.loc[name, 'Total On-Chip Power (W)'] = pareto_set[i]['result']['power']
    mae.to_csv('MAE.csv')
    mse.to_csv('MSE.csv')
    vivado_results.to_csv('ours.csv')
        
