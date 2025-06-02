from django.contrib import admin
from .models import *
from .forms import *



class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1  # Number of empty forms to display for adding new attachments
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


class SmartKPIAdmin(admin.ModelAdmin):
    list_display = ('kpi', 'first_half_percent', 'first_half_unit', 'second_half_percent', 'second_half_unit', 'budget')
    list_filter = ('kpi__office',)  # Filter by related Office through KPI
    inlines = [AttachmentInline]



admin.site.register(OPCR_Smart_kpi)
admin.site.register(Organization_Outcome)
admin.site.register(Pillars)
admin.site.register(KPI)
admin.site.register(Office)
# admin.site.register(SmartKPI)
admin.site.register(DPCR)
admin.site.register(Employee)
admin.site.register(Division)
admin.site.register(IPCR_OPCR)
admin.site.register(ActivitiesOPCR)
admin.site.register(ActivitiesDPCR)
admin.site.register(Pillar_kpi)
admin.site.register(OPCR)
admin.site.register(IPCR_DPCR)
admin.site.register(Attachment)
admin.site.register(Cluster)

