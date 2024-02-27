// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import './interfaces/IUnichain.sol';
// import './interfaces/IERC20.sol';
import "../lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol";

contract Unichain is IUnichain {
    using SafeERC20 for IERC20;
    address public owner;
    mapping(address => uint256) public reserves;

    function setOwner(address new_owner) external {
        require(msg.sender == owner);
        owner = new_owner;
    }

    function swap(string memory beneficiary, uint256 amount_in, address asset_in, string memory asset_out, uint256 min_amount_out) external {
        IERC20(asset_in).safeTransferFrom(msg.sender, address(this), amount_in);
        uint256 reserve_balance = reserves[asset_in];
        uint256 curr_balance = IERC20(asset_in).balanceOf(address(this));

        uint256 amount_sent = curr_balance - reserve_balance;
        require(amount_sent > 0);

        emit Swap(beneficiary, amount_sent, asset_in, asset_out, min_amount_out);
        reserves[asset_in] = reserves[asset_in] + amount_sent;
    }
    
    constructor() {
        owner = msg.sender;
    }
}
