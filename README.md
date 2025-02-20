# EVM Bulk Sender

This project implements an EVM Bulk Sender dApp using a smart contract and a web interface.

## Overview

The EVM Bulk Sender application allows you to send ERC20 tokens to multiple recipients in a single transaction. The project consists of three major components:

- **Smart Contract:**  
  An optimized Solidity contract (`BulkSendOptimized.sol`) that performs bulk transfers using gas-saving techniques.

- **Backend API:**  
  A Flask application (`app.py`) that processes CSV uploads containing recipient addresses and token amounts (in wei) and returns the parsed data in JSON format.

- **Frontend Interface:**  
  A web interface (`templates/index.html`) that integrates with MetaMask, allows CSV file upload or manual data entry, calculates computed wei amounts, and facilitates token approval and bulk transfer transactions using Web3.js and ethers.js.

## Features

- **CSV Upload & Manual Entry:**  
  - Upload a CSV file with recipient addresses and token amounts (in wei).  
  - Edit, add, or delete recipient rows manually.  
  - Automatically display a computed wei value based on the input.

- **Bulk Transfer Functionality:**  
  - Utilize the Solidity bulk transfer contract to efficiently send tokens to multiple recipients.
  
- **MetaMask Integration:**  
  - Connect your MetaMask wallet to interact with the dApp on your chosen Ethereum network.
  
- **Configurable Bulk Contract Address:**  
  - The BulkSend contract address is user-editable via an input field in the web interface.

## Requirements

- [Node.js](https://nodejs.org/) (for managing frontend dependencies)
- [Python 3](https://www.python.org/) and Flask (for running the backend API)
- [MetaMask](https://metamask.io/) browser extension
- A deployed ERC20 token and a BulkSend contract on your target network

## Installation & Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/bobo-coding/evm-bulk-sender.git
    cd evm-bulk-sender
    ```

2. **Install Python Dependencies:**

    Create a virtual environment (optional) and install the required packages:

    ```bash
    pip install Flask web3
    ```

3. **Run the Flask Backend:**

    ```bash
    python app.py
    ```

    By default, the backend will run on `http://localhost:5001`.

4. **Open the Web Interface:**

    Open your browser and navigate to `http://localhost:5001`.

## Deploying the Smart Contract

The Solidity contract is located in the `contracts` folder as `BulkSendOptimized.sol`. To deploy the contract:

1. Open [Remix](https://remix.ethereum.org/) or use a development framework like [Hardhat](https://hardhat.org/).
2. Compile and deploy the contract using Solidity version 0.8.17 or higher.
3. After deployment, update the "Bulk Contract Address" field in the web interface if required.

## Usage

1. **Connect MetaMask:**  
   Click on the "Connect MetaMask" button and select your account.
   
2. **Enter Contract Addresses:**  
   - Provide the ERC20 Token Contract Address in the designated input field.
   - Provide the BulkSend Contract Address in the "Bulk Contract Address" field.

3. **CSV Upload & Manual Editing:**  
   - Upload a CSV file with recipient addresses and token amounts (the amounts are expected as wei).  
   - The parsed CSV data will appear in an editable table where you can manually add, modify, or delete rows.  
   - The "Computed Amount (wei)" column will display the resulting value (computed using a heuristic if needed).

4. **Approve & Send Bulk Transfer:**  
   - Click the "Approve Token Transfer" button to approve the BulkSend contract for the required amount.
   - Once approved, click "Send Bulk Transfer" to execute the transaction.

## Project Structure 