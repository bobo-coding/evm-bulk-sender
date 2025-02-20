// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

interface IERC20 {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

/// @title BulkSendOptimized
/// @notice Optimized bulk transfer contract to send tokens from the sender to multiple recipients in one transaction.
contract BulkSendOptimized {
    /// @notice Transfers tokens from the caller to each recipient for the specified amounts.
    /// @param token The ERC20 token address.
    /// @param recipients An array of recipient addresses.
    /// @param amounts An array of token amounts (in wei) to transfer.
    /// @return success True if all transfers succeed.
    function bulkSend(
        address token,
        address[] calldata recipients,
        uint256[] calldata amounts
    ) external returns (bool success) {
        // Ensure that the input arrays have the same length.
        require(recipients.length == amounts.length, "Length mismatch");

        uint256 count = recipients.length;
        IERC20 tokenContract = IERC20(token);
        address sender = msg.sender;

        // Loop over each recipient
        for (uint256 i = 0; i < count; ) {
            // Transfer tokens from the sender to current recipient. Reverts if transfer fails.
            require(
                tokenContract.transferFrom(sender, recipients[i], amounts[i]),
                "Transfer failed"
            );
            unchecked {
                ++i; // Unchecked increment saves a bit of gas.
            }
        }
        return true;
    }
} 