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

# Используем версию NDK, которая точно есть в репозиториях
android.ndk = 25.2.9519653
android.build_tools_version = 33.0.0
# Явно указываем SDK, чтобы не было 404 ошибки при поиске
android.sdk = 33
