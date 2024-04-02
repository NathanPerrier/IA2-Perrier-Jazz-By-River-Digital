from ..config import *


class ForgotPasswordAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_code', 'expiration_time')
    search_fields = ('user', 'reset_code', 'expiration_time')
    