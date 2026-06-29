\# AMBA AXI4-Lite Memory Slave \& Verification Intellectual Property (VIP)



\## 📌 Overview



This repository contains a synthesizable, parameterized \*\*AMBA AXI4-Lite RAM Slave\*\* implementation together with a complete verification environment built using \*\*Python\*\*, \*\*Cocotb\*\*, and \*\*PyVSC (Python Verification Stimulus and Coverage)\*\*.



The verification environment applies \*\*Constrained Random Verification (CRV)\*\* to thoroughly validate the AXI4-Lite protocol, stressing handshake timing, address alignment, and memory transactions under randomized operating conditions.



\---



\## 🏗️ Design Architecture



The design implements a fully compliant \*\*AMBA AXI4-Lite Memory Slave\*\* featuring:



\* 32-bit data bus

\* 8-bit address space

\* Single outstanding transactions

\* Fully synthesizable RTL implementation



\### AXI4-Lite Transaction Channels



The design operates through the five standard AXI4-Lite channels, each using the `VALID`/`READY` handshake protocol.



| Channel                | Description                                     |

| ---------------------- | ----------------------------------------------- |

| \*\*Write Address (AW)\*\* | Receives target write addresses from the master |

| \*\*Write Data (W)\*\*     | Accepts 32-bit write data                       |

| \*\*Write Response (B)\*\* | Returns transaction status (`2'b00` = \*\*OKAY\*\*) |

| \*\*Read Address (AR)\*\*  | Receives target read addresses                  |

| \*\*Read Data (R)\*\*      | Returns requested data to the master            |



\---



\## 🔬 Verification Strategy



The verification environment is implemented using:



\* Python

\* Cocotb

\* PyVSC



Instead of relying on directed test vectors, the testbench employs \*\*Constrained Random Verification (CRV)\*\* to maximize protocol coverage.



\### Bus Functional Model (BFM)



A reusable Python Bus Functional Model (`Axi4LiteMaster`) abstracts low-level AXI signal manipulation into high-level asynchronous API calls:



\* `write\_bus()`

\* `read\_bus()`



This enables concise and reusable transaction generation while maintaining protocol compliance.



\---



\## 🎲 Constrained Random Verification (PyVSC)



PyVSC provides a SystemVerilog-style constraint solver for randomized stimulus generation.



\### Implemented Constraints



\#### Address Alignment



Addresses are constrained to \*\*4-byte boundaries\*\* to model realistic processor memory accesses.



```python

address % 4 == 0

```



\#### Memory Boundary Protection



Randomized addresses are automatically limited to the valid RAM address space, preventing transactions outside the allocated memory region.



\---



\## 🐛 Development Bug Hunt (Authenticity Log)



\### Combinational Read Data Sampling



\#### Problem



Early simulation runs exhibited intermittent read failures caused by the RAM's combinational output path:



```verilog

assign rdata = memory\[araddr];

```



Since the memory output changed immediately after the rising clock edge, the Python monitor occasionally sampled the updated value due to delta-cycle scheduling.



\#### Solution



The monitoring VIP was redesigned to sample bus signals during the \*\*FallingEdge\*\* (setup window), ensuring all read data was stable before protocol validation.



This eliminated race conditions and produced deterministic simulation behavior.



\---



\## 🚀 Getting Started



\### Prerequisites



Install the following tools:



\* Python 3

\* Icarus Verilog (`iverilog`)

\* Cocotb

\* PyVSC



\---



\### Clone the Repository



```bash

git clone https://github.com/YourUsername/axi4-lite-ram-vip.git

cd axi4-lite-ram-vip

```



\---



\### Install Python Dependencies



```bash

pip install cocotb pyvsc

```



\---



\### Run the Simulation



```bash

cd sim

make WAVES=1

```



\---



\## 📂 Repository Structure



```text

axi4-lite-ram-vip/

│

├── rtl/

│   └── axi\_lite\_ram.sv

│

├── tb/

│   ├── axi\_master\_driver.py

│   └── test\_axi\_lite.py

│

├── sim/

│   └── Makefile

│

├── docs/

│   ├── axi4\_lite terminal PASS.png

│   └── axi4\_lite waveform.png

│

└── README.md

```



\---



\## 🎯 Learning Objectives



This project demonstrates practical implementation of:



\* AMBA AXI4-Lite Protocol

\* Memory-Mapped Peripheral Design

\* Cocotb-based Verification

\* Python Bus Functional Models (BFMs)

\* Constrained Random Verification (CRV)

\* PyVSC Constraint Solving

\* Protocol Handshake Verification

\* Transaction-Level Verification

\* Verification Debugging and Delta-Cycle Analysis



\---



\## 📜 License



This project is intended for educational and learning purposes.



\---



\## ✅ Verification Results



The verification environment validates:



\* AXI4-Lite `VALID/READY` handshake compliance

\* Correct write transactions

\* Correct read transactions

\* Address alignment requirements

\* Memory boundary protection

\* Randomized transaction sequences

\* Stable protocol behavior across multiple constrained-random test iterations



!\[Terminal Pass](docs/axi4\_lite%20terminal%20PASS.png)

!\[Terminal Pass](docs/axi4\_lite%20waveform.png)





