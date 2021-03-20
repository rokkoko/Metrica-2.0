from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClaimTopic, Claim

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Claim)
admin.site.register(ClaimTopic)
