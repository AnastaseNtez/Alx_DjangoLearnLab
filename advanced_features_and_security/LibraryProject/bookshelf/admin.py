from django.contrib import admin
# Cleaned up imports: only necessary ones are kept
from .models import Book, Library, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Keep for CustomUserAdmin
from .models import CustomUser # Import CustomUser for registration

# --- 1. Custom User Admin Configuration ---
class CustomUserAdmin(BaseUserAdmin):
    """
    Define a custom admin for the CustomUser model, inheriting from Django's BaseUserAdmin.
    """
    
    # Add custom fields to the list display
    list_display = BaseUserAdmin.list_display + ('date_of_birth', 'is_staff', 'is_active')
    
    # Customize the main edit form fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Customize the "Add User" form fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


# --- 2. Book Admin Configuration ---

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model, including created_by tracking.
    """
    list_display = ['title', 'author', 'publication_year', 'created_by', 'created_at']
    list_filter = ['publication_year', 'created_at', 'created_by']
    search_fields = ['title', 'author', 'isbn', 'description']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'isbn', 'description')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user on creation."""
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# --- 3. Library Admin Configuration ---

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """
    Admin interface for Library model.
    """
    list_display = ['name', 'location', 'book_count']
    search_fields = ['name', 'location']
    filter_horizontal = ['books'] # Nicer widget for Many-to-Many fields
    
    def book_count(self, obj):
        """Display number of books in the library."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


# --- 4. UserProfile Admin Configuration ---

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ['user', 'role', 'date_joined']
    list_filter = ['role', 'date_joined']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Additional Info', {
            'fields': ('bio', 'date_joined'),
        }),
    )
    
    readonly_fields = ['date_joined']