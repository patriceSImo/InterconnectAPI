from django.contrib import admin
from .models.apiCallModel import APICall, APICallStatistics
from .models.apiTokensModels import APIToken

class APICallAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'method', 'status', 'created_at')
    search_fields = ('endpoint', 'method', 'status')

class APICallStatisticsAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'method', 'status', 'created_at')
    search_fields = ('endpoint', 'method', 'status')

class APITokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'created_at', 'expires_at')
    search_fields = ('token',)

admin.site.register(APICall, APICallAdmin)
admin.site.register(APICallStatistics, APICallStatisticsAdmin)
admin.site.register(APIToken, APITokenAdmin)
