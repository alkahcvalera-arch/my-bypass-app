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

# Эти параметры критичны для того, чтобы сборка не падала
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
# Не указываем здесь android.ndk, чтобы использовался системный из YAML

[buildozer]
log_level = 2
warn_on_root = 1
