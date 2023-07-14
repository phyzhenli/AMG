import argparse


def get_args():
    default = '(default: %(default)s)'
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=['unsigned', 'signed'], help="unsigned or signed multiplier")
    parser.add_argument("-x_width", type=int, required=True, help=f"operand x width")
    parser.add_argument("-y_width", type=int, required=True, help=f"operand y width")
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()
    mode = args.mode
    x_width = args.x_width
    y_width = args.y_width

    pp_number = x_width
    pp_width = y_width

    ha_array_top = mode + '_' + str(x_width) + 'x' + str(y_width) + '_mul_ha_array'
    ha_array_number = int(pp_number/2) if int(pp_number%2) == 0 else int( (pp_number-1)/2 )
    with open(ha_array_top + '.v', 'w') as f:
        print('module ' +  ha_array_top + ' (', file=f)
        print('  input [' + str(x_width-1) + ':0] x,', file=f )
        print('  input [' + str(y_width-1) + ':0] y,', file=f )

        ha_array_top_width = y_width + 1
        ha_array_bot_width = y_width - 1
        for i in range(ha_array_number):
            print('  output [' + str(ha_array_top_width-1) + ':0] ha_array_' + str(i) + '_t,', file=f )
            print('  output [' + str(ha_array_bot_width-1) + ':0] ha_array_' + str(i) + '_b' + (',' if i != ha_array_number - 1 else ''), file=f )

        print(');', file=f)
        print(file=f)

        for i in range(pp_number):
            print('  wire [' + str(pp_width-1) + ':0] pp' + str(i) + ' = y & {' + str(y_width) + '{x[' + str(i) + ']}};', file=f )
        print(file=f)

        for i in range(ha_array_number):
            t_pp_index = i * 2
            b_pp_index = t_pp_index + 1
            for j in range(pp_width):
                if j == 0:
                    print('  assign ha_array_' + str(i) + '_t[0] = pp' + str(t_pp_index) + '[0];', file=f)
                    print('  assign ha_array_' + str(i) + '_b[' + str(ha_array_bot_width-1) + '] = pp' + str(b_pp_index) + '[' + str(pp_width-1) + '];', file=f)
                elif j == pp_width - 1:
                    print('  HA U_pp' + str(t_pp_index) + '_' + str(j) + '_pp' + str(b_pp_index) + '_' + str(j-1) + ' (.A(pp' + str(t_pp_index) + '[' + str(j) + ']), .B(pp' + str(b_pp_index) + '[' + str(j-1) + ']), .C(ha_array_' + str(i) + '_t[' + str(j+1) + ']), .S(ha_array_' + str(i) + '_t[' + str(j) + ']) );', file=f)
                else:
                    print('  HA U_pp' + str(t_pp_index) + '_' + str(j) + '_pp' + str(b_pp_index) + '_' + str(j-1) + ' (.A(pp' + str(t_pp_index) + '[' + str(j) + ']), .B(pp' + str(b_pp_index) + '[' + str(j-1) + ']), .C(ha_array_' + str(i) + '_b[' + str(j-1) + ']), .S(ha_array_' + str(i) + '_t[' + str(j) + ']) );', file=f)
            print(file=f)

        print('endmodule', file=f)

    mul_top = mode + '_' + str(x_width) + 'x' + str(y_width) + '_mul_top'
    with open(mul_top + '.v', 'w') as f:
        print('module ' +  mul_top + ' (', file=f)
        print('  input [' + str(x_width-1) + ':0] x,', file=f )
        print('  input [' + str(y_width-1) + ':0] y,', file=f )
        print('  output [' + str(x_width+y_width-1) + ':0] z', file=f )
        print(');', file=f)
        print(file=f)

        ha_array_top_width = y_width + 1
        ha_array_bot_width = y_width - 1
        for i in range(ha_array_number):
            print('  wire [' + str(ha_array_top_width-1) + ':0] ha_array_' + str(i) + '_t;', file=f )
            print('  wire [' + str(ha_array_bot_width-1) + ':0] ha_array_' + str(i) + '_b;', file=f )
        if pp_number % 2 != 0:
            print('  wire [' + str(pp_width-1) + ':0] pp' + str(pp_number-1) + ' = y & {' + str(y_width) + '{x[' + str(x_width-1) + ']}};', file=f )
        print(file=f)

        print('  ' + ha_array_top + ' U_ha_array ( .x(x), .y(y)', file=f, end='')
        for i in range(ha_array_number):
            print(', .ha_array_' + str(i) + '_t(' + 'ha_array_' + str(i) + '_t)' + 
                  ', .ha_array_' + str(i) + '_b(' + 'ha_array_' + str(i) + '_b)', file=f, end='')
        print(' );', file=f)
        print(file=f)

        print('  assign z = ', file=f, end='')
        if pp_number % 2 != 0:
                print('{ pp' + str(pp_number-1) + ', ' + str(pp_number-1) + '\'b0 } + ', file=f, end='')
        for i in range(ha_array_number):
            ha_top_shift_number = i * 2
            ha_bot_shift_number = i * 2 + 2
            if i == 0:
                print('{ ha_array_' + str(i) + '_t } + ', file=f, end='')
            else:
                print('{ ha_array_' + str(i) + '_t, ' + str(ha_top_shift_number) + '\'b0 } + ', file=f, end='')
            print('{ ha_array_' + str(i) + '_b, ' + str(ha_bot_shift_number) + '\'b0 }' + (' + ' if i != ha_array_number - 1 else ''), file=f, end='')
        print(';', file=f)
        print(file=f)

        print('endmodule', file=f)
        print(file=f)

        print('module HA (', file=f)
        print('  input A,', file=f)
        print('  input B,', file=f)
        print('  output C,', file=f)
        print('  output S', file=f)
        print(');', file=f)
        print(file=f)

        # print('  assign S = A ^ B;', file=f)
        # print('  assign C = A & B;', file=f)
        print('  assign { C, S } = A + B;', file=f)
        print(file=f)
        print('endmodule', file=f)