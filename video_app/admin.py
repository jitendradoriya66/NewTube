from django.contrib import admin
from video_app.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(category)
admin.site.register(LikeDislike)
admin.site.register(watchLetter)
admin.site.register(Subscription)


