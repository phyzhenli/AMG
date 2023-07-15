module unsigned_8x8_mul_top (
  input [7:0] x,
  input [7:0] y,
  output [15:0] z
);

  wire [8:0] ha_array_0_t;
  wire [6:0] ha_array_0_b;
  wire [8:0] ha_array_1_t;
  wire [6:0] ha_array_1_b;
  wire [8:0] ha_array_2_t;
  wire [6:0] ha_array_2_b;
  wire [8:0] ha_array_3_t;
  wire [6:0] ha_array_3_b;

  unsigned_8x8_mul_ha_array U_ha_array ( .x(x), .y(y), .ha_array_0_t(ha_array_0_t), .ha_array_0_b(ha_array_0_b), .ha_array_1_t(ha_array_1_t), .ha_array_1_b(ha_array_1_b), .ha_array_2_t(ha_array_2_t), .ha_array_2_b(ha_array_2_b), .ha_array_3_t(ha_array_3_t), .ha_array_3_b(ha_array_3_b) );

  assign z = { ha_array_0_t } + { ha_array_0_b, 2'b0 } + { ha_array_1_t, 2'b0 } + { ha_array_1_b, 4'b0 } + { ha_array_2_t, 4'b0 } + { ha_array_2_b, 6'b0 } + { ha_array_3_t, 6'b0 } + { ha_array_3_b, 8'b0 };

endmodule

module HA (
  input A,
  input B,
  output C,
  output S
);

  assign { C, S } = A + B;

endmodule
