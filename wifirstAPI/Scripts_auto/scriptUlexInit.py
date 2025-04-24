import sys
import requests
from datetime import datetime, timezone, timedelta
import logging
import json
import os,re
import django
from django.forms.models import model_to_dict

# Ajout du chemin vers le dossier contenant 'cxxxxeAPIs'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
try:
    # Configuration de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cxxxxeAPIs.settings')
    django.setup()
except Exception as e:
    print(f"Erreur lors de l'initialisation de Django : {e}")
    
from xxxxxxxAPI.models.apiCallModel import APICall, APICallxxxxxxx
from wxxxxxtAPI.models.statsModels import APIStatsSelforce
from wxxxxxtAPI.Scripts_auto.scriptInocx import process_new_entry_inocx,update_stats

# Configuration des logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from datetime import datetime


def validate_datetime_alarm(data):
    date_format = data.get("datetime_alarm")
    if not date_format:
        logging.debug("Erreur: 'datetime_alarm' est manquant dans les données.")
        return None  # Pas de date fournie

    try:
        # Vérifier si la date est au format complet avec secondes
        if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", date_format):
            date_obj = datetime.strptime(date_format, "%d/%m/%Y %H:%M:%S")
            formatted_date = date_obj.strftime("%Y/%m/%d %H:%M:%S")
            logging.debug(f"Date reformattée avec secondes : {formatted_date}")
            return formatted_date

        # Vérifier si la date est au format sans secondes
        if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}", date_format):
            # Convertir en datetime et reformater avec les secondes
            date_obj = datetime.strptime(date_format, "%d/%m/%Y %H:%M")
            formatted_date = date_obj.strftime("%Y/%m/%d %H:%M:%S")
            logging.debug(f"Date reformattée avec secondes : {formatted_date}")
            return formatted_date

        # Si aucun format ne correspond
        raise ValueError(f"Format de date non valide : {date_format}")

    except Exception as e:
        logging.error(f"Erreur de validation de la date : {e}")
        return None

def send_to_uxxx (data):
    # Vérifier si datetime_alarm est présent dans les données
    date_format = None
    if data.get("datetime_alarm"):
        try: 
            date_format = validate_datetime_alarm(data)
            if not date_format:
                logging.error("La date fournie est invalide ou manquante.")
                return {"error": "Invalid or missing datetime_alarm"}
                    
        except ValueError as e:
            logging.debug(f"Erreur de conversion de la date : {e}")
            return {"error": f"Date format error: {e}"}
    else:
        logging.debug("Erreur: 'datetime_alarm' est manquant dans les données.")
        return {"error": "datetime_alarm is missing"}

    # Remplacer le symbole '+' dans le numéro de téléphone
    num = data.get("phone", "").replace('+', '%2B')
    pin_tem = APICall.objects.filter(id_api_call=data.get("id_api_call")).values_list("pin",flat=True).first()
            
    #extraction des 6 premiers chiffres
    pin = pin_tem[-8:]
    
    # configuration de la requette a envoyer à uxxx
    endpoint = f"https://wxxxxxt.xx.xxxxxxxx.net/api/session.php?param=xxxxxxxxxxxxxxxxxxxx:wxxxxxt@wxxxxxt&phone={num}&pin={pin}"
    data_send = {
        "context": {
            "id_cxxxxe_sender": data.get("id_api_call"),
            "customer_name":data.get("contact"),
            "datetime_alarm":date_format,
            "location":data.get("location"),
            "transfer_number":"+33170927594",
            "company":data.get("company"),
            "phone": data.get("phone"),
            "call_start_point":"",
            "site":data.get("site")
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data_encode = json.dumps(data_send, ensure_ascii=False).encode('utf-8')
    logging.debug(f" la data envoyé à uxxx est la : {data_send}")
    try:
        # Envoyer les données à l'API via une requête POST
        response = requests.post(endpoint, data=data_encode, headers=headers)
        response.raise_for_status()  # Pour vérifier les erreurs dans la réponse
                
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")
                

    return response
        

def process_new_entry(entry_id):
    try:
        logging.debug(f"Connexion à la base de données réussie pour l'entrée ID {entry_id}.")
        data_found =  APICallwxxxxxt.objects.filter(id_todo_from_wxxxxxt=entry_id).first()
        # Convertir l'objet Django en dictionnaire
        data = model_to_dict(data_found)
        id_cxxxxe_sender = data.get("id_api_call")

        if not data:
            logging.error(f"Aucune donnée trouvée pour l'ID {entry_id}")
            return

        try:
            new_stat = APIStatsSelforce.objects.create(
                    id_cxxxxe_sender = data.get("id_api_call"),
                    salesforce_id = data.get("id_salesforce"),
                    final_cxxxxe_status = "SALESFORCE INIT",
                    create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

        except Exception as e:
            logging.debug(f"Une erreur est survenue lors de la création de la ligne statistique : {e}")
            APIStatsSelforce.objects.filter(id_cxxxxe_sender=id_cxxxxe_sender).update(raison_crash = e,)
        
        #Creation de la session chez uxxx
        response = send_to_uxxx(data)
        response_text = response.content.decode('utf-8-sig')

        # Vérifier si la requête a été exécutée avec succès
        if response.status_code == 200:
            logging.info(f"Données envoyées avec succès à l'API. Réponse: {response_text}")
            
            response_data = json.loads(response_text)
            #mise à jour champs pin_uxxx_sender dans la table todo_from_uxxx
            pin = response_data.get("pin")
            logging.debug(f"la valeur du pin mis en base est :{pin}")
            
            update_stats(id_cxxxxe_sender,"cxxxxe_status_detail","uxxx session 1 OK")
            APIStatsSelforce.objects.filter(id_cxxxxe_sender=id_cxxxxe_sender).update(final_cxxxxe_status="uxxx session 1 OK")
            update_stats(id_cxxxxe_sender,"cxxxxe_status_detail",pin )
            APIStatsSelforce.objects.filter(id_cxxxxe_sender=id_cxxxxe_sender).update(uxxx_id=pin)
            
            try:
                logging.debug(f"Execution du script pour inoCx avec l'id_todo_from_wxxxxxt : {entry_id}")
                process_new_entry_inocx(data_found)

            except Exception as e:
                logging.error(f"erreur lors de l'exécution du script de inoCx xxx2: {e}")
                APIStatsSelforce.objects.filter(id_cxxxxe_sender=id_cxxxxe_sender).update(raison_crash = e,)

        else:
            ###
            # envois de reponse finale à selforce avec un echec du coté de uxxx
            #
            logging.error(f"Erreur lors de l'envoi des données à xxx l'API. Statut HTTP: {response.status_code}, Réponse: {response}")
            #fermer le ticket dans selforce avec comme cmom creation du boot off
            
    except Exception as e:
        logging.error(f"Erreur lors du traitement de l'entrée ID {entry_id}: {e}")
        APIStatsSelforce.objects.filter(id_cxxxxe_sender=id_cxxxxe_sender).update(raison_crash = e,)
        update_stats(id_cxxxxe_sender,"cxxxxe_status_detail",e)
        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <entry_id>")
        sys.exit(1)
    
    entry_id = sys.argv[1]
    process_new_entry(entry_id)
