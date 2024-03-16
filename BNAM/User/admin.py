from django.contrib import admin
from django.contrib.auth import get_user_model
from Budget.models import Budget

UserProfile = get_user_model()

class BudgetInline(admin.TabularInline):
    model = Budget

class UserAdmin(admin.ModelAdmin):
    inlines = [
        BudgetInline,
    ]
    search_fields = ['userprofile']

admin.site.register(UserProfile, UserAdmin)
