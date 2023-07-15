// MSE: 207708
// MAE: 365

module  unsigned_mul_8x8_vivado_opt_0p6_log_2_pareto_235 (
  input [7:0] x,
  input [7:0] y,
  output [6:0] ha_array_0_b,
  output [8:0] ha_array_0_t,
  output [6:0] ha_array_1_b,
  output [8:0] ha_array_1_t,
  output [6:0] ha_array_2_b,
  output [8:0] ha_array_2_t,
  output [6:0] ha_array_3_b,
  output [8:0] ha_array_3_t
);

  assign index_16 = y[6] & x[1];
  assign index_17 = y[7] & x[1];
  assign index_18 = y[0] & x[2];
  assign index_19 = y[1] & x[2];
  assign index_20 = y[2] & x[2];
  assign index_21 = y[3] & x[2];
  assign index_22 = y[4] & x[2];
  assign index_23 = y[5] & x[2];
  assign index_24 = y[6] & x[2];
  assign index_25 = y[7] & x[2];
  assign index_26 = y[0] & x[3];
  assign index_27 = y[1] & x[3];
  assign index_28 = y[2] & x[3];
  assign index_29 = y[3] & x[3];
  assign index_30 = y[4] & x[3];
  assign index_31 = y[5] & x[3];
  assign index_32 = y[6] & x[3];
  assign index_33 = y[7] & x[3];
  assign index_34 = y[0] & x[4];
  assign index_35 = y[1] & x[4];
  assign index_36 = y[2] & x[4];
  assign index_37 = y[3] & x[4];
  assign index_38 = y[4] & x[4];
  assign index_39 = y[5] & x[4];
  assign index_40 = y[6] & x[4];
  assign index_41 = y[7] & x[4];
  assign index_42 = y[0] & x[5];
  assign index_43 = y[1] & x[5];
  assign index_44 = y[2] & x[5];
  assign index_45 = y[3] & x[5];
  assign index_46 = y[4] & x[5];
  assign index_47 = y[5] & x[5];
  assign index_48 = y[6] & x[5];
  assign index_49 = y[7] & x[5];
  assign index_50 = y[0] & x[6];
  assign index_51 = y[1] & x[6];
  assign index_52 = y[2] & x[6];
  assign index_53 = y[3] & x[6];
  assign index_54 = y[4] & x[6];
  assign index_55 = y[5] & x[6];
  assign index_56 = y[6] & x[6];
  assign index_57 = y[7] & x[6];
  assign index_58 = y[0] & x[7];
  assign index_59 = y[1] & x[7];
  assign index_60 = y[2] & x[7];
  assign index_61 = y[3] & x[7];
  assign index_62 = y[4] & x[7];
  assign index_63 = y[5] & x[7];
  assign index_64 = y[6] & x[7];
  assign index_65 = y[7] & x[7];
  assign index_66 = y[0] & x[0];
  assign index_67 = y[1] & x[0];
  assign index_68 = y[2] & x[0];
  assign index_69 = y[3] & x[0];
  assign index_70 = y[4] & x[0];
  assign index_71 = y[5] & x[0];
  assign index_72 = y[6] & x[0];
  assign index_73 = y[7] & x[0];
  assign index_74 = y[0] & x[1];
  assign index_75 = y[1] & x[1];
  assign index_76 = y[2] & x[1];
  assign index_77 = y[3] & x[1];
  assign index_78 = y[4] & x[1];
  assign index_79 = y[5] & x[1];

  // eliminate
  assign index_80 = 1'b0;
  assign index_81 = 1'b0;

  // eliminate
  assign index_82 = 1'b0;
  assign index_83 = 1'b0;

  // eliminate
  assign index_84 = 1'b0;
  assign index_85 = 1'b0;

  // only OR sum
  assign index_86 = 1'b0;
  assign index_87 = index_70 | index_77;

  // only OR sum
  assign index_88 = 1'b0;
  assign index_89 = index_71 | index_78;

  // eliminate
  assign index_90 = 1'b0;
  assign index_91 = 1'b0;

  // eliminate
  assign index_92 = 1'b0;
  assign index_93 = 1'b0;

  // eliminate
  assign index_94 = 1'b0;
  assign index_95 = 1'b0;

  // eliminate
  assign index_96 = 1'b0;
  assign index_97 = 1'b0;

  // eliminate
  assign index_98 = 1'b0;
  assign index_99 = 1'b0;

  // only OR sum
  assign index_100 = 1'b0;
  assign index_101 = index_22 | index_29;

  // only OR sum
  assign index_102 = 1'b0;
  assign index_103 = index_23 | index_30;

  // only OR sum
  assign index_104 = 1'b0;
  assign index_105 = index_24 | index_31;

  // $ha
  assign { index_106, index_107 } = index_25 + index_32;

  // eliminate
  assign index_108 = 1'b0;
  assign index_109 = 1'b0;

  // eliminate
  assign index_110 = 1'b0;
  assign index_111 = 1'b0;

  // only A carry
  assign index_112 = index_37;
  assign index_113 = 1'b0;

  // eliminate
  assign index_114 = 1'b0;
  assign index_115 = 1'b0;

  // $ha
  assign { index_116, index_117 } = index_39 + index_46;

  // $ha
  assign { index_118, index_119 } = index_40 + index_47;

  // $ha
  assign { index_120, index_121 } = index_41 + index_48;

  // only OR sum
  assign index_122 = 1'b0;
  assign index_123 = index_51 | index_58;

  // only OR sum
  assign index_124 = 1'b0;
  assign index_125 = index_52 | index_59;

  // $ha
  assign { index_126, index_127 } = index_53 + index_60;

  // $ha
  assign { index_128, index_129 } = index_54 + index_61;

  // $ha
  assign { index_130, index_131 } = index_55 + index_62;

  // $ha
  assign { index_132, index_133 } = index_56 + index_63;

  // $ha
  assign { index_134, index_135 } = index_57 + index_64;

  assign ha_array_0_b[0] = index_80;
  assign ha_array_0_b[1] = index_82;
  assign ha_array_0_b[2] = index_84;
  assign ha_array_0_b[3] = index_86;
  assign ha_array_0_b[4] = index_88;
  assign ha_array_0_b[5] = index_90;
  assign ha_array_0_b[6] = index_17;
  assign ha_array_0_t[0] = index_66;
  assign ha_array_0_t[1] = index_81;
  assign ha_array_0_t[2] = index_83;
  assign ha_array_0_t[3] = index_85;
  assign ha_array_0_t[4] = index_87;
  assign ha_array_0_t[5] = index_89;
  assign ha_array_0_t[6] = index_91;
  assign ha_array_0_t[7] = index_93;
  assign ha_array_0_t[8] = index_92;
  assign ha_array_1_b[0] = index_94;
  assign ha_array_1_b[1] = index_96;
  assign ha_array_1_b[2] = index_98;
  assign ha_array_1_b[3] = index_100;
  assign ha_array_1_b[4] = index_102;
  assign ha_array_1_b[5] = index_104;
  assign ha_array_1_b[6] = index_33;
  assign ha_array_1_t[0] = index_18;
  assign ha_array_1_t[1] = index_95;
  assign ha_array_1_t[2] = index_97;
  assign ha_array_1_t[3] = index_99;
  assign ha_array_1_t[4] = index_101;
  assign ha_array_1_t[5] = index_103;
  assign ha_array_1_t[6] = index_105;
  assign ha_array_1_t[7] = index_107;
  assign ha_array_1_t[8] = index_106;
  assign ha_array_2_b[0] = index_108;
  assign ha_array_2_b[1] = index_110;
  assign ha_array_2_b[2] = index_112;
  assign ha_array_2_b[3] = index_114;
  assign ha_array_2_b[4] = index_116;
  assign ha_array_2_b[5] = index_118;
  assign ha_array_2_b[6] = index_49;
  assign ha_array_2_t[0] = index_34;
  assign ha_array_2_t[1] = index_109;
  assign ha_array_2_t[2] = index_111;
  assign ha_array_2_t[3] = index_113;
  assign ha_array_2_t[4] = index_115;
  assign ha_array_2_t[5] = index_117;
  assign ha_array_2_t[6] = index_119;
  assign ha_array_2_t[7] = index_121;
  assign ha_array_2_t[8] = index_120;
  assign ha_array_3_b[0] = index_122;
  assign ha_array_3_b[1] = index_124;
  assign ha_array_3_b[2] = index_126;
  assign ha_array_3_b[3] = index_128;
  assign ha_array_3_b[4] = index_130;
  assign ha_array_3_b[5] = index_132;
  assign ha_array_3_b[6] = index_65;
  assign ha_array_3_t[0] = index_50;
  assign ha_array_3_t[1] = index_123;
  assign ha_array_3_t[2] = index_125;
  assign ha_array_3_t[3] = index_127;
  assign ha_array_3_t[4] = index_129;
  assign ha_array_3_t[5] = index_131;
  assign ha_array_3_t[6] = index_133;
  assign ha_array_3_t[7] = index_135;
  assign ha_array_3_t[8] = index_134;

endmodule
