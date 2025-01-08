import os,re, sys,django
import mysql.connector
import requests
from datetime import datetime, timezone,timedelta
import logging
import pytz
import json
from django.forms.models import model_to_dict

# Ajout du chemin vers le dossier contenant 'wifirstAPI'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    # Configuration de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cometeAPIs.settings')
    django.setup()
except Exception as e:
    print(f"Erreur lors de l'initialisation de Django : {e}")

# Importez les modèles après avoir configuré Django
from wifirstAPI.models.scriptsModel import InoCxTask
from wifirstAPI.models.statsModels import APIStatsSelforce

# Configuration des logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Correspondance entre `displayed_number` et `id_campagne`
campaign_map = {
    '+33170704670': 114,
    '+33170704673': 117,
    '+33170809848': 115,
    '+33172753400': 116,
    '+33173309572': 118,
    '+33186650619': 120,
    '+33186650621': 121
}

id_masque = 44
priorite = 30

# URL de l'API (initialement sans `id_campagne`)
url_template = "https://comete.ino.cx/api/voicecampaigns/{}/targets"

headers = {
    "X-INOCX-TOKEN": "11a1b8c84f82416f9abbe4bdebb3d3a6",
    "X-INOCX-SECRET": "a18936fc93ce4806b5393505f9ef0fe8",
    "X-INOCX-USERNAME": "matthieu.ganivet@comete.ai",
    "Content-Type": "application/json",
    "User-Agent": "Server-To-Server-Request"
}




from datetime import datetime
import logging
import re

def get_date_conv(data):
    try:
        # Vérifier si la chaîne est au format 'DD/MM/YYYY HH:MM:SS'
        if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", data):
            # Convertir la chaîne au format 'DD/MM/YYYY HH:MM:SS' en objet datetime
            date_obj = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            # Reformatage de l'objet datetime en 'YYYY-MM-DD HH:MM:SS'
            date_format = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            return date_format

    except ValueError as e:
        logging.error(f"Erreur de conversion de la date : {e}")
        return None

def update_stats(id, element, value):
    # Récupérer l'instance correspondant à id_comete_sender
    instance = APIStatsSelforce.objects.filter(id_comete_sender=id).first()

    # Vérifier que l'instance existe avant de procéder
    if not instance:
        raise ValueError("L'instance avec cet id_comete_sender n'existe pas")

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mettre à jour 'comete_status'
    if element == "comete_status":
        if not isinstance(instance.comete_status, dict):
            instance.comete_status = {}
        # Ajouter la nouvelle valeur avec un index incrémental et un horodatage
        new_key = str(len(instance.comete_status) + 1)
        instance.comete_status[new_key] = {"value": value, "timestamp": current_time}

    # Mettre à jour 'comete_status_detail'
    elif element == "comete_status_detail":
        if not isinstance(instance.comete_status_detail, dict):
            instance.comete_status_detail = {}
        new_key = str(len(instance.comete_status_detail) + 1)
        instance.comete_status_detail[new_key] = {"value": value, "timestamp": current_time}

    # Ajouter d'autres éléments à mettre à jour comme 'inocx_status', 'call_duration', etc.
    elif element == "inocx_status":
        if not isinstance(instance.inocx_status, dict):
            instance.inocx_status = {}
        new_key = str(len(instance.inocx_status) + 1)
        instance.inocx_status[new_key] = {"value": value, "timestamp": current_time}
        
    elif element == "call_duration_details":
        if not isinstance(instance.call_duration, dict):
            instance.call_duration = {}
        new_key = str(len(instance.call_duration) + 1)
        instance.call_duration_details[new_key] = {"value": value, "timestamp": current_time}

    elif element == "retour_ulex":
        if not isinstance(instance.retour_ulex, dict):
            instance.retour_ulex = {}
        new_key = str(len(instance.retour_ulex) + 1)
        instance.retour_ulex[new_key] = {"value": value, "timestamp": current_time}

    # Sauvegarder l'instance après mise à jour
    instance.save()

    return instance

