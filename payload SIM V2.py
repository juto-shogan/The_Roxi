import os
import sys
import time
import random
import base64
import json
import zlib
from hashlib import sha256
from Crypto.Cipher import AES, ChaCha20_Poly1305
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# === CONFIGURATION ===
MASTER_KEY = "SuperSecretKey"  # Change this for deployment
PAYLOAD_STORAGE = "payloads.dat"
LOG_FILE = "payload_sim.log"
SELF_DESTRUCT = True  # Auto-delete after execution (set False to disable)

# === MULTI-STAGE PAYLOADS ===
MULTI_STAGE_PAYLOADS = {
    "stage1": [
        "echo 'Stage 1 Payload: Initial Reconnaissance...'",
        "echo 'Stage 1 Payload: System Enumeration...'"
    ],
    "stage2": [
        "echo 'Stage 2 Payload: Establishing Persistence...'",
        "echo 'Stage 2 Payload: Credential Dumping...'"
    ],
    "stage3": [
        "echo 'Stage 3 Payload: Data Exfiltration...'",
        "echo 'Stage 3 Payload: Cleanup Operations...'"
    ]
}

# === UTILITIES ===

def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def derive_key(passphrase, salt, rounds=100_000):
    return PBKDF2(passphrase, salt, dkLen=32, count=rounds)


def encrypt_triple(payload):
    # Compress payload before encryption (level 8)
    compressed = zlib.compress(payload.encode(), level=8)
    
    # Layer 1: AES-256 EAX
    salt1 = get_random_bytes(16)
    key1 = derive_key(MASTER_KEY, salt1)
    cipher1 = AES.new(key1, AES.MODE_EAX)
    ciphertext1, tag1 = cipher1.encrypt_and_digest(compressed)
    
    # Layer 2: ChaCha20-Poly1305
    salt2 = get_random_bytes(16)
    key2 = derive_key(MASTER_KEY, salt2)
    cipher2 = ChaCha20_Poly1305.new(key=key2)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(ciphertext1)
    
    # Layer 3: AES-256 EAX
    salt3 = get_random_bytes(16)
    key3 = derive_key(MASTER_KEY, salt3)
    cipher3 = AES.new(key3, AES.MODE_EAX)
    ciphertext3, tag3 = cipher3.encrypt_and_digest(ciphertext2)
    
    payload_package = {
        "salt1": base64.b64encode(salt1).decode(),
        "nonce1": base64.b64encode(cipher1.nonce).decode(),
        "tag1": base64.b64encode(tag1).decode(),
        "salt2": base64.b64encode(salt2).decode(),
        "nonce2": base64.b64encode(cipher2.nonce).decode(),
        "tag2": base64.b64encode(tag2).decode(),
        "salt3": base64.b64encode(salt3).decode(),
        "nonce3": base64.b64encode(cipher3.nonce).decode(),
        "tag3": base64.b64encode(tag3).decode(),
        "ciphertext": base64.b64encode(ciphertext3).decode()
    }
    return json.dumps(payload_package)


def decrypt_triple(payload_package):
    package = json.loads(payload_package)
    
    salt1 = base64.b64decode(package["salt1"])
    nonce1 = base64.b64decode(package["nonce1"])
    tag1 = base64.b64decode(package["tag1"])
    
    salt2 = base64.b64decode(package["salt2"])
    nonce2 = base64.b64decode(package["nonce2"])
    tag2 = base64.b64decode(package["tag2"])
    
    salt3 = base64.b64decode(package["salt3"])
    nonce3 = base64.b64decode(package["nonce3"])
    tag3 = base64.b64decode(package["tag3"])
    
    ciphertext3 = base64.b64decode(package["ciphertext"])
    
    # Layer 3 Decrypt
    key3 = derive_key(MASTER_KEY, salt3)
    cipher3 = AES.new(key3, AES.MODE_EAX, nonce=nonce3)
    ciphertext2 = cipher3.decrypt_and_verify(ciphertext3, tag3)
    
    # Layer 2 Decrypt
    key2 = derive_key(MASTER_KEY, salt2)
    cipher2 = ChaCha20_Poly1305.new(key=key2, nonce=nonce2)
    ciphertext1 = cipher2.decrypt_and_verify(ciphertext2, tag2)
    
    # Layer 1 Decrypt
    key1 = derive_key(MASTER_KEY, salt1)
    cipher1 = AES.new(key1, AES.MODE_EAX, nonce=nonce1)
    compressed = cipher1.decrypt_and_verify(ciphertext1, tag1)
    
    # Decompress the payload
    payload = zlib.decompress(compressed).decode()
    return payload

# === PAYLOAD MANAGEMENT ===

def store_encrypted_payloads():
    encrypted = {
        stage: [encrypt_triple(p) for p in payloads]
        for stage, payloads in MULTI_STAGE_PAYLOADS.items()
    }
    with open(PAYLOAD_STORAGE, "w") as f:
        json.dump(encrypted, f)
    log_event("Stored encrypted multi-stage payloads (triple-encrypted with compression level 8).")


def load_payloads():
    with open(PAYLOAD_STORAGE, "r") as f:
        encrypted = json.load(f)
    decrypted = {
        stage: [decrypt_triple(p) for p in payloads]
        for stage, payloads in encrypted.items()
    }
    log_event("Decrypted multi-stage payloads successfully.")
    return decrypted

def execute_payload(payload):
    log_event(f"Executing payload: {payload}")
    os.system(payload)

def execute_multi_stage(payloads):
    for stage in sorted(payloads.keys()):
        log_event(f"--- Executing {stage} ---")
        for payload in payloads[stage]:
            anti_analysis_delay()
            execute_payload(payload)

def anti_analysis_delay():
    delay = random.randint(2, 6)
    log_event(f"Anti-analysis delay: Sleeping for {delay} seconds...")
    time.sleep(delay)

def self_destruct():
    log_event("Triggering self-destruct sequence...")
    try:
        os.remove(PAYLOAD_STORAGE)
        os.remove(LOG_FILE)
        os.remove(__file__)
    except Exception as e:
        log_event(f"Self-destruct failed: {e}")

# === MAIN FUNCTION ===

def main():
    if not os.path.exists(PAYLOAD_STORAGE):
        log_event("Payloads not found; encrypting and storing...")
        store_encrypted_payloads()
    else:
        log_event("Encrypted payloads found; loading...")
    
    payloads = load_payloads()
    
    anti_analysis_delay()
    execute_multi_stage(payloads)
    
    if SELF_DESTRUCT:
        anti_analysis_delay()
        self_destruct()

# === ENTRY POINT ===
if __name__ == "__main__":
    main()