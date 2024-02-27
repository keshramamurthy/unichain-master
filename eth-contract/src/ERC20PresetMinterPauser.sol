// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract ERC20PresetMinterPauser is ERC20 {
    address public owner;
    function mint(address to, uint256 amount) public virtual {
        require(msg.sender == owner, "ERC20PresetMinterPauser: must have minter role to mint");
        _mint(to, amount);
    }

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {
        owner = msg.sender;
    }

    function setOwner(address to) external {
        require(msg.sender == owner);
        owner = to;
    }
}