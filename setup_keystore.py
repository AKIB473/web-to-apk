"""
Setup keystore for Android signing.

Strategy:
  - If KEYSTORE_BASE64 secret is set: decode it and configure signing.
  - If not set (no secret): generate a temporary self-signed keystore for demo builds.
    The APK will be signed but NOT suitable for Play Store without a real keystore.

Usage: python3 setup_keystore.py
"""

import os
import base64
import subprocess
import pathlib

GRADLE_PATH = pathlib.Path("android/app/build.gradle")
KEYSTORE_PATH = pathlib.Path("android/app/release.keystore")

# ── Detect if real keystore is available ──────────────────────────────────────
keystore_b64    = os.environ.get("KEYSTORE_BASE64", "").strip()
store_pass      = os.environ.get("SIGNING_STORE_PASSWORD", "").strip()
key_alias       = os.environ.get("SIGNING_KEY_ALIAS", "").strip()
key_pass        = os.environ.get("SIGNING_KEY_PASSWORD", "").strip()

has_real_keystore = bool(keystore_b64 and store_pass and key_alias and key_pass)

if has_real_keystore:
    # ── Use provided keystore ─────────────────────────────────────────────────
    print("Using keystore from KEYSTORE_BASE64 secret...")
    try:
        keystore_bytes = base64.b64decode(keystore_b64)
        KEYSTORE_PATH.write_bytes(keystore_bytes)
        print(f"  Keystore written: {KEYSTORE_PATH} ({len(keystore_bytes)} bytes)")
    except Exception as e:
        print(f"  ERROR decoding keystore: {e}")
        raise SystemExit(1)

else:
    # ── Generate a demo keystore ──────────────────────────────────────────────
    print("No KEYSTORE_BASE64 secret found — generating demo keystore...")
    store_pass = "android"
    key_alias  = "androiddebugkey"
    key_pass   = "android"

    result = subprocess.run([
        "keytool", "-genkeypair",
        "-keystore", str(KEYSTORE_PATH),
        "-alias",    key_alias,
        "-keyalg",   "RSA",
        "-keysize",  "2048",
        "-validity", "365",
        "-storepass", store_pass,
        "-keypass",   key_pass,
        "-dname",     "CN=WebToAPK Demo, OU=Dev, O=Demo, L=City, S=State, C=US",
        "-storetype", "JKS",
        "-noprompt",
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("  keytool stdout:", result.stdout)
        print("  keytool stderr:", result.stderr)
        raise SystemExit(1)

    print(f"  Demo keystore generated: {KEYSTORE_PATH}")
    print("  NOTE: This APK is signed with a demo key. For Play Store, add real secrets.")

    # Write passwords to env file for gradle to read
    os.environ["SIGNING_STORE_PASSWORD"] = store_pass
    os.environ["SIGNING_KEY_ALIAS"]      = key_alias
    os.environ["SIGNING_KEY_PASSWORD"]   = key_pass

# ── Append signing config to build.gradle ────────────────────────────────────
gradle_content = GRADLE_PATH.read_text()

if "signingConfigs" not in gradle_content:
    signing_block = f"""
android {{
    signingConfigs {{
        release {{
            storeFile file("release.keystore")
            storePassword System.getenv("SIGNING_STORE_PASSWORD") ?: "{store_pass}"
            keyAlias      System.getenv("SIGNING_KEY_ALIAS")      ?: "{key_alias}"
            keyPassword   System.getenv("SIGNING_KEY_PASSWORD")   ?: "{key_pass}"
        }}
    }}
    buildTypes {{
        release {{
            minifyEnabled false
            shrinkResources false
            signingConfig signingConfigs.release
        }}
    }}
}}
"""
    GRADLE_PATH.write_text(gradle_content + signing_block)
    print(f"  Signing config appended to {GRADLE_PATH}")
else:
    print(f"  signingConfigs already present in {GRADLE_PATH}")

print("Keystore setup complete.")
