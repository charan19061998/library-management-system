from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, BorrowRequest, BorrowHistory

# Register models with custom admin classes

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'available_copies')  # Explicit fields to display

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date', 'status')  
    
@admin.register(BorrowHistory)
class BorrowHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at')  