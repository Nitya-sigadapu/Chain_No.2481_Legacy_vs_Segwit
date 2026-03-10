from bitcoinrpc.authproxy import AuthServiceProxy

# RPC connection
rpc_user = "student"
rpc_password = "bitcoin123"

rpc = AuthServiceProxy("http://%s:%s@127.0.0.1:18443" % (rpc_user, rpc_password))

# load wallet safely
try:
    rpc.loadwallet("testwallet")
except:
    pass

print("\nConnected to Bitcoin RPC\n")

# Generate P2SH-SegWit addresses
A = rpc.getnewaddress("A","p2sh-segwit")
B = rpc.getnewaddress("B","p2sh-segwit")
C = rpc.getnewaddress("C","p2sh-segwit")

print("Address A:", A)
print("Address B:", B)
print("Address C:", C)

# fund A
fund_txid = rpc.sendtoaddress(A,20)
print("\nFunding TXID:", fund_txid)

# mine block
rpc.generatetoaddress(1,A)

# find UTXO for A
utxos = rpc.listunspent()

utxoA = None
for u in utxos:
    if u["address"] == A:
        utxoA = u
        break

print("\nUTXO for A:", utxoA)

# ---------- TRANSACTION A -> B ----------

inputs = [{
    "txid": utxoA["txid"],
    "vout": utxoA["vout"]
}]

amount_to_send = 5
fee = 0.0001
change = float(utxoA["amount"]) - amount_to_send - fee

outputs = {
    B: amount_to_send,
    A: change
}

raw_tx_ab = rpc.createrawtransaction(inputs,outputs)

print("\nRaw TX A->B:")
print(raw_tx_ab)

decoded_ab = rpc.decoderawtransaction(raw_tx_ab)

print("\nDecoded TX A->B:")
print(decoded_ab)

signed_ab = rpc.signrawtransactionwithwallet(raw_tx_ab)

print("\nSigned TX A->B:")
print(signed_ab["hex"])

txid_ab = rpc.sendrawtransaction(signed_ab["hex"])

print("\nBroadcast TXID A->B:",txid_ab)

# mine block
rpc.generatetoaddress(1,A)

# ---------- FIND UTXO FOR B ----------

utxos = rpc.listunspent()

utxoB = None
for u in utxos:
    if u["address"] == B:
        utxoB = u
        break

print("\nUTXO for B:",utxoB)

# ---------- TRANSACTION B -> C ----------

inputs = [{
    "txid": utxoB["txid"],
    "vout": utxoB["vout"]
}]

amount_to_send = 2
fee = 0.0001
change = float(utxoB["amount"]) - amount_to_send - fee

outputs = {
    C: amount_to_send,
    B: change
}

raw_tx_bc = rpc.createrawtransaction(inputs,outputs)

print("\nRaw TX B->C:")
print(raw_tx_bc)

decoded_bc = rpc.decoderawtransaction(raw_tx_bc)

print("\nDecoded TX B->C:")
print(decoded_bc)

signed_bc = rpc.signrawtransactionwithwallet(raw_tx_bc)

print("\nSigned TX B->C:")
print(signed_bc["hex"])

txid_bc = rpc.sendrawtransaction(signed_bc["hex"])

print("\nBroadcast TXID B->C:",txid_bc)

rpc.generatetoaddress(1,A)

print("\nSegWit transaction flow complete.")