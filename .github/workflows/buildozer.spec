[app]
title = Ghost Reader
package.name = ghostreader
package.domain = org.omerbrod
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,android
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
