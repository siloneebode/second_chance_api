from django.db.models.signals import post_save
from django.dispatch import receiver
from Domain.auth.models import EmailVerification
from django.core.mail import send_mail


# Le signal se déclenche quand un EmailVerification object vient d'etre sauvegardé
@receiver(post_save, sender=EmailVerification)
def send_email_confirmation(sender, instance, **kwargs):
    send_mail('Vérification de compte',
              'Here is the message.',
              'ebodesilone@gmail.com', [instance.author.email], fail_silently=False)
