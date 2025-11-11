from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

# --- Custom Admin for CustomUser (Step 4) ---
class CustomUserAdmin(UserAdmin):
    """
    Define the admin configuration for the CustomUser model.
    """
    # Define fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

    # Fields to include in the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Fields to include in the "Change User" form
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Unregister the default User model if it was registered (good practice when replacing it)
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Register the custom models
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Book model (including the new FK field)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'created_by')
    list_filter = ('publication_year',)
    search_fields = ('title', 'author')