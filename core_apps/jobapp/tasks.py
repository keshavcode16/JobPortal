from celery import shared_task
from celery.utils.log import get_task_logger
from .models import *
from datetime import datetime



logger = get_task_logger(__name__)

