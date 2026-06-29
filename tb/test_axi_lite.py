import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from axi_master_driver import Axi4LiteMaster
import vsc

# ============================================================================
# 1. The Constrained Random Transaction Object
# ============================================================================
@vsc.randobj
class AxiTransaction:
    def __init__(self):
        # We need an 8-bit address (our RAM is 256 bytes) and 32-bit data
        self.addr = vsc.rand_bit_t(8)
        self.data = vsc.rand_bit_t(32)
    
    @vsc.constraint
    def address_alignment(self):
        # Address must be 4-byte aligned (divisible by 4)
        self.addr % 4 == 0
        # Address must stay safely within our 256-byte memory array
        self.addr < 252

# ============================================================================
# 2. The Stress Test
# ============================================================================
@cocotb.test()
async def test_axi_randomized_stress(dut):
    """Stress test AXI4-Lite RAM with Constrained Randomization."""
    
    # Start clock and reset
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    master = Axi4LiteMaster(dut, dut.clk)
    await master.reset()

    dut.rst_n.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")

    # Initialize the PyVSC randomizer
    rand_txn = AxiTransaction()
    NUM_TRANSACTIONS = 20
    
    dut._log.info(f"Starting Constrained Random Stress Test: {NUM_TRANSACTIONS} Transactions")

    # Bombard the bus!
    for i in range(NUM_TRANSACTIONS):
        # 1. Generate new random, constrained values
        rand_txn.randomize()
        
        # Extract the random integers
        test_addr = int(rand_txn.addr)
        test_data = int(rand_txn.data)
        
        dut._log.info(f"--- Transaction {i+1}/{NUM_TRANSACTIONS} ---")
        dut._log.info(f"WRITING -> Addr: {hex(test_addr)}, Data: {hex(test_data)}")
        
        # 2. Execute the Write
        await master.write_bus(address=test_addr, data=test_data)
        
        # 3. Execute the Read from the exact same random address
        dut._log.info(f"READING <- Addr: {hex(test_addr)}")
        read_data = await master.read_bus(address=test_addr)
        
        # 4. The Automated Golden Checker
        assert read_data == test_data, f"DATA CORRUPTION at {hex(test_addr)}! Wrote {hex(test_data)}, Read {hex(read_data)}"
    
    dut._log.info("MASSIVE SUCCESS: AXI4-Lite Bus survived constrained random stress testing!")
    await Timer(50, unit="ns")
