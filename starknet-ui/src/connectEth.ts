import { Network, ethers } from "ethers";
const network = new Network("Devnet", 0x7a69);
const provider = new ethers.BrowserProvider(window.ethereum, network);
const signer = await provider.getSigner();
// eslint-disable-next-line
let accounts = [];

const connectETHButton: HTMLElement | null = document.getElementById('eth_connect');

// FILL IN CONTRACT ADDRESS
const ERC20ContractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
// FILL IN ABI
const ABI = '[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"allowance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientAllowance","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientBalance","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC20InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC20InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC20InvalidSender","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"}],"name":"ERC20InvalidSpender","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]';
const ERC20Contract = new ethers.Contract(ERC20ContractAddress, ABI, signer);

const UnichainAddress = "0x68B1D87F95878fE05B998F19b66F4baba5De1aed";
const UnichainABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"beneficiary","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount_in","type":"uint256"},{"indexed":true,"internalType":"address","name":"asset_in","type":"address"},{"indexed":false,"internalType":"string","name":"asset_out","type":"string"},{"indexed":false,"internalType":"uint256","name":"min_amount_out","type":"uint256"}],"name":"Swap","type":"event"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"reserves","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"new_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"beneficiary","type":"string"},{"internalType":"uint256","name":"amount_in","type":"uint256"},{"internalType":"address","name":"asset_in","type":"address"},{"internalType":"string","name":"asset_out","type":"string"},{"internalType":"uint256","name":"min_amount_out","type":"uint256"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
// eslint-disable-next-line
const UnichainContract = new ethers.Contract(UnichainAddress, UnichainABI, signer);

export const handleConnectWallet = async () => {
    // Your logic to connect the wallet
    try {
      // Check if MetaMask is installed
      if (window.ethereum) {
        // Request user's permission to connect their MetaMask wallet
        accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        // setConnected(true);
        if (connectETHButton != null) {
          connectETHButton.innerText = "connected";
        }
        console.log('Wallet connected successfully!');
      } else {
        console.log('MetaMask not detected. Please install MetaMask to connect your wallet.');
      }
    } catch (error) {
      console.error('Error connecting wallet:', error);
    }
  };

  export const callApprove = async (address: string) => {
    // SET AN ARBITRARY VALUE CAUSE DK YET
    console.log(await provider.listAccounts());
    const tokenOne: HTMLInputElement | null = document.getElementById("tokenOne") as HTMLInputElement;
    const tokenTwo: HTMLInputElement | null = document.getElementById("tokenTwo") as HTMLInputElement;
    const tokenOneValue = tokenOne.value;
    const tokenTwoValue = tokenTwo.value;

    console.log(tokenOne, "1");
    console.log(tokenTwo, "2");
    console.log(tokenOneValue, "3");
    console.log(tokenTwoValue, "4");

    if (tokenOneValue === "Choose" || tokenTwoValue === "Choose") {
      console.log('Please select both wallets'); // AKHIL REJECT THIS
    }
    

    // CHECK IF EITHER IS "Choose", IF SO THEN ERROR/DISPLAY ERR MESSAGE
    const tokenOneAmt: HTMLInputElement | null = document.getElementById("token-one-amount") as HTMLInputElement;
    const tokenOneAmount = Number(tokenOneAmt.value);
    const amountIn = BigInt(tokenOneAmount * Math.pow(10, 18));
    // eslint-disable-next-line
    const erc20WithSigner: any = ERC20Contract.connect(signer);
    // DK WHAT ADDRESS SIGNR WILL ALLOW TO SPEND. APPROVE HAS TWO INPUTS: ADDRESS SPENDER AND VALUE ALLOWED TO SPEND
    const tx = await erc20WithSigner.approve(UnichainAddress, amountIn)
    
    await tx.wait()

    callSwap(tokenOneAmount, address)
  }

  export const callSwap = async (amount: number, address: string) => {
    // Call the Unichain Contract here
    // eslint-disable-next-line
    const unichainWithSigner: any = UnichainContract.connect(signer);
    
    const tokenOne: HTMLInputElement | null = document.getElementById("tokenOne") as HTMLInputElement;
    const tokenTwo: HTMLInputElement | null = document.getElementById("tokenTwo") as HTMLInputElement;
    const tokenOneValue = tokenOne.value;
    const tokenTwoValue = tokenTwo.value;
    console.log(address, amount, tokenOneValue, tokenTwoValue, (amount / 10));
    const amountIn = BigInt(amount * Math.pow(10, 18));
    const amountOut = BigInt(amount * Math.pow(10, 18));
    const tx = await unichainWithSigner.swap(
      address,
      amountIn,
      tokenOneValue,
      tokenTwoValue,
      amountOut
    );

    await tx.wait();
  }