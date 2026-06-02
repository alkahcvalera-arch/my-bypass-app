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
android.build_tools_version = 33.0.0

# Указываем пути к локальным папкам, которые мы создали
android.sdk_path = .buildozer/android/platform/android-sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/28.0.13004108

[buildozer]
log_level = 2
warn_on_root = 1
