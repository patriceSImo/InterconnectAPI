from django.apps import AppConfig

class xxxxxxxAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wxxxxxtAPI'

    def ready(self):
        import wxxxxxtAPI.Scripts_auto.scriptInocx
        import wxxxxxtAPI.Scripts_auto.monitor_wxxxxxt
        import wxxxxxtAPI.Scripts_auto.scriptuxxxInit
        