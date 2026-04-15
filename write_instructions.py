"""Write keystore setup instructions file. Used by generate_keystore workflow."""
import pathlib

instructions = """================================================================
KEYSTORE SETUP - READ THIS CAREFULLY
================================================================

Your keystore has been generated. Follow these steps NOW:

STEP 1: Add GitHub Secrets
---------------------------
Go to: Your Repo > Settings > Secrets and variables > Actions
Click "New repository secret" and add ALL FOUR secrets:

  Secret name: KEYSTORE_BASE64
  Value: [copy the ENTIRE contents of keystore_base64.txt]

  Secret name: SIGNING_STORE_PASSWORD
  Value: [the store password you entered when running this workflow]

  Secret name: SIGNING_KEY_ALIAS
  Value: [the key alias you entered - e.g. release-key]

  Secret name: SIGNING_KEY_PASSWORD
  Value: [the key password you entered]

STEP 2: Save your keystore file
--------------------------------
Download release.jks and store it safely FOREVER.
If you lose it, you cannot update your app on Google Play.

Recommended backup locations:
  - Password manager (1Password, Bitwarden, etc.)
  - Encrypted cloud storage
  - USB drive in a safe physical location

STEP 3: Push to main branch
----------------------------
Once all 4 secrets are added, push any commit to main.
Your build will produce a REAL signed APK and AAB.

================================================================
NEVER share your keystore or passwords with anyone.
NEVER commit release.jks or keystore_base64.txt to git.
The artifact expires in 24 hours - download it NOW.
================================================================
"""

pathlib.Path("KEYSTORE_SETUP_INSTRUCTIONS.txt").write_text(instructions)
print("Instructions written.")
