// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract VerificationManager is AccessControl {
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    struct Verification {
        address verifier;
        bool accepted;
        uint8 reasonCode;
        uint256 timestamp;
        bool exists;
    }

    mapping(uint256 => Verification) public verifications;

    event SubmissionVerified(
        uint256 indexed submissionId,
        address indexed verifier,
        bool accepted,
        uint8 reasonCode,
        uint256 timestamp
    );

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
    }

    function setVerification(
        uint256 submissionId,
        bool accepted,
        uint8 reasonCode
    ) external onlyRole(VERIFIER_ROLE) {
        require(!verifications[submissionId].exists, "Already verified");

        verifications[submissionId] = Verification({
            verifier: msg.sender,
            accepted: accepted,
            reasonCode: reasonCode,
            timestamp: block.timestamp,
            exists: true
        });

        emit SubmissionVerified(
            submissionId,
            msg.sender,
            accepted,
            reasonCode,
            block.timestamp
        );
    }

    function getVerification(uint256 submissionId) external view returns (Verification memory) {
        require(verifications[submissionId].exists, "Verification does not exist");
        return verifications[submissionId];
    }

    function isAccepted(uint256 submissionId) external view returns (bool) {
        require(verifications[submissionId].exists, "Verification does not exist");
        return verifications[submissionId].accepted;
    }
}