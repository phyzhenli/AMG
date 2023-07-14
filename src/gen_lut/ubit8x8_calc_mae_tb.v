`timescale 1ms/1ms

module ubit8x8_calc_mae_tb;

parameter bit = 8;

reg  [bit-1:0] x;
reg  [bit-1:0] y;
wire [bit*2-1:0] z;
unsigned_8x8_mul_top u1(x, y, z);
wire [bit*2-1:0] exact_z = x * y;

wire signed [63:0] signed_z = z;
wire signed [63:0] signed_exact_z = exact_z;
wire signed [63:0] error = signed_z - signed_exact_z;
wire signed [63:0] abs_error = (error[63] == 1)? (~error + 1'b1) : error;

reg clk;
parameter period = 2;
reg [64:0] mae;
// integer file;

initial begin
  x = 0;
  y = 0;
  clk = 0;
  mae = 0;
  // file = $fopen("lut.txt");
end

always #(period/2) clk =~clk;

always@(posedge clk) begin
  mae <= mae + abs_error;
  y <= y + 1;
  // $fwrite(file, "%0d ", mse);
  if (y == 2**bit-1) begin
    x <= x + 1;
    // $fwrite(file, "\n");
  end
  if (x == 2**bit-1 && y == 2**bit-1) begin
    $display("MAE: %0f", $bitstoreal(mae+abs_error) / $bitstoreal(2**16));
    // $fclose(file);
    $finish;
  end
end

endmodule
