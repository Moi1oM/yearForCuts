from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, RegisterForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = RegisterForm

    list_display = ('email', 'nickname','hidden','is_staff', 'is_admin', 'public_id')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname',)}),
        ('Staff', {'fields': ('is_staff',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Pubic_id', {'fields': ('public_id',)}),
        ('Hidden', {'fields': ('hidden',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)