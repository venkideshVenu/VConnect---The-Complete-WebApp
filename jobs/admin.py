from django.contrib import admin
from .models import TagModel, JobModel, ApplicantModel

@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name']
    ordering = ['name']

@admin.register(JobModel)
class JobModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'type', 'location', 'created']
    list_filter = ['type', 'created', 'tags']
    search_fields = ['title', 'description', 'location']
    raw_id_fields = ['owner']
    filter_horizontal = ['tags']
    date_hierarchy = 'created'
    list_per_page = 20
    
    def get_queryset(self, request):
        # Optimize query by prefetching related fields
        return super().get_queryset(request).select_related('owner')

@admin.register(ApplicantModel)
class ApplicantModelAdmin(admin.ModelAdmin):
    list_display = ['get_applicant_name', 'job', 'status', 'is_read', 'created']
    list_filter = ['status', 'is_read', 'created']
    search_fields = ['user__user__email', 'user__user__first_name', 'user__user__last_name', 'job__title']
    raw_id_fields = ['user', 'job']
    date_hierarchy = 'created'
    list_per_page = 20
    
    def get_applicant_name(self, obj):
        return obj.user.user.get_full_name() if obj.user else 'Deleted User'
    get_applicant_name.short_description = 'Applicant'
    
    def get_queryset(self, request):
        # Optimize query by prefetching related fields
        return super().get_queryset(request).select_related('user__user', 'job')