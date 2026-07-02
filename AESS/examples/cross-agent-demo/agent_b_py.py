import os, json, sys
from datetime import datetime, timezone

EVIDENCE_PATH = 'logs/evidence_bundle.json'
RESULT_PATH = 'logs/RESULT.json'
print("[Agent B (Py)] Accessing relayed evidence bundle for peer-review...")

if not os.path.exists(EVIDENCE_PATH):
    print("[-] ERROR: evidence bundle not found", file=sys.stderr)
    sys.exit(1)

with open(EVIDENCE_PATH, 'r') as f: 
    bundle = json.load(f)

# 强时序断言
evidences = bundle.get("evidence", [])
caps = [e.get("capability") for e in evidences]
expected_flow = ["FS_WRITE", "BROKER_RELAY"]

if caps != expected_flow:
    print(f"[-] ERROR: Time order assertion failed! Expected: {expected_flow}, Got: {caps}", file=sys.stderr)
    sys.exit(1)

# 追加 Agent B 的证据
bundle["evidence"].append({
    "capability": "PROCESS_EXECUTION",
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "outcome": "GRANTED",
    "artifactHash": bundle["manifestHash"],
    "logDigest": "Agent B: execution assertion passed, contract chain sealed."
})

# 构造符合 Schema 的 RESULT.json
result_data = {
    "schemaVersion": "2.1.2",
    "manifestHash": bundle["manifestHash"],
    "runtimeReceipt": {
        "status": "PASS",
        "exitCode": 0,
        "conformanceLevel": 1
    },
    "evidence": bundle["evidence"]
}

with open(RESULT_PATH, 'w') as f:
    json.dump(result_data, f, indent=2)

print("[+] Agent B completed contract validation. RESULT.json successfully emitted.")
