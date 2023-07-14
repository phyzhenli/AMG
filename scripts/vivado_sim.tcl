set_param general.maxThreads 1

create_project -force project_1 project_1 -part xcvu3p-ffvc1517-3-e
add_files -norecurse <path_to_verilog_file>
# add_files -norecurse <path_to_verilog_file>
add_files -fileset sim_1 -norecurse <path_to_testbench_file>
import_files -force -norecurse
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1
launch_simulation
run all
