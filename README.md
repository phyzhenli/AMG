# Automated Efficient FPGA-Based Approximate Multipliers Generator via Black Box Optimization

## Contents:
- src: the codes of the generator.
- multipliers: Verilog models of open-source/reproduced multipliers and our generated multipliers with unsigend 8x8.
- scripts: scripts for vivado.

## src
#### Dependencies
- Python 3.9.7 (Maybe other versions also work)
- [Yosys](https://github.com/YosysHQ/yosys)
- [Hyperopt](https://github.com/hyperopt/hyperopt)
- [MongoDB](http://hyperopt.github.io/hyperopt/scaleout/mongodb/) (Attention for version compatibility, verified version: MongoDB 4.4.22 for pymongo 3.12.0)
- [Vivado 2023.1](https://www.xilinx.com/support/download.html)
- Synopsys VCS

#### How to run
After solving the dependencies, open terminal and follow the steps:

Step-0: compile `yosys_plugins/gen_cgp/gen_cgp.cpp`:
```
cd yosys_plugins/gen_cgp
yosys-config --build gen_cgp.so gen_cgp.cpp
cd ../../
```

Step-1: run `gen_ha_multiplier/gen_ha_multiplier.py` to generate `*_ha_array.v` and `*_mul_top.v`, for example:
```
cd gen_ha_multiplier
python3 gen_ha_multiplier.py unsigned -x_width 8 -y_width 8
cd ../
```

Step-2: translate `*_ha_array.v` to YAML file through yosys plugin gen_cgp.so, for example:
```
cd yosys_plugins/gen_cgp
yosys -Q -T -m gen_cgp.so -p "read_verilog \
../../gen_ha_multiplier/unsigned_8x8_mul_ha_array.v \
../../gen_ha_multiplier/ha_blackbox.v; \
techmap; opt -purge; \
gen_cgp mul.yaml"
cd ../../
```
Rename `mul.yaml` as needed.

- Step-3: run `opt.py` to search approximate multipliers:
```
cd opt
export PYTHONPATH=../cgp2verilog:../run_vivado:../get_results
python3 opt.py \
-cgp_yaml <path_to_YAML_file> \
-opt_percent <desired_HA_opt_percent> \
-verilog_file <desired_verilog_filename> \
-verilog_top_file <path_to_top_verilog_file> \
-vivado_exe <path_to_vivado> \
-mae_testbench_file <path_to_mae_testbench> \
-mse_testbench_file <path_to_mse_testbench>
cd ../
```
for example:
```
python3 opt.py \
-cgp_yaml ../yosys_plugins/gen_cgp/unsigned_8x8_mul_ha_array.yaml \
-opt_percent 0.5 \
-verilog_file unsigned_8x8_mul_ha_array.v \
-verilog_top_file ../gen_ha_multiplier/unsigned_8x8_mul_top.v \
-vivado_exe vivado \
-mae_testbench_file ../gen_lut/ubit8x8_calc_mae_tb.v \
-mse_testbench_file ../gen_lut/ubit8x8_calc_mse_tb.v
```

- Step-4: run `get_mongo_results.py` to get multipliers:
```
cd opt
python3 get_mongo_results.py
cd ../
```

## multipliers

### open source

- [EvoApprox8b](http://www.fit.vutbr.cz/research/groups/ehw/approxlib/)

<!--- [EvoApprox8b](http://www.fit.vutbr.cz/research/groups/ehw/approxlib/) is a library that contains 500 Pareto optimal 8-bit approximate multipliers evolved by a multi-objective Cartesian Genetic Programming (CGP). The library provides Verilog, Matlab, and C models of all approximate circuits. -->
[//]: # (In addition to standard circuit parameters, circuit error is given for seven different error metrics.)

V. Mrazek, R. Hrbacek, Z. Vasicek and L. Sekanina, "EvoApprox8b:  Library of Approximate Adders and Multipliers for Circuit Design and Benchmarking of Approximation Methods," Design, Automation & Test in Europe Conference & Exhibition (DATE), 2017, 2017, pp. 258-261, doi: 10.23919/DATE.2017.7926993.

- [EvoApproxLib<sup>LITE</sup>](https://ehw.fit.vutbr.cz/evoapproxlib/)

<!--- [EvoApproxLib<sup>LITE</sup>](https://ehw.fit.vutbr.cz/evoapproxlib/) is a lightweight library of approximate circuits with formally guaranteed error parameters based on [EvoApprox8b](http://www.fit.vutbr.cz/research/groups/ehw/approxlib/). Hardware as well as software models are provided for each circuit. -->

V. Mrazek, Z. Vasicek, L. Sekanina, H. Jiang and J. Han, "Scalable Construction of Approximate Multipliers With Formally Guaranteed Worst Case Error," in IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 26, no. 11, pp. 2572-2576, Nov. 2018, doi: 10.1109/TVLSI.2018.2856362.

- DRUM

S. Hashemi, R. I. Bahar and S. Reda, "DRUM: A Dynamic Range Unbiased Multiplier for approximate applications," 2015 IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 2015, pp. 418-425, doi: 10.1109/ICCAD.2015.7372600.

<!-- Available at: https://github.com/scale-lab/DRUM and https://github.com/phyzhenli/DRUM. -->

- FPT2022

S. Yao and L. Zhang, "Hardware-Efficient FPGA-Based Approximate Multipliers for Error-Tolerant Computing," 2022 International Conference on Field-Programmable Technology (ICFPT), Hong Kong, 2022, pp. 1-8, doi: 10.1109/ICFPT56656.2022.9974399.

### reproduced unsigned 8x8 multipliers

- AC

<!--- AC is a multiplier with two approximate 4-2 compressors. -->

<!-- A. Momeni, J. Han, P. Montuschi and F. Lombardi, "Design and Analysis of Approximate Compressors for Multiplication," in IEEE Transactions on Computers, vol. 64, no. 4, pp. 984-994, April 2015, doi: 10.1109/TC.2014.2308214. -->
S. Venkatachalam and S. -B. Ko, "Design of Power and Area Efficient Approximate Multipliers," in IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 25, no. 5, pp. 1782-1786, May 2017, doi: 10.1109/TVLSI.2016.2643639.

- CR

<!--- CR leverages a newly-designed approximate adder that limits its carry propagation to the nearest neighbors for fast partial product accumulation. Different levels of accuracy can be achieved through a configurable error recovery by using different numbers of most significant bits (MSBs) for error reduction. -->

C. Liu, J. Han and F. Lombardi, "A low-power, high-performance approximate multiplier with configurable partial error recovery," 2014 Design, Automation & Test in Europe Conference & Exhibition (DATE), 2014, pp. 1-4, doi: 10.7873/DATE.2014.108.

- KMap

<!--- KMap is a multiplier architecture with tunable error characteristics, that leverages a modified inaccurate 2×2 building block. -->

P. Kulkarni, P. Gupta and M. Ercegovac, "Trading Accuracy for Power with an Underdesigned Multiplier Architecture," 2011 24th International Conference on VLSI Design, 2011, pp. 346-351, doi: 10.1109/VLSID.2011.51.

- OU

<!--- OU is an approximate and unbiased floating-point multiplier, which is mathematically proved optimal in terms of square error for the given bases of the space {1, x, y, x<sub>2</sub>, y<sub>2</sub>}. We use the method to generate integer multipliers. -->

C. Chen, S. Yang, W. Qian, M. Imani, X. Yin and C. Zhuo, "Optimally Approximated and Unbiased Floating-Point Multiplier with Runtime Configurability," 2020 IEEE/ACM International Conference On Computer Aided Design (ICCAD), 2020, pp. 1-9.

- RoBA

<!--- RoBA is a multiplier that rounds the operands to the nearest exponent of two. -->

R. Zendegani, M. Kamal, M. Bahadori, A. Afzali-Kusha and M. Pedram, "RoBA Multiplier: A Rounding-Based Approximate Multiplier for High-Speed yet Energy-Efficient Digital Signal Processing," in IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 25, no. 2, pp. 393-401, Feb. 2017, doi: 10.1109/TVLSI.2016.2587696.

- SDLC

<!--- SDLC is an energy-efficient approximate multiplier design using a significance-driven logic compression approach. Fundamental to this approach is an algorithmic and configurable lossy compression of the partial product rows based on their progressive bit significance. -->

I. Qiqieh, R. Shafik, G. Tarawneh, D. Sokolov and A. Yakovlev, "Energy-efficient approximate multiplier design using bit significance-driven logic compression," Design, Automation & Test in Europe Conference & Exhibition (DATE), 2017, 2017, pp. 7-12, doi: 10.23919/DATE.2017.7926950.

I. Haddadi, I. Qiqieh, R. Shafik, F. Xia, M. Al-hayanni and A. Yakovlev, "Run-time Configurable Approximate Multiplier using Significance-Driven Logic Compression," 2021 IEEE 39th International Conference on Computer Design (ICCD), 2021, pp. 117-124, doi: 10.1109/ICCD53106.2021.00029.

- TOSAM

S. Vahdat, M. Kamal, A. Afzali-Kusha and M. Pedram, "TOSAM: An Energy-Efficient Truncation- and Rounding-Based Scalable Approximate Multiplier," in IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 27, no. 5, pp. 1161-1173, May 2019, doi: 10.1109/TVLSI.2018.2890712.

- PPAM

G. Zervakis, K. Tsoumanis, S. Xydis, D. Soudris and K. Pekmestzi, "Design-Efficient Approximate Multiplication Circuits Through Partial Product Perforation," in IEEE Transactions on Very Large Scale Integration (VLSI) Systems, vol. 24, no. 10, pp. 3105-3117, Oct. 2016, doi: 10.1109/TVLSI.2016.2535398.

- Wallace

An exact multiplier implemented by Wallace Tree technique.

- Star

An exact multiplier implemented using Verilog star operator, which is usually built by Xilinx IP.


### ours

Our generated unsigned 8x8 multipliers.

