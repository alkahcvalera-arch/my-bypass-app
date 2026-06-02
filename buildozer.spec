[app]
title = Bypass
package.name = bypass
package.domain = org.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
android.permissions = INTERNET
orientation = portrait

android.api = 33
android.minapi = 21
# Важно: если здесь не указать ndk, он может попытаться его скачать. 
# Но с BUILDOZER_SKIP_SDK_INSTALL он будет обязан взять путь из ENV.
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724
android.sdk_path = /usr/local/lib/android/sdk

[buildozer]
log_level = 2
warn_on_root = 1
