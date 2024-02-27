// SPDX-License-Identifier: UNLICENSED 
pragma solidity ^0.8.13;

interface IUnichain {
    event Swap(string beneficiary, uint256 amount_in, address indexed asset_in, string asset_out, uint256 min_amount_out);
    function swap(string memory beneficiary, uint256 amount_in, address asset_in, string memory asset_out, uint256 min_amount_out) external;
    function setOwner(address new_owner) external;
}