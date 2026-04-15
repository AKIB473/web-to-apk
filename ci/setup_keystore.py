"""
ci/setup_keystore.py — Signing setup for GitHub Actions.

Priority:
  1. If KEYSTORE_BASE64 + all signing secrets are set → use real keystore (Play Store ready)
  2. If not → generate a fresh demo keystore for this build (works on any Android device)

The demo keystore changes each build, so it cannot be used for Play Store updates.
Run the "Setup Keystore" workflow once to get a permanent key.
"""

import os, sys, base64, subprocess, pathlib

GRADLE  = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "android/app/build.gradle")
KEYFILE = pathlib.Path("android/app/release.keystore")

b64   = os.environ.get("KEYSTORE_BASE64", "").strip()
sp    = os.environ.get("SIGNING_STORE_PASSWORD", "").strip()
alias = os.environ.get("SIGNING_KEY_ALIAS", "").strip()
kp    = os.environ.get("SIGNING_KEY_PASSWORD", "").strip()

real = bool(b64 and sp and alias and kp)

if real:
    print("[signing] Using permanent keystore from secrets...")
    raw = base64.b64decode(b64)
    KEYFILE.write_bytes(raw)
    print(f"  Keystore: {KEYFILE} ({len(raw):,} bytes)")
    label = "PERMANENT KEY — Play Store ready"
else:
    print("[signing] No secrets found → generating demo keystore for this build...")
    print("  Tip: Run the 'Setup Keystore' workflow to get a permanent key for Play Store.")
    sp, alias, kp = "buildpass", "buildkey", "buildpass"
    r = subprocess.run([
        "keytool", "-genkeypair",
        "-keystore", str(KEYFILE),
        "-alias", alias,
        "-keyalg", "RSA", "-keysize", "2048", "-validity", "1",
        "-storepass", sp, "-keypass", kp,
        "-dname", "CN=Demo, OU=Dev, O=Demo, L=X, ST=X, C=US",
        "-storetype", "JKS", "-noprompt",
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR:", r.stderr[-600:])
        sys.exit(1)
    print(f"  Demo keystore: {KEYFILE} ({KEYFILE.stat().st_size:,} bytes)")
    # Export to GITHUB_ENV so Gradle steps can read them
    genv = os.environ.get("GITHUB_ENV", "")
    if genv:
        with open(genv, "a") as f:
            f.write(f"SIGNING_STORE_PASSWORD={sp}\n")
            f.write(f"SIGNING_KEY_ALIAS={alias}\n")
            f.write(f"SIGNING_KEY_PASSWORD={kp}\n")
    label = "DEMO KEY — sideload only"

print(f"  Mode: {label}")

# Write signing block to build.gradle
content = GRADLE.read_text()
if "signingConfigs" in content:
    print("[gradle] signingConfigs already present — skipping")
    sys.exit(0)

block = f"""
android {{
    signingConfigs {{
        release {{
            storeFile file("release.keystore")
            storePassword System.getenv("SIGNING_STORE_PASSWORD") ?: "{sp}"
            keyAlias      System.getenv("SIGNING_KEY_ALIAS")      ?: "{alias}"
            keyPassword   System.getenv("SIGNING_KEY_PASSWORD")   ?: "{kp}"
        }}
    }}
    buildTypes {{
        release {{
            minifyEnabled   true
            shrinkResources true
            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
            signingConfig signingConfigs.release
        }}
    }}
}}
"""
GRADLE.write_text(content + block)
print(f"[gradle] Signing config written to {GRADLE}")
