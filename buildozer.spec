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

android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.meta_data = service:org.omerbrod.ghostreader.NotificationService

[buildozer]
log_level = 2
