from django.contrib import admin
from .models import Conversation,CodeGenrator,ContentGenrator
# Register your models here.
admin.site.register(Conversation)
admin.site.register(CodeGenrator)
admin.site.register(ContentGenrator)