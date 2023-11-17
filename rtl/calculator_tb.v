module calculator_tb;

  // Parameters
  parameter CLK_PERIOD = 10;  // Clock period in time units

  // Signals
  reg clk;
  reg rst;
  reg data_we;
  reg inst_we;
  reg [7:0] data_in;
  reg [7:0] inst_in;
  reg [3:0] data_addr;
  reg [3:0] inst_addr;
  wire [7:0] data_out;
  wire [7:0] inst_out;

  // Instantiate the module
  calculator uut (
    .clk(clk),
    .rst(rst),
    .data_we(data_we),
    .inst_we(inst_we),
    .data_in(data_in),
    .inst_in(inst_in),
    .data_addr(data_addr),
    .inst_addr(inst_addr),
    .data_out(data_out),
    .inst_out(inst_out)
  );

  // Clock generation
  always #((CLK_PERIOD / 2)) clk = ~clk;

  // Initial block
  initial begin
    // Initialize signals
    clk = 0;
    rst = 0;
    data_we = 0;
    inst_we = 0;
    data_in = 8'h00;
    inst_in = 8'h00;
    data_addr = 4'h0;
    inst_addr = 4'h1;

    // Apply reset
    #10 rst = 1;

    // Write data and instruction values
    #10 data_we = 1;
    data_in = 8'hAA;
    data_addr = 4'h0;

    #10 inst_we = 1;
    inst_in = 8'h55;
    inst_addr = 4'h1;

    // Read data and instruction values
    #10 data_we = 0;
    #10 inst_we = 0;

    // Monitor outputs and perform comparisons
    #10 $display("Data_out = %h, Inst_out = %h", data_out, inst_out);
    #10 if (data_out == 8'hAA) $display("Data comparison passed!");
       else $display("Data comparison failed!");

    #10 if (inst_out == 8'h55) $display("Inst comparison passed!");
       else $display("Inst comparison failed!");

    // End simulation
    #10 $finish;
  end

endmodule