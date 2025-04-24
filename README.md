# InterconnectAPI
InterconnectAPI est une API d'interconnexion entre le CRM Salesforce, une plateforme d'appel téléphonique et un bot.  

## Données sensibles
Toutes les données sensibles ont été remplacées par des "x" pour des raisons de sécurité.  

## Fonctionnement

1. Initialisation d'un ticket dans Salesforce
Une fois qu'un incident est déclaré dans le CRM, une requête est automatiquement envoyée à cette API.  

2. Déclenchement de l'appel
Après le traitement des données envoyées, une requête HTTP est envoyée à la plateforme de téléphonie pour initier un appel vers le client chez qui l'incident a été déclaré.  

3. Mise en contact avec le bot
Une fois que le client a décroché l'appel, via une requête HTTP, il est mis en contact avec le bot, qui va tenter de résoudre le problème signalé.  

## NB 
*Ce micro-service fait partie d'un ensemble de services permettant l'automatisation d'un workflow de prise en charge automatique des incidents.*  

## Exécution du projet  

Étapes pour exécuter ce projet Django
Cloner le dépôt

Commencez par cloner ce dépôt GitHub sur votre machine locale :

bash
Copier
git clone https://github.com/patriceSImo/InterconnectAPI.git
Accéder au répertoire du projet

Accédez au répertoire du projet cloné :

bash
Copier
cd InterconnectAPI
Installer les dépendances

Assurez-vous que vous avez Python et pip installés. Ensuite, installez les dépendances nécessaires en exécutant la commande suivante :

bash
Copier
pip install -r requirements.txt
Appliquer les migrations

Avant de lancer le serveur, appliquez les migrations pour préparer la base de données :

bash
Copier
python manage.py migrate
Lancer le serveur de développement

Maintenant, vous pouvez démarrer le serveur Django en exécutant la commande suivante :

bash
Copier
python manage.py runserver
Cela démarrera le serveur local sur http://127.0.0.1:8000/. Vous pouvez ouvrir ce lien dans votre navigateur pour accéder à l'application.




