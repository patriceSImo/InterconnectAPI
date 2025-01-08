class MultiDBRouter:
    """
    Un routeur qui dirige les lectures, écritures et migrations vers les bases de données appropriées.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'wifirstAPI' and model.__name__ in ['APICallWifirst','InoCxTask','APIStatsSelforce','APIRequestLog']:
            return 'wifirst'  # lecture dans 'wifirst' pour APICallWifirst et autres
        return 'python'  # Lectures dans 'python'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'wifirstAPI' and model.__name__ in ['APICallWifirst','InoCxTask','APIStatsSelforce','APIRequestLog']:
            return 'wifirst'  # Écritures dans 'wifirst' pour APICallWifirst
        return 'python'  # Écritures dans 'python' pour les autres modèles

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ['python', 'wifirst']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in ['apicallwifirst','inocxtask','apistatsselforce','apirequestlog']:
            return db == 'wifirst'
        elif model_name in []:
            return db==None
        else:
            return db == 'python'
