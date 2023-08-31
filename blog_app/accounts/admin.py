from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.template.defaultfilters import slugify

from .forms import BlogAppUserCreationForm, BlogAppUserChangeForm
from .models import BlogAppUser, Profile

UserModel = get_user_model()

@admin.register(BlogAppUser)
class BlogAppUserAdmin(UserAdmin):
    add_form = BlogAppUserCreationForm
    form = BlogAppUserChangeForm
    model = UserModel
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('full_name',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.slug:
    #         obj.slug = slugify(obj.full_name)
    #     super().save_model(request, obj, form, change)
    #
    # search_fields = ('first_name', 'last_name')
