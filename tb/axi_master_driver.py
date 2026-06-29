import cocotb
from cocotb.triggers import RisingEdge, ReadOnly


class Axi4LiteMaster:
    """A Python Bus Functional Model (BFM) for an AXI4-Lite Master."""

    def __init__(self, dut, clk):
        self.dut = dut
        self.clk = clk

    async def reset(self):
        """Initializes all Master signals to 0."""
        self.dut.awvalid.value = 0
        self.dut.wvalid.value  = 0
        self.dut.bready.value  = 0
        self.dut.arvalid.value = 0
        self.dut.rready.value  = 0
        self.dut.awaddr.value  = 0
        self.dut.wdata.value   = 0
        self.dut.araddr.value  = 0

    async def write_bus(self, address, data):
        """Executes a full AXI4-Lite Write Transaction using Py-Coroutines."""

        # 1. Drive the Write Address Channel (AW)
        await RisingEdge(self.clk)
        self.dut.awaddr.value = address
        self.dut.awvalid.value = 1

        # Wait for the Slave to say "READY"
        await ReadOnly()
        while self.dut.awready.value == 0:
            await RisingEdge(self.clk)
            await ReadOnly()

        # Address accepted, turn off valid
        await RisingEdge(self.clk)
        self.dut.awvalid.value = 0

        # 2. Drive the Write Data Channel (W)
        self.dut.wdata.value = data
        self.dut.wvalid.value = 1

        # Wait for the Slave to say "READY"
        await ReadOnly()
        while self.dut.wready.value == 0:
            await RisingEdge(self.clk)
            await ReadOnly()

        # Data accepted, turn off valid
        await RisingEdge(self.clk)
        self.dut.wvalid.value = 0

        # 3. Wait for the Write Response (B)
        self.dut.bready.value = 1  # Tell slave we are ready for response

        await ReadOnly()
        while self.dut.bvalid.value == 0:
            await RisingEdge(self.clk)
            await ReadOnly()

        # Response received!
        response = self.dut.bresp.value

        await RisingEdge(self.clk)
        self.dut.bready.value = 0

        if response != 0:
            cocotb.log.error(f"AXI Write Error! Response code: {response}")

    async def read_bus(self, address):
        """Executes a full AXI4-Lite Read Transaction."""
        
        # 1. Drive the Read Address Channel (AR)
        await RisingEdge(self.clk)
        self.dut.araddr.value = address
        self.dut.arvalid.value = 1
        
        # Wait for the Slave to say "READY"
        await ReadOnly()
        while self.dut.arready.value == 0:
            await RisingEdge(self.clk)
            await ReadOnly()
            
        # Address accepted
        await RisingEdge(self.clk)
        self.dut.arvalid.value = 0

        # 2. Wait for the Read Data Channel (R)
        self.dut.rready.value = 1 # Tell slave we are ready to receive data
        
        await ReadOnly()
        while self.dut.rvalid.value == 0:
            await RisingEdge(self.clk)
            await ReadOnly()
            
        # Capture the data!
        data = self.dut.rdata.value.to_unsigned()
        response = self.dut.rresp.value
        
        await RisingEdge(self.clk)
        self.dut.rready.value = 0
        
        if response != 0:
            cocotb.log.error(f"AXI Read Error! Response code: {response}")
            
        return data
   
