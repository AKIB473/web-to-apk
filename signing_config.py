"""
Appends signing config to android/app/build.gradle.
Called by CI workflow — avoids heredoc syntax in YAML.
"""
import sys
import pathlib

gradle_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "android/app/build.gradle")

signing_block = """
android {
    signingConfigs {
        release {
            storeFile     file("release.keystore")
            storePassword System.getenv("SIGNING_STORE_PASSWORD")
            keyAlias      System.getenv("SIGNING_KEY_ALIAS")
            keyPassword   System.getenv("SIGNING_KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            minifyEnabled   true
            shrinkResources true
            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
            signingConfig signingConfigs.release
        }
        debug {
            applicationIdSuffix ".debug"
            versionNameSuffix   "-debug"
            debuggable          true
        }
    }
}
"""

current = gradle_path.read_text()
gradle_path.write_text(current + signing_block)
print(f"Signing config appended to {gradle_path}")
