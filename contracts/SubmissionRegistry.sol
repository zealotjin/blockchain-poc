// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SubmissionRegistry {
    struct Submission {
        address submitter;
        string contentHash;
        string uri;
        string mime;
        uint256 timestamp;
    }

    mapping(uint256 => Submission) public submissions;
    uint256 public submissionCount;

    event SubmissionRegistered(
        uint256 indexed id,
        address indexed submitter,
        string contentHash,
        string uri,
        string mime,
        uint256 timestamp
    );

    function registerSubmission(
        string memory contentHash,
        string memory uri,
        string memory mime
    ) external returns (uint256) {
        uint256 submissionId = submissionCount++;

        submissions[submissionId] = Submission({
            submitter: msg.sender,
            contentHash: contentHash,
            uri: uri,
            mime: mime,
            timestamp: block.timestamp
        });

        emit SubmissionRegistered(
            submissionId,
            msg.sender,
            contentHash,
            uri,
            mime,
            block.timestamp
        );

        return submissionId;
    }

    function getSubmission(uint256 id) external view returns (Submission memory) {
        require(id < submissionCount, "Submission does not exist");
        return submissions[id];
    }
}