def process_new_entry_inocx(data):
    data = model_to_dict(data)
    logging.debug(f"nouveau script avec les donnees{data}")
    try:
        # Identification du `id_campagne` en fonction du `displayed_number`
        displayed_number = data.get("displayed_number")
        id_campagne =114
        
        #aller chercher en BD
        if displayed_number in campaign_map :
            id_campagne = campaign_map.get(displayed_number)
        logging.debug(f"Numéro de la campagen séléctionnée est : {id_campagne}")
        
        if id_campagne is None:
            logging.error(f"Numéro affiché non reconnu : {displayed_number}")
            id_campagne = 144
        
        url = url_template.format(id_campagne)
        logging.debug(f"URL de la campagne: {url}")

        identifiant = data.get("id_api_call")
        contact = data.get("phone")
        logging.debug(f"le contact zzz1 envoyées à l'API: {contact}")

        # Obtenir l'heure actuelle dans le fuseau horaire de Paris
        paris_tz = pytz.timezone('Europe/Paris')
        now_in_paris = datetime.now(paris_tz)

        # Ajouter 20 secondes à l'heure actuelle
        date_creation = now_in_paris + timedelta(seconds=5)

        # Convertir l'heure au format UTC
        date_creation_utc = date_creation.astimezone(pytz.utc)

        targets = [{
            "data": {
                "identifiant": identifiant
            },
            "importDuplicates": True,
            "priority": priorite,
            "startDate": date_creation_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "campaignTargetLayoutId": id_masque,
            "numbers": [contact]
        }]
        
        payload = {
            "targets": targets
        }

        targets= json.dumps(payload)
        logging.debug(f"Données envoyées à l'API: {targets}")

        response = requests.post(url, headers=headers, data=targets)
        
        if response.status_code == 200:
            logging.info(f"Appel d'API réussi: {response.json()}")
            response_json = response.json()
            id_cible = response_json['value']['cleanTargets'][0]['id']
            #création de la table inocx_task_followup
            id_comete_sender= data.get("id_api_call")
            
            try:
                response_json = response.json()

                # Création de l'objet InoCxTask
                task_followup = InoCxTask.objects.create(
                    id_cible=id_cible,  # Adaptez cette clé en fonction de votre réponse JSON
                    attempt_number=0,  # Exemple : tentative initiale
                    id_comete_sender=data.get("id_api_call"),
                    contact_id=data.get("contact_id"),
                    id_salesforce=data.get("id_salesforce"),
                    datetime_alarm=get_date_conv(data.get("datetime_alarm")),
                    datetime_request=get_date_conv(data.get("datetime_request")),
                    displayed_number=data.get("displayed_number"),
                    company=data.get("company"),
                    contact=data.get("contact"),
                    location=data.get("location"),
                    phone=data.get("phone"),
                    pin_ulex_sender=data.get("pin_ulex_sender"),
                    status=response.status_code,
                    start_point="premier appel",
                    code_back_call="START",
                    response=response_json  # Stocker la réponse complète en JSON
                )
                logging.info(f"Objet InoCxTask créé avec succès : {task_followup}")
                
            except json.JSONDecodeError:
                logging.error("impossoble de décoder la reponse en json")
                APIStatsSelforce.objects.filter(id_comete_sender=id_comete_sender).update(raison_crash = e,)
            
            update_stats(id_comete_sender,"comete_status","inoCx CALL 1 Ok")
            APIStatsSelforce.objects.filter(id_comete_sender=id_comete_sender).update(final_comete_status="inoCx CALL 1 Ok")
            APIStatsSelforce.objects.filter(id_comete_sender=id_comete_sender).update(inocx_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inocx_id= id_cible)
            update_stats(id_comete_sender,"comete_status_datail",f"inoCx id_cible :{id_cible}")
            update_stats(id_comete_sender,"inocx_status","CALL CREATE")
            
        else:
            
            logging.error(f"Erreur lors de l'envoi des données à l'API. zzz Statut HTTP: {response.status_code}, Réponse: {response.text}")
            update_stats(id_comete_sender,"comete_status","inoCx KO")
            APIStatsSelforce.objects.filter(id=id_comete_sender).update(comete_status="inoCx KO")
            update_stats(id_comete_sender,"inocx_status",response.text)

    except Exception as e:
        logging.error(f"Erreur lors du traitement de l'entrée avec les données ffff fournies: {e}")
        update_stats(data.get("id_api_call"),"comete_status","inoCx KO")
        APIStatsSelforce.objects.filter(id=id_comete_sender).update(comete_status="inoCx KO")
        APIStatsSelforce.objects.filter(id_comete_sender=data.get("id_api_call")).update(raison_crash=e)
        

    finally:
        logging.debug("Connexion à la base de données fermée.")
        
        

