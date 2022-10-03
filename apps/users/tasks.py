import logging
import os

import requests
from celery import shared_task

logger = logging.getLogger(__name__)

mailgun_base_url = os.environ.get("MAILGUN_BASE_URL")
mailgun_api_key = os.environ.get("MAILGUN_API_KEY")
sender = os.environ.get("SENDER")


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_account_activation_email(
    self,
    email,
    absolute_url,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Activate your account",
            "text": "Hi "
            + email
            + " Use the link below to verify your email \n"
            + absolute_url,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.info(response.text)
    except Exception as e:
        logger.error(e)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_new_account_activation_email(
    self,
    email,
    absolute_url,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Activate your account",
            "text": "Hi "
            + email
            + " Use the link below to verify your email \n"
            + absolute_url,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.info(response.text)
    except Exception as e:
        logger.error(e)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_password_reset_email(
    self,
    email,
    absolute_url,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Reset your password",
            "text": "Hi "
            + email
            + " Use the link below to reset your password \n"
            + absolute_url,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.info(response.text)
    except Exception as e:
        logger.error(e)
