// ==============================================================
// Generated by Vitis HLS v2024.1
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.
// ==============================================================
`timescale 1 ns / 1 ps
module KAN_lut_0_0_2_RAM_1P_LUTRAM_1R1W (
    address0, ce0, q0, 
    reset, clk);

parameter DataWidth = 3;
parameter AddressWidth = 6;
parameter AddressRange = 64;
 
input[AddressWidth-1:0] address0;
input ce0;
output reg[DataWidth-1:0] q0;

input reset;
input clk;

 
(* rom_style = "distributed" *)reg [DataWidth-1:0] rom0[0:AddressRange-1];


initial begin
     
    $readmemh("./KAN_lut_0_0_2_RAM_1P_LUTRAM_1R1W.dat", rom0);
end

  
always @(posedge clk) 
begin 
    if (ce0) 
    begin
        q0 <= rom0[address0];
    end
end


endmodule

