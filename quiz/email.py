from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags

def BalanceEmailService(username, calification, totalQ, success, to):
    balance = "De un total de " + str(totalQ) + " preguntas, acertaste " + str(success) + "."
    calificationString = str(calification) + "/100"
    if calification >= 70:
        emoji = "https://d1oco4z2z1fhwp.cloudfront.net/templates/default/671/7.png"
    else:  
        if calification <= 30:
            emoji = "https://d1oco4z2z1fhwp.cloudfront.net/templates/default/671/2.png"
        else:
            emoji = "https://d1oco4z2z1fhwp.cloudfront.net/templates/default/671/4.png"
    html_message = loader.render_to_string(
            'index.html',
            {
                'username': username,
                'calificationString':  calificationString,
                'balanceText': balance,
                'emoji': emoji
            }
        )
    try:
        to_email = to
        subject = "Resultados del Quiz para "+username
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, 'dehiker@demomailtrap.com', [to_email], html_message=html_message)
        return True
    except Exception as e:
        error_message = str(e)
        print("Error de emailService: ", error_message)
        return False
