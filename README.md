# PyChain: Simple Blockchain in Python

This project is a minimal blockchain implementation in Python, It demonstrates the core concepts of blockchain technology, including block creation, proof-of-work mining, and chain validation, all accessible via a simple Flask web API.

## Project Name
**PyChain**

## Features
- **Block Structure:** Each block contains an index, timestamp, proof (for mining), and the hash of the previous block.
- **Proof of Work:** A basic algorithm to secure the blockchain by requiring computational work to mine new blocks.
- **Chain Validation:** Ensures the integrity of the blockchain by checking hashes and proofs.
- **REST API:** Interact with the blockchain using HTTP endpoints.

## Endpoints
- `GET /mine_block` — Mines a new block and returns its details.
- `GET /get_chain` — Returns the full blockchain and its length.

## Getting Started

### Prerequisites
- Python 3.7+
- Flask

### Installation
1. Clone this repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
Start the Flask server:
```bash
python main.py
```
The API will be available at `http://0.0.0.0:5000/`.

## Example Usage
- To mine a block: Open your browser or use curl to visit `http://localhost:5000/mine_block`
- To view the blockchain: Visit `http://localhost:5000/get_chain`

## File Structure
- `main.py` — Flask app exposing the blockchain API.
- `blocks.py` — Contains the `Blockchain` class and core logic.
- `requirements.txt` — Python dependencies.

## Limitations
- No transaction support (blocks only contain proof and hashes).
- No peer-to-peer networking or distributed consensus.
- Not suitable for production use.

