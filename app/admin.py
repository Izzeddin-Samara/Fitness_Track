from django.contrib import admin
from .models import Coach

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'bio', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email')

