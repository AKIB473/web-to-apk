"""
ci/save_secrets.py — Saves keystore as GitHub Secrets automatically.
Called by the Setup Keystore workflow.
"""

import os, sys, base64, json, urllib.request, urllib.error

token  = os.environ["GH_TOKEN"]
repo   = os.environ["GH_REPO"]
sp     = os.environ["STORE_PASSWORD"]
alias  = os.environ["KEY_ALIAS"]
kp     = os.environ["KEY_PASSWORD"]

# Read keystore file
jks_path = "release.jks"
if not os.path.exists(jks_path):
    print(f"ERROR: {jks_path} not found")
    sys.exit(1)

with open(jks_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

print(f"Keystore: {len(b64)} chars base64")

# ── Get repo public key for secret encryption ──────────────────────────────
def gh_get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def gh_put(url, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28"
    })
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code

# Get public key
pub = gh_get(f"https://api.github.com/repos/{repo}/actions/secrets/public-key")
key_id  = pub["key_id"]
pub_key = pub["key"]

print(f"Repo public key ID: {key_id}")

# Encrypt secrets using libsodium (PyNaCl)
try:
    from nacl import encoding, public as nacl_public

    def encrypt(pub_key_b64, value):
        pk_bytes = base64.b64decode(pub_key_b64)
        pk = nacl_public.PublicKey(pk_bytes)
        box = nacl_public.SealedBox(pk)
        encrypted = box.encrypt(value.encode("utf-8"))
        return base64.b64encode(encrypted).decode()

    secrets = {
        "KEYSTORE_BASE64":        b64,
        "SIGNING_STORE_PASSWORD": sp,
        "SIGNING_KEY_ALIAS":      alias,
        "SIGNING_KEY_PASSWORD":   kp,
    }

    for name, value in secrets.items():
        encrypted = encrypt(pub_key, value)
        status = gh_put(
            f"https://api.github.com/repos/{repo}/actions/secrets/{name}",
            {"encrypted_value": encrypted, "key_id": key_id}
        )
        if status in [201, 204]:
            print(f"  Saved secret: {name}")
        else:
            print(f"  ERROR saving {name}: HTTP {status}")

    print("\nAll secrets saved. Your next build will use this permanent keystore.")

except ImportError:
    # PyNaCl not installed — print instructions instead
    print("\nNote: PyNaCl not available. Add secrets manually:")
    print(f"\n  KEYSTORE_BASE64 = {b64[:50]}...")
    print(f"  SIGNING_STORE_PASSWORD = {sp}")
    print(f"  SIGNING_KEY_ALIAS = {alias}")
    print(f"  SIGNING_KEY_PASSWORD = {kp}")
    print("\nGo to: Settings > Secrets and variables > Actions")
