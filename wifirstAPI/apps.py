from django.apps import AppConfig

class WifirstAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wifirstAPI'

    def ready(self):
        import wifirstAPI.Scripts_auto.scriptInocx
        import wifirstAPI.Scripts_auto.monitor_wifirst
        import wifirstAPI.Scripts_auto.scriptUlexInit
        