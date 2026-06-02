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

# Фиксируем API и Build Tools
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0

[buildozer]
log_level = 2
warn_on_root = 1
