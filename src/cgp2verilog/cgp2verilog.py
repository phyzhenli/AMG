import yaml
import argparse
from os.path import abspath, expanduser


def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("-cgp_yaml", type=str, required=True, help=f"cgp file in YAML format")
    parser.add_argument("-verilog_file", type=str, required=True, help=f"output verilog file")
    return parser.parse_args()

def gen_assignment(cell_ins: list, cell_type, f):
    if cell_type == '$_NOT_':
        print('~ ' + cell_ins[0] + ';', file=f)
    if cell_type == '$_BUF_':
        print(cell_ins[0] + ';', file=f)
    if cell_type == '$_AND_':
        print(cell_ins[0] + ' & ' + cell_ins[1] + ';', file=f)
    if cell_type == '$_NAND_':
        print('~ ( ' + cell_ins[0] + ' & ' + cell_ins[1] + ' );', file=f)
    if cell_type == '$_OR_':
        print(cell_ins[0] + ' | ' + cell_ins[1] + ';', file=f)
    if cell_type == '$_NOR_':
        print('~ ( ' + cell_ins[0] + ' | ' + cell_ins[1] + ' );', file=f)
    if cell_type == '$_XOR_':
        print(cell_ins[0] + ' ^ ' + cell_ins[1] + ';', file=f)
    if cell_type == '$_XNOR_':
        print('~ ( ' + cell_ins[0] + ' ^ ' + cell_ins[1] + ' );', file=f)
    if cell_type == '$_ANDNOT_':
        print(cell_ins[0] + ' & ( ~ ' + cell_ins[1] + ' );', file=f)
    if cell_type == '$_ORNOT_':
        print(cell_ins[0] + ' | ( ~ ' + cell_ins[1] + ' );', file=f)

def gen_verilog(cgp, verilog_file):
    with open(verilog_file, 'w') as f:
        print('module  ' + cgp['top'] + ' (', file=f)
        inputs_index_name = {}
        for input in cgp['inputs']:
            print('  input [' + str(input['width']-1) + ':0] ' + input['name'] + ',', file=f)
            for i in input['indexes']:
                inputs_index_name[i['index']] = i['name']

        outputs_index_name = {}
        for output in cgp['outputs']:
            print('  output [' + str(output['width']-1) + ':0] ' + output['name'] + ( '' if output == cgp['outputs'][-1] else ',' ), file=f)
            for o in output['indexes']:
                outputs_index_name[o['index']] = o['name']
        print(');', file=f)
        print(file=f)


        for cell in cgp['circuit']:
            if cell['type'] in ['$_NOT_', '$_BUF_', '$_AND_', '$_NAND_', '$_OR_', '$_NOR_', '$_XOR_', '$_XNOR_', '$_ANDNOT_', '$_ORNOT_']:
                print('  assign index_'+ str(cell['outputs'][0]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, cell['type'], f)

            if cell['type'] == 'eliminate':
                print(file=f)
                print('  // eliminate', file=f)
                for o in cell['outputs']:
                    print('  assign index_' + str(o) + ' = 1\'b0;', file=f)
            
            if cell['type'] == 'only AND sum':
                print(file=f)
                print('  // only AND sum', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = 1\'b0;', file=f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_AND_', f)

            if cell['type'] == 'only OR sum':
                print(file=f)
                print('  // only OR sum', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = 1\'b0;', file=f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_OR_', f)

            if cell['type'] == 'only XOR sum':
                print(file=f)
                print('  // only XOR sum', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = 1\'b0;', file=f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_XOR_', f)

            if cell['type'] == 'only AND carry':
                print(file=f)
                print('  // only AND carry', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_AND_', f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = 1\'b0;', file=f)

            if cell['type'] == 'only OR carry':
                print(file=f)
                print('  // only OR carry', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_OR_', f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = 1\'b0;', file=f)

            if cell['type'] == 'only XOR carry':
                print(file=f)
                print('  // only XOR carry', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_XOR_', f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = 1\'b0;', file=f)

            if cell['type'] == 'only A carry':
                print(file=f)
                print('  // only A carry', file=f)
                print('  assign index_' + str(cell['outputs'][0]) + ' = ', file=f, end='')
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                gen_assignment(cell_ins, '$_BUF_', f)
                print('  assign index_' + str(cell['outputs'][1]) + ' = 1\'b0;', file=f)
                

            if cell['type'] == '$ha':
                print(file=f)
                print('  // $ha', file=f)
                cell_ins = []
                for cell_input_index in cell['inputs']:
                    if cell_input_index in inputs_index_name:
                        cell_ins.append(inputs_index_name[cell_input_index])
                    else:
                        cell_ins.append('index_' + str(cell_input_index))
                print('  assign { index_' + str(cell['outputs'][0]) + ', index_' + str(cell['outputs'][1]) + ' } = ' + cell_ins[0] + ' + ' + cell_ins[1] + ';', file=f)

        print(file=f)
        for output in cgp['outputs']:
            for o in output['indexes']:
                print('  assign ' + o['name'] + ' = ', file=f, end='')
                if o['index'] in inputs_index_name:
                    print(inputs_index_name[o['index']] + ';', file=f)
                else:
                    print('index_' + str(o['index']) + ';', file=f)
        print(file=f)
        print('endmodule', file=f)

if __name__ == '__main__':

    args = get_args()
    cgp_yaml = abspath(expanduser(args.cgp_yaml))
    verilog_file = abspath(expanduser(args.verilog_file))

    with open(cgp_yaml, 'r') as f:
        cgp = yaml.safe_load(f)

    print(cgp)
    gen_verilog(cgp, verilog_file)