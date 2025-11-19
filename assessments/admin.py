from django.contrib import admin
from .models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'crack_percentage', 'pothole_probability', 'severity', 'condition_score', 'analysis_status', 'created_at')
	list_filter = ('analysis_status', 'severity', 'created_at')
	readonly_fields = ('created_at', 'updated_at')
	search_fields = ('user__username',)
