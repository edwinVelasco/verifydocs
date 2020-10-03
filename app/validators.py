from django.core.exceptions import ValidationError


def validate_domainonly_email(value):
    """
    Let's validate the email passed is in the domain "yourdomain.com"
    """
    if not "ufps.edu.co" in value:
        raise ValidationError("Lo sentimos, el correo electrónico enviado no "
                              "es válido. Todos los correos electrónicos "
                              "deben estar registrados en este dominio "
                              "únicamente ufps.edu.co..")

