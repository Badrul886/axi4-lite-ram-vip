# Default simulator
SIM ?= icarus

# Language of the hardware
TOPLEVEL_LANG ?= verilog

# Path to the Verilog source file in the rtl directory
VERILOG_SOURCES += $(PWD)/../rtl/axi_lite_ram.sv

# The name of the top-level Verilog module
TOPLEVEL = axi_lite_ram

# Tell cocotb to look inside the tb/ folder for Python modules
export PYTHONPATH := $(PWD)/../tb:$(PYTHONPATH)
MODULE = test_axi_lite

# Include Cocotb's standard simulation rules
include $(shell cocotb-config --makefiles)/Makefile.sim