set_param general.maxThreads 1

set outputDir ./reports
file mkdir $outputDir

read_verilog <path_to_verilog_file>

synth_design -top ubit8x7_star -part xcvu3p-ffvc1517-3-e -flatten full
create_clock -period 10 -name VCLK
set_input_delay 0 -clock VCLK [all_inputs]
set_output_delay 0 -clock VCLK [all_outputs]

opt_design
place_design
phys_opt_design
route_design
report_power -file $outputDir/post_route_power.rpt
report_timing -file $outputDir/post_route_timing.rpt
report_utilization -file $outputDir/post_route_util.rpt
