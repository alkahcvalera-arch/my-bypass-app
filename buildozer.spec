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
# Фиксируем путь, где buildozer ТОЧНО должен найти aidl
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.build_tools_version = 33.0.0

[buildozer]
log_level = 2
warn_on_root = 1
