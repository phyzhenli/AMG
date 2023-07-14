import argparse
import subprocess
import yaml
from os.path import abspath, expanduser
import time

def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("-benchs_info_file", type=str, required=True, help=f"benchmarks infomation file, YAML format")
    parser.add_argument("-vivado_exe", type=str, required=True, help=f"vivado executable file")
    parser.add_argument("-process", type=int, default=1, required=False, help=f"parallel number, {default}")
    parser.add_argument("-memory", type=int, default=10000, required=False, help=f"memory limit in MB, {default}")
    return parser.parse_args()

def create_tcl(bench_info):
    with open(abspath(expanduser(bench_info['out_dir'])) + '/' + bench_info['top'] + '/run_vivado.tcl', 'w') as f:
        print('set_param general.maxThreads 1', file=f)
        print(file=f)
        print('set outputDir ./reports', file=f)
        print('file mkdir $outputDir', file=f)
        print(file=f)
        for file in bench_info['file(s)']:
            if file.endswith('.v'):
                print('read_verilog ' + abspath(expanduser(file)), file=f)
            if file.endswith('.vhd'):
                print('read_vhdl ' + abspath(expanduser(file)), file=f)
        print(file=f)
        print('synth_design -top ' + bench_info['top'] + ' -part xcvu3p-ffvc1517-3-e -flatten full', file=f)
        print('create_clock -period 10 -name VCLK', file=f)
        print('set_input_delay 0 -clock VCLK [all_inputs]', file=f)
        print('set_output_delay 0 -clock VCLK [all_outputs]', file=f)
        print(file=f)
        print('opt_design',file =f)
        print('place_design', file=f)
        print('phys_opt_design', file=f)
        print('route_design', file=f)
        print('report_power -file $outputDir/post_route_power.rpt', file=f)
        print('report_timing -file $outputDir/post_route_timing.rpt', file=f)
        print('report_utilization -file $outputDir/post_route_util.rpt', file=f)
        # print('write_verilog -force $outputDir/post_route_netlist.v', file=f)
        
if __name__ == '__main__':
    args = get_args()
    benchs_info_file = args.benchs_info_file
    vivado_exe = args.vivado_exe
    process = args.process
    memory = args.memory

    with open(args.benchs_info_file, 'r') as f:
        benchs_info = yaml.safe_load(f)

    for bench_info in benchs_info:
        if 'comment' not in bench_info:
            work_dir = abspath(expanduser(bench_info['out_dir'])) + '/' + bench_info['top']
            subprocess.run(['mkdir', '-p', work_dir])

            create_tcl(bench_info)

            cmd=vivado_exe + ' -nolog -nojournal -mode batch -source run_vivado.tcl'
            while True:
                num_jobs = len( subprocess.check_output(['bjobs']).splitlines() ) - 1
                print('== process : ', process)
                print('== run jobs: ', num_jobs)
                if num_jobs < process:
                    subprocess.run(['bsub', '-o', work_dir+'/bsub.log', '-R', 'rusage[mem=' + str(memory) + ']', cmd], stdout=subprocess.DEVNULL, cwd=work_dir)
                    print(bench_info['top'])
                    print()
                    time.sleep(1)
                    break
                else:
                    print('Waiting ....... ')
                    time.sleep(1)