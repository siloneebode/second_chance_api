from datetime import datetime

from django.http.response import JsonResponse
from django.utils.timezone import now
from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from Domain.Utils.otp_generator import generate_otp_code
from Domain.account.models import User
from Domain.additionalInfo.models import UserLoginIp
from Domain.auth.models import EmailVerification
from Domain.auth.serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        email_verification = EmailVerification(author=user)
        email_verification.save()

        return JsonResponse({
            "message": "Insciption réussi, confirme ton compte...",
            "data": {
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }},
            status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def send_verification_email(self, request, *args, **kwargs):

        # on récupère l'utilisateur actuellement connecté
        user = User.objects.get(pk=kwargs['pk'])
        verification = EmailVerification(author=user)

        # on regarde si en base de donnée on a un déja une demande.
        verification = EmailVerification.objects.filter(author=user)

        # s'il existe déja une demande en base de donnée
        if verification:
            # SI la demande en bd n'est pas expirée on retourne une erreur 401
            if verification.get().expired_at > now():
                verification.delete()
                verification = EmailVerification.objects.create(author=user)
            else:
                # si la demande est expirée on la supprime puis on recrée une autre demande de vérification d'email.
                return JsonResponse({'message': "Vous avez déja une demande en cours, vérifie ta boite mail."},
                                    status=status.HTTP_409_CONFLICT)
        otp = generate_otp_code()
        verification.code = otp
        verification.expired_at = now() + timedelta(days=1)
        verification.save()

        return JsonResponse({'message': "Demande de vérification envoyé avec success"},
                            status=status.HTTP_201_CREATED)

    @action(['POST'], detail=False)
    def confirm_account(self, request, token):  # on récupère le token depuis la requette
        user = request.user
        email_verification = None
        # on recherche s'il y'a une demande de confirmation qui correspond au token et à l'utilisateur
        try:
            email_verification = EmailVerification.objects.filter(token=token, author=user).get()
        except EmailVerification.DoesNotExist:
            return JsonResponse({"message": "Erreur inconnue... Ressayez plus tard ! "},
                                status=status.HTTP_401_UNAUTHORIZED)

            # si la demande existe et qu'elle est expirée on retourne un status 401
        if email_verification.expired_at < now():
            return JsonResponse({"message": "Demande de confirmation expirée..."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # si tout est ok on passe l'attribut email_confirmed à True et son supprime automatiquement
            # la demande en base de donnée.
            user.email_confirmed = True
            user.save()
            # je mets à jour le status du user sur firebase.
            email_verification.delete()
            # A la fin on envoie un mail à l'utilisateur que son email a bien été confirmé.
            # send_confirmation_mail.delay({'id': user.id, 'email': user.email, 'username': user.username})
            return JsonResponse({"message": "Email vérifié avec success"}, status=status.HTTP_200_OK)

    @action(['POST'], detail=False)
    def registration_validation(self, request):
        """
        Je vérifie le type de données passé dans la requête.
        :param request: email | username
        :return:
        """

        action = request.data['action']
        data = request.data['data']

        if action == 'username':
            user = User.objects.filter(username=data)
            if user:
                return JsonResponse(
                    {
                        "message": "Ce nom d'utilisateur est déja utilisé ",
                        "data": 1
                    })
            else:
                return JsonResponse({})
        else:
            user = User.objects.filter(email=data)
            if user:
                return JsonResponse({
                    "message": "Cette address email est déja utilisé ",
                    "data": 1
                })
            else:
                return JsonResponse({})


class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.filter(pk=serializer.validated_data['user']['id']).get()

            # on récupère l'address ip de l'utilisateur actuel
            ip = get_client_ip(request)

            # on cherche en base de donnée ses autres address ip
            # on retourne une liste d'ip de l'utilisateur => ['ip1', 'ip2'...]
            user_ip = UserLoginIp.objects.filter(owner=user).values_list('user_ip', flat=True)

            # si l'utilisateur n'a pas encore d'ip on crée un ip et on retourne les tokens
            if user_ip is None:
                new_user_ip = UserLoginIp(owner=user, user_ip=ip)
                new_user_ip.save()
                return JsonResponse({serializer.validated_data}, status=status.HTTP_200_OK)

            # si l'utilisateur a déja au moins un ip et que l'ip actuel ne correspond pas à cette ip.
            # on sauvegarde cette ip et on lui envoie un message de confirmation
            if user_ip != [] and ip not in user_ip:
                new_user_ip = UserLoginIp(owner=user, user_ip=ip)
                new_user_ip.save()
                #TODO: Envoyer un mail pour signaler.

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshTokenView(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)
