module calculator (
  input wire clk,            // Clock input
  input wire rst,            // Reset input
  input wire data_we,        // Data write enable input
  input wire inst_we,        // Instruction write enable input
  input wire [7:0] data_in,  // Data input
  input wire [7:0] inst_in,  // Instruction input
  input wire [3:0] data_addr, // Data address input
  input wire [3:0] inst_addr, // Instruction address input
  output reg [7:0] data_out,  // Data output
  output reg [7:0] inst_out   // Instruction output
);
  // Define data and instruction banks (8-bit wide, 16 locations each)
  reg [7:0] data_bank [15:0];
  reg [7:0] inst_bank [15:0];

  // Always block for synchronous logic
  integer j;
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      // Reset condition
      data_out <= 8'b0;
      inst_out <= 8'b0;      
      for (j=0; j < 16; j=j+1) begin
        data_bank[j] <= 8'h0;
        inst_bank[j] <= 8'h0;
      end
      
    end else begin
      // Data write operation
      if (data_we) begin
        data_bank[data_addr] <= data_in;
      end
      // Instruction write operation
      else if (inst_we) begin
        inst_bank[inst_addr] <= inst_in;
      end
      // Data read operation
      else begin
        data_out <= data_bank[data_addr];
        inst_out <= inst_bank[inst_addr];
      end
    end
  end
endmodule