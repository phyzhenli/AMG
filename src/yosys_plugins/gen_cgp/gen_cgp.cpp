#include "kernel/register.h"
#include "kernel/sigtools.h"
#include "kernel/celltypes.h"
#include "kernel/ffinit.h"
#include "kernel/ff.h"
#include "kernel/log.h"
#include "backends/rtlil/rtlil_backend.h"
#include <numeric>

USING_YOSYS_NAMESPACE
PRIVATE_NAMESPACE_BEGIN

const std::string str(const RTLIL::SigBit &sig)
{
    std::string str = RTLIL::unescape_id(sig.wire->name);
    for (size_t i = 0; i < str.size(); i++)
        if (str[i] == '#' || str[i] == '=' || str[i] == '<' || str[i] == '>')
            str[i] = '?';

    if (sig.wire->width != 1)
        str += stringf("[%d]", sig.wire->upto ? sig.wire->start_offset + sig.wire->width - sig.offset - 1 : sig.wire->start_offset + sig.offset);

    return str;
}

bool done(const dict<RTLIL::Cell*, bool> cell_flag)
{
    for (auto &it : cell_flag)
        if (it.second == false)
            return false;
    return true;
}

struct gen_cgpPass : public Pass
{
    gen_cgpPass() : Pass("gen_cgp", "generate Cartesian Genetic Programming configuration to YAML file") {}
    void help() override
    {
        log("\n");
        log("    gen_cgp [filename]\n");
        log("\n");
        log("This pass generate Cartesian Genetic Programming configuration of the current gate-level circuit_cgp. Do this after techmap.\n");
        log("\n");
    }
    void execute(std::vector<std::string> args, RTLIL::Design *design) override
    {
        log_header(design, "Generating Cartesian Genetic Programming configuration.\n\n");
        log_assert(design->selected_modules().size() == 1);
        RTLIL::Module *module = design->selected_modules()[0];

        dict<RTLIL::Cell*, bool> cell_flag;
                for (auto cell : module->cells())
            cell_flag[cell] = false;

        SigMap sigmap(module);
        dict<RTLIL::SigBit, int> visited_sigbits;
        dict<RTLIL::SigBit, int> sigbit_weight;
        int index = 0;
        for (auto wire : module->wires())
            if (wire->port_input)
                for (int i = 0; i < wire->width; i++) {
                    visited_sigbits[sigmap(RTLIL::SigBit(wire, i))] = index;
                    index++;
                    sigbit_weight[sigmap(RTLIL::SigBit(wire, i))] = i;
                }
        // int number_inputs = index;

        dict<RTLIL::SigBit, RTLIL::Cell*> sigbit_to_driver_index;
        for (auto cell : module->cells())
            for (auto &conn : cell->connections())
                if (cell->output(conn.first)) {
                    log_assert(conn.second.size() == 1);
                    const RTLIL::SigBit bit = sigmap(conn.second);
                    sigbit_to_driver_index[bit] = cell;
                }
        
        std::vector<RTLIL::Cell*> cells_in_seq;
        dict<RTLIL::Cell*, std::vector<int>> cell_weights;

        while (!done(cell_flag)) {
            for (auto cell : module->cells()) {
                if (!cell_flag[cell]) {
                    bool legal = true;
                    for (auto &conn : cell->connections())
                        if (cell->input(conn.first)) {
                            log_assert(conn.second.size() == 1);
                            const RTLIL::SigBit sigb = sigmap(conn.second);
                            if (!visited_sigbits.count(sigb) && !conn.second.is_fully_zero())
                                legal = false;
                        }
                    if (legal) {
                        for (auto &conn : cell->connections()) {
                            log_assert(conn.second.size() == 1);
                            const RTLIL::SigBit sigb = sigmap(conn.second);
                            if (cell->input(conn.first)) {
                                cell_weights[cell].push_back( sigbit_weight[sigb] );
                            }
                            if (cell->output(conn.first)) {
                                visited_sigbits[sigb] = index;
                                index++;
                                if ( cell->type == ID($_AND_) ) {
                                    log_assert(cell_weights[cell].size() == 2);
                                    sigbit_weight[sigb] = cell_weights[cell][0] + cell_weights[cell][1];
                                }
                                // if ( cell->type == "\\HA" ) {
                                //     log_assert(cell_weights[cell].size() == 2);
                                //     if (conn.first == "\\C")
                                //         sigbit_weight[sigb] = ( cell_weights[cell][0] + cell_weights[cell][1] ) / 2 + 1;
                                //     if (conn.first == "\\S")
                                //         sigbit_weight[sigb] = ( cell_weights[cell][0] + cell_weights[cell][1] ) / 2;
                                // }
                            }
                        }
                        cells_in_seq.push_back(cell);
                        cell_flag[cell] = true;
                    }
                }
            }
            // break;
        }

        if (args.size() == 2)
        {
            std::string filename = args[1];
            
            if (filename.substr(filename.find_last_of(".") + 1) != "yaml")
                log_cmd_error("%s is not a valid filename!\n", filename.c_str());

            FILE *f = fopen(filename.c_str(), "w");

            fprintf(f, "top: %s\n", RTLIL::unescape_id(module->name).c_str());

            fprintf(f, "\n");

            fprintf(f, "inputs:\n");
            for (auto wire : module->wires())
                if (wire->port_input) {
                    fprintf(f, "  - name: %s\n", RTLIL::unescape_id(wire->name).c_str());
                    fprintf(f, "    width: %d\n", wire->width);
                    fprintf(f, "    indexes:\n");
                    for (int i = 0; i < wire->width; i++) {
                        fprintf(f, "      - name: %s\n", str(RTLIL::SigBit(wire, i)).c_str());
                        fprintf(f, "        index: %d\n", visited_sigbits[sigmap(RTLIL::SigBit(wire, i))]);
                    }
                }
            fprintf(f, "\n");
            fprintf(f, "outputs:\n");
            for (auto wire : module->wires())
                if (wire->port_output) {
                    fprintf(f, "  - name: %s\n", RTLIL::unescape_id(wire->name).c_str());
                    fprintf(f, "    width: %d\n", wire->width);
                    fprintf(f, "    indexes:\n");
                    for (int i = 0; i < wire->width; i++) {
                        fprintf(f, "      - name: %s\n", str(RTLIL::SigBit(wire, i)).c_str());
                        fprintf(f, "        index: %d\n", visited_sigbits[sigmap(RTLIL::SigBit(wire, i))]);
                    }
                }
            fprintf(f, "\n");
            fprintf(f, "circuit:\n");
            for(auto &cell : cells_in_seq) {
                if (cell->type == "\\HA")
                    fprintf(f, "  - type: $ha\n");
                else
                    fprintf(f, "  - type: %s\n", (cell->type).c_str());

                fprintf(f, "    inputs: [");
                std::vector<int> cell_inputs;
                for (auto &conn : cell->connections()) {
                    if (cell->input(conn.first)) {
                        log_assert(conn.second.size() == 1);
                        if (!conn.second.is_fully_zero())
                            cell_inputs.push_back(visited_sigbits[sigmap(conn.second)]);
                    }
                }
                for (size_t i = 0; i < cell_inputs.size(); i++)
                    if (i == 0)
                        fprintf(f, "%d", cell_inputs[i]);
                    else
                        fprintf(f, ",%d", cell_inputs[i]);
                fprintf(f, "]\n");

                fprintf(f, "    outputs: [");
                std::vector<int> cell_outputs;
                for (auto &conn : cell->connections()) {
                    if (cell->output(conn.first)) {
                        log_assert(conn.second.size() == 1);
                        cell_outputs.push_back(visited_sigbits[sigmap(conn.second)]);
                    }
                }
                for (size_t i = 0; i < cell_outputs.size(); i++)
                    if (i == 0)
                        fprintf(f, "%d", cell_outputs[i]);
                    else
                        fprintf(f, ",%d", cell_outputs[i]);
                fprintf(f, "]\n");

                if (!cell_weights[cell].empty()) {
                    fprintf(f, "    weight: ");
                    int sum_weights = 0;
                    for (auto &w : cell_weights[cell])
                        sum_weights += w;
                    if (cell->type == ID($_AND_))
                        fprintf(f, "%d\n", sum_weights);
                    if (cell->type == "\\HA")
                        fprintf(f, "%d\n", sum_weights / int( cell_weights[cell].size() ) );
                }
                fprintf(f, "\n");
            }
            fclose(f);
        }
    }
} gen_cgpPass;

PRIVATE_NAMESPACE_END

