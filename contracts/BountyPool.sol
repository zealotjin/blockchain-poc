// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract BountyPool is Ownable, ReentrancyGuard {
    IERC20 public stablecoin;

    struct Bounty {
        uint256 totalFunds;
        uint256 remainingFunds;
        address funder;
    }

    struct Claimable {
        address recipient;
        uint256 amount;
        bool claimed;
        bool exists;
    }

    mapping(uint256 => Bounty) public bounties;
    mapping(uint256 => Claimable) public claimablePayouts;

    event BountyFunded(uint256 indexed bountyId, uint256 amount, address indexed funder);
    event ClaimableSet(uint256 indexed submissionId, address indexed recipient, uint256 amount);
    event PayoutClaimed(uint256 indexed submissionId, address indexed recipient, uint256 amount);

    constructor(address _stablecoin) Ownable(msg.sender) {
        stablecoin = IERC20(_stablecoin);
    }

    function fundBounty(uint256 bountyId, uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        require(stablecoin.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        bounties[bountyId].totalFunds += amount;
        bounties[bountyId].remainingFunds += amount;
        bounties[bountyId].funder = msg.sender;

        emit BountyFunded(bountyId, amount, msg.sender);
    }

    function markClaimable(
        uint256 submissionId,
        address recipient,
        uint256 amount
    ) external onlyOwner {
        require(!claimablePayouts[submissionId].exists, "Already marked claimable");
        require(amount > 0, "Amount must be greater than 0");

        claimablePayouts[submissionId] = Claimable({
            recipient: recipient,
            amount: amount,
            claimed: false,
            exists: true
        });

        emit ClaimableSet(submissionId, recipient, amount);
    }

    function claim(uint256 submissionId, address recipient) external nonReentrant {
        Claimable storage claimable = claimablePayouts[submissionId];
        require(claimable.exists, "No claimable payout");
        require(claimable.recipient == recipient, "Not authorized recipient");
        require(!claimable.claimed, "Already claimed");

        claimable.claimed = true;
        require(stablecoin.transfer(recipient, claimable.amount), "Transfer failed");

        emit PayoutClaimed(submissionId, recipient, claimable.amount);
    }

    function getBounty(uint256 bountyId) external view returns (Bounty memory) {
        return bounties[bountyId];
    }

    function getClaimable(uint256 submissionId) external view returns (Claimable memory) {
        require(claimablePayouts[submissionId].exists, "No claimable payout");
        return claimablePayouts[submissionId];
    }
}