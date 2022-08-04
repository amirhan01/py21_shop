from django.core.mail import send_mail

from shop.celery import app


@app.task
def spam_email():

    full_link = f'привет!'
    send_mail(
        'From shop project',
        full_link,
        'shamuza0102@gmail.com',
        ['shamuza0102@gmail.com']
    )
