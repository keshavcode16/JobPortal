from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime




logger = get_task_logger(__name__)


    
@shared_task
def send_email_task(email):
    from .verification import SendEmail
    try:
        SendEmail().send_verification_email(email)
        return True
    except Exception as error:
        # print(error)
        logger.info(f"Exception in processing notify_on_place_order {str(error)}")
        return False