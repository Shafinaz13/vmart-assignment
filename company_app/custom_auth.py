from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from company.models import CustomUser

User = get_user_model()


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            if email:
                custom_user = CustomUser.objects.get(email=email)
                user = custom_user.user
            else:
                user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
