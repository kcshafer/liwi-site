from django.contrib import admin

from registration.models import User, SecurityQuestion

admin.site.register(User)
admin.site.register(SecurityQuestion)