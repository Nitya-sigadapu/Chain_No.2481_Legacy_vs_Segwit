# Chain_No.2481_Legacy_vs_Segwit
# CS 216 — Bitcoin Transactions Project

## Legacy vs SegWit Transaction Analysis

### Team Members

| Name                         | Roll Number |
| ---------------------------- | ----------- |
|  Lucky Reddy Prayuktha Reddy | 240041025 |
| Sigadapu Nitya               | 240005048 |
| Sudhiksha Vijayagiri         | 240001079 |
| Katravath Madhavi            | 240041021 |

---

# Project Overview

This project demonstrates the creation and analysis of Bitcoin transactions using **Bitcoin Core in regtest mode**. Two types of transaction structures were implemented and analyzed:

1. **Legacy P2PKH Transactions**
2. **SegWit P2SH-P2WPKH Transactions**

For each transaction type we:

* Generated three addresses (A, B, C)
* Created two transactions:

  * **A → B**
  * **B → C**
* Decoded the transactions
* Examined script structure
* Validated scripts using **btcdeb**
* Compared transaction size, vsize, and weight

The goal is to understand how SegWit improves efficiency compared to legacy transactions.

---

# Prerequisites

The following software must be installed:

* **Bitcoin Core**
* **Python 3**
* Python package:

```
pip install python-bitcoinrpc
```

* **btcdeb debugger**

Bitcoin Core must be running in **regtest mode** with RPC enabled.

Example `bitcoin.conf`:

```
regtest=1
server=1
rpcuser=student
rpcpassword=bitcoin123
txindex=1
```

# Starting Bitcoin Core

Start Bitcoin Core in regtest mode:

```
bitcoind -regtest -daemon
```

Verify connection:

```
bitcoin-cli -regtest getblockchaininfo
```

---

# Creating Wallet

Create a wallet before running the scripts:

```
bitcoin-cli -regtest createwallet testwallet
```

Mine initial blocks to generate spendable coins:

```
bitcoin-cli -regtest generatetoaddress 101 <address>
```

This step is required because coinbase rewards become spendable only after **100 confirmations**.

---

# Running the Program

Two Python scripts are included:

```
test.py           → Legacy transactions
segwit_test.py    → SegWit transactions
```

Run the scripts using:

```
python test.py
```

and

```
python segwit_test.py
```

The scripts perform the following steps automatically:

1. Connect to the Bitcoin RPC node
2. Generate addresses A, B, and C
3. Fund address A
4. Mine blocks to confirm transactions
5. Create raw transactions
6. Decode transactions
7. Sign transactions
8. Broadcast transactions
9. Mine blocks to confirm transactions

---

# Transaction Flow

### Legacy Transactions

```
A → B   (5 BTC)
B → C   (2 BTC)
```

Script type used:

```
P2PKH (Pay-to-Public-Key-Hash)
```

Example script:

```
OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
```

---

### SegWit Transactions

```
A' → B'
B' → C'
```

Script type used:

```
P2SH-P2WPKH
```

Key differences:

* Signature moved to **witness data**
* Reduced transaction weight
* Lower effective transaction fees

---

# Output Produced

The scripts print:

* Generated addresses
* Raw transactions
* Decoded transaction structure
* Signed transaction hex
* Broadcast TXIDs
* UTXO information

The following values are extracted for analysis:

* `scriptPubKey.asm`
* `scriptSig.asm`
* `txinwitness`
* `size`
* `vsize`
* `weight`

---

# Script Validation Using btcdeb

The Bitcoin Script debugger **btcdeb** was used to validate the execution of scripts.

Example command:

```
btcdeb
```

Example script execution:

```
exec <signature> <pubkey> OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
```

The debugger shows stack operations such as:

```
PUSH stack
POP stack
OP_CHECKSIG
```

This confirms correct script validation.

---

# Comparative Analysis

The project compares:

* Transaction size
* Virtual size (vsize)
* Weight
* Script structure
* Signature placement

SegWit transactions demonstrate:

* Reduced transaction weight
* Lower fee cost
* Fix for transaction malleability
* Compatibility with Layer-2 solutions such as the **Lightning Network**

---

# Repository Structure

```
project/
│
├── legacy.py              # Legacy transaction script
├── segwit.py       # SegWit transaction script
├── README.md
└── report.pdf
```

---

# Notes

* The project uses **Bitcoin regtest**, so no real Bitcoin is used.
* Blocks are mined locally for testing purposes.
* Transactions are confirmed by mining **one block after each broadcast**.

---

# References

* Bitcoin Developer Documentation
* Bitcoin Core RPC API
* Bitcoin Script Documentation
* CS216 Course Material
