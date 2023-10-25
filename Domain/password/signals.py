from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import render_to_string
from Domain.auth.tasks import send_mail_task

from Domain.password.models import PasswordReset


@receiver(post_save, sender=PasswordReset)
def send_email_for_password_reset(sender, instance, **kwargs):
    data = {
        'subject': 'Réinitialisation de mot de passe ',
        'message': render_to_string('mails/password/reset.html', {'token': instance}),
        'to_email': [instance.author.email],
        'text_content': 'Confirme ton address email'
    }
    print(data)
    send_mail_task.delay(data)
