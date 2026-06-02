[app]
# (str) Title of your application
title = Bypass

# (str) Package name
package.name = bypass

# (str) Package domain (needed for android/ios packaging)
package.domain = org.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include everything just in case)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Добавьте сюда библиотеку hostpython3, иначе сборка упадет
requirements = python3,kivy

# (list) Permissions
android.permissions = INTERNET

# (str) Supported orientation
orientation = portrait

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
