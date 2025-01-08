import os
import subprocess
from django.db.models.signals import post_save
from django.dispatch import receiver
from wifirstAPI.models.apiCallModel import APICallWifirst,APICall
from wifirstAPI.models.scriptsModel import InoCxTask
import logging
import colorlog

# Configuration des logs avec colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@receiver(post_save, sender=APICallWifirst)
def execute_script_on_insert(sender, instance, created, **kwargs):
    logger.debug(f"Signal post_save received for {instance}")
    if created:
        logger.debug(f"New APICallWifirst created with ID: {instance.id_todo_from_wifirst}")
        entry_id = instance.id_todo_from_wifirst
        
        # Utiliser un chemin relatif basé sur le répertoire du script
        script_dir = os.path.dirname(__file__)
        script_path = os.path.join(script_dir, '..', 'Scripts_auto', 'scriptUlexInit.py')
        
        try:
            logger.debug(f"Executing script: {script_path} with entry ID: {entry_id}")
            result = subprocess.run(
                ["python", script_path, str(entry_id)],
                capture_output=True, text=True
            )
    
            if result.stderr:
                if "Traceback" in result.stderr or "Error" in result.stderr:
                    logger.error(f"Script errors: {result.stderr}")
                else:
                    logger.warning(f"Script output with warnings: {result.stderr}")
            else:
                logger.info(f"Script output: {result.stdout}")

        except Exception as e:
            logger.error(f"Error executing script: {e}")
