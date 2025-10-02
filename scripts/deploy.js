const hre = require("hardhat");
const fs = require("fs");

async function main() {
  console.log("Deploying contracts...");

  // Deploy MockUSDT first
  const MockUSDT = await hre.ethers.getContractFactory("MockUSDT");
  const mockUSDT = await MockUSDT.deploy();
  await mockUSDT.waitForDeployment();
  console.log("MockUSDT deployed to:", await mockUSDT.getAddress());

  // Deploy SubmissionRegistry
  const SubmissionRegistry = await hre.ethers.getContractFactory("SubmissionRegistry");
  const submissionRegistry = await SubmissionRegistry.deploy();
  await submissionRegistry.waitForDeployment();
  console.log("SubmissionRegistry deployed to:", await submissionRegistry.getAddress());

  // Deploy VerificationManager
  const VerificationManager = await hre.ethers.getContractFactory("VerificationManager");
  const verificationManager = await VerificationManager.deploy();
  await verificationManager.waitForDeployment();
  console.log("VerificationManager deployed to:", await verificationManager.getAddress());

  // Deploy BountyPool with MockUSDT address
  const BountyPool = await hre.ethers.getContractFactory("BountyPool");
  const bountyPool = await BountyPool.deploy(await mockUSDT.getAddress());
  await bountyPool.waitForDeployment();
  console.log("BountyPool deployed to:", await bountyPool.getAddress());

  // Save deployment addresses
  const deploymentInfo = {
    network: hre.network.name,
    mockUSDT: await mockUSDT.getAddress(),
    submissionRegistry: await submissionRegistry.getAddress(),
    verificationManager: await verificationManager.getAddress(),
    bountyPool: await bountyPool.getAddress(),
    deployedAt: new Date().toISOString()
  };

  fs.writeFileSync(
    "./deployments/addresses.json",
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log("\n=== Deployment Summary ===");
  console.log(`Network: ${deploymentInfo.network}`);
  console.log(`MockUSDT: ${deploymentInfo.mockUSDT}`);
  console.log(`SubmissionRegistry: ${deploymentInfo.submissionRegistry}`);
  console.log(`VerificationManager: ${deploymentInfo.verificationManager}`);
  console.log(`BountyPool: ${deploymentInfo.bountyPool}`);
  console.log("\nAddresses saved to ./deployments/addresses.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });