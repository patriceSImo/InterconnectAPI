from django.db import models

class APIStatsSelforce(models.Model):
    id_stats_selforce = models.AutoField(primary_key=True)
    id_comete_sender = models.CharField(max_length=50,blank=True)  # Id envoyé par comete pour le suivi
    salesforce_id = models.CharField(max_length=50,blank=True)  # Salesforce ID
    salesforce_datetime = models.CharField(max_length=191, blank=True) # Date et heure de l'appel Salesforce
    final_comete_status = models.CharField(max_length=50, blank=True) # Status final du traitement d'un cas afin de faciliter la recherche
    comete_status = models.JSONField(null=True, blank=True, default=dict)  # Stocke l'historique des statuts Comete
    comete_status_detail = models.JSONField(null=True, blank=True, default=dict)  # Stocke les détails des statuts Comete
    nb_attempt = models.IntegerField(null=True, blank=True)  # Nombre de tentatives
    ulex_id = models.TextField(blank=True)  # ID Ulex
    ulex_datetime = models.CharField(max_length=191, blank=True)  # Date et heure Ulex
    inocx_id = models.TextField(blank=True)  # ID Inocx
    inocx_datetime = models.CharField(max_length=191, blank=True)  # Date et heure Inocx
    inocx_status = models.JSONField(null=True, blank=True, default=dict) # Statut Inocx (NRP, Occupé, Traité)
    call_duration_details =models.JSONField(null=True, blank=True, default=dict)
    call_duration = models.CharField(max_length=191, blank=True)
    retour_ulex = models.JSONField(null=True, blank=True, default=dict)
    update_salesforce = models.JSONField(null=True, blank=True, default=dict) 
    raison_crash = models.TextField(blank=True)
    create_at = models.CharField(max_length=25, blank=True)

    class Meta:
        db_table = 'api_stats_selforce'

    def __str__(self):
        # Utilisation de __dict__ pour récupérer tous les attributs de l'instance
        fields = ', '.join([f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"APIStatsSelforce({fields})"