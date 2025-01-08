import requests
import json
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Informations pour obtenir le token
BASE_URL = "https://wifirst.my.salesforce.com"
TOKEN_URL = f"{BASE_URL}/services/oauth2/token"
CLIENT_ID = "3MVG9fTLmJ60pJ5K0o0WvIxguwqZc4RdDn_AlhU4.JJjMo0zUu74CQpnTSWnthy2EM5HgBdwi.G1a_I.oEhYV"
CLIENT_SECRET = "D7182F27AD00E5B3B07A40D6AD2B88DF83FFA91E420DB2DC7067A51FBF8C1E72"


def get_access_token():
    payload = {
        'grant_type': 'client_credentials',  # Utilise client_credentials comme grant_type
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Envoyer la requête POST pour obtenir le jeton d'accès
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    # Vérifier si la requête a réussi
    if response.status_code in [200, 201]:
        logging.info("Token request succeeded.")
        return response.json()['access_token']  # Récupérer le jeton d'accès
    else:
        raise Exception(f"Failed to get access token: {response.text}")

# Fonction pour envoyer une requête PATCH
def send_patch_request(case_id,patch_data):
    
    access_token = get_access_token()

    # URL de la requête PATCH (dépendant de l'ID du case)
    patch_url = f"{BASE_URL}/services/data/v60.0/sobjects/CASE/{case_id}"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.patch(patch_url, data=json.dumps(patch_data), headers=headers)

    if response.status_code in [200, 204]:
        logging.debug("Patch request succeeded.")
        return response.json()
    else:
        logging.debug(f"Failed to send patch request: {response.status_code} - {response.text}")
        return None
