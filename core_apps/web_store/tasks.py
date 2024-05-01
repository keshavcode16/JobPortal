from celery import shared_task
from celery.utils.log import get_task_logger
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *
from datetime import datetime




logger = get_task_logger(__name__)


@shared_task
def notify_on_place_order(thread_payload, profileId, orderId):
    try:
        return False
    except Exception as error:
        # print(error)
        logger.info(f"Exception in processing notify_on_place_order {str(error)}")
        return False