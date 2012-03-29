from django.contrib import admin
from TCC.automation.models import *

class ClientJobAdmin(admin.ModelAdmin):
    list_display = ('job_no', 'type_of_consultancy','receipt_no' )
    search_fields = ('job_no',)
    list_filter = ['date']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','address_1','address_2','state','city' )
    search_fields = ('job_no',)
    list_filter = ['date']

class AmountAdmin(admin.ModelAdmin):
    list_display = ('job_no', 'lab','field','total' )
    search_fields = ('job_no',)
    list_filter = ['job_no']


class VariableAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','name' )
    search_fields = ('names',)
    list_filter = ['title']

admin.site.register(Amount, AmountAdmin)
admin.site.register(ClientJob, ClientJobAdmin)
admin.site.register(Variable, VariableAdmin)
