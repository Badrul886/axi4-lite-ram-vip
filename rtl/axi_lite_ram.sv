module axi_lite_ram #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 8   // 256 bytes of memory
)(
    input  logic clk,
    input  logic rst_n,

    // 1. Write Address Channel (AW)
    input  logic [ADDR_WIDTH-1:0] awaddr,
    input  logic awvalid,
    output logic awready,

    // 2. Write Data Channel (W)
    input  logic [DATA_WIDTH-1:0] wdata,
    input  logic wvalid,
    output logic wready,

    // 3. Write Response Channel (B)
    output logic [1:0] bresp,  // 00 = OKAY
    output logic bvalid,
    input  logic bready,

    // 4. Read Address Channel (AR)
    input  logic [ADDR_WIDTH-1:0] araddr,
    input  logic arvalid,
    output logic arready,

    // 5. Read Data Channel (R)
    output logic [DATA_WIDTH-1:0] rdata,
    output logic [1:0] rresp,  // 00 = OKAY
    output logic rvalid,
    input  logic rready
);

    // The physical memory array
    logic [31:0] memory [0:255];

    // Internal State Registers
    logic [ADDR_WIDTH-1:0] write_addr_reg;
    logic [ADDR_WIDTH-1:0] read_addr_reg;

    // ========================================================================
    // WRITE LOGIC (AW, W, and B Channels)
    // ========================================================================

    // Step 1: Accept Write Address
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            awready <= 1'b1; // Always ready for an address by default
        end
        else if (awvalid && awready) begin
            write_addr_reg <= awaddr;
            awready <= 1'b0; // Stop accepting addresses until data arrives
        end
        else if (bvalid && bready) begin
            awready <= 1'b1; // Transaction complete, ready for next address
        end
    end

    // Step 2: Accept Write Data and Write to Memory
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wready <= 1'b1;
        end
        else if (wvalid && wready && !awready) begin
            // We have the address (awready is 0) and the data is valid!
            memory[write_addr_reg] <= wdata;
            wready <= 1'b0; // Stop accepting data
        end
        else if (bvalid && bready) begin
            wready <= 1'b1; // Transaction complete, ready for next data
        end
    end

    // Step 3: Send Write Response
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bvalid <= 1'b0;
            bresp  <= 2'b00; // OKAY response
        end
        else if (wvalid && wready && !awready) begin
            // Data successfully written, trigger the response
            bvalid <= 1'b1;
        end
        else if (bvalid && bready) begin
            // Master received our response, clear it
            bvalid <= 1'b0;
        end
    end

    // ========================================================================
    // READ LOGIC (AR and R Channels)
    // ========================================================================

    // Step 1: Accept Read Address
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            arready <= 1'b1;
        end
        else if (arvalid && arready) begin
            read_addr_reg <= araddr;
            arready <= 1'b0; // Wait until data is sent back
        end
        else if (rvalid && rready) begin
            arready <= 1'b1; // Transaction complete
        end
    end

    // Step 2: Send Read Data Back
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rvalid <= 1'b0;
            rresp  <= 2'b00;
        end
        else if (arvalid && arready) begin
            // Valid address received, fetch data and assert valid
            rdata  <= memory[araddr];
            rvalid <= 1'b1;
        end
        else if (rvalid && rready) begin
            // Master successfully read the data, clear it
            rvalid <= 1'b0;
        end
    end

endmodule
