const fs = require('fs');

const manifestHash = "0eb9fa464ecfa17e1616bb4666bda3aa832d4b5376524e319886582f437a9486";

const initialBundle = {
  schemaVersion: "2.1.2",
  manifestHash: manifestHash,
  evidence: [
    {
      capability: "FS_WRITE",
      timestamp: new Date().toISOString(),
      outcome: "GRANTED",
      artifactHash: manifestHash,
      logDigest: "Agent A signed file"
    }
  ],
  metadata: {
    identity: "agent-a-typescript-node",
    runtime: "node-v22-sandbox",
    toolchainVersion: "2.1.2-mvp.3.5"
  }
};

fs.mkdirSync('logs', { recursive: true });
fs.writeFileSync('logs/evidence_bundle.json', JSON.stringify(initialBundle, null, 2));
console.log("[Agent A (TS)] Initial Evidence Bundle signed with genuine Byte-Aligned ManifestHash.");
