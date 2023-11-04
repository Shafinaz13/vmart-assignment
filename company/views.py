from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from company.serializers import CustomUserSerializer, CompanySerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    position = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


def email_validate(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def home(request):
    return render(request, 'home.html')


def user_signup(request):
    context = {'form': SignupForm(), "is_login": False}
    return render(request, 'login.html', context)


@require_http_methods(["POST"])
def signup_submit(request):
    email = request.POST['email']
    company = request.POST['company']
    position = request.POST['position']
    phone_number = request.POST['phone_number']
    password = request.POST['password']
    is_correct_email = email_validate(email)
    username = str(request.POST['username'])
    if not is_correct_email:
        context = {'form': SignupForm(), "is_login": False,
                   "incorrect_email": "Invalid Email Id"}
        return render(request, 'login.html', context)
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        custom_user = CustomUser.objects.create(
            user=user, email=str(email), company_id=company, position=position, phone_number=phone_number)
        custom_user.company.no_of_employees += 1
        custom_user.company.save()
        context1 = {"form": LoginForm(), "is_login": True}
        return render(request, "login.html", context1)
    else:
        context = {'form': SignupForm(), "is_login": False,
                   "email_already_exists": "Account with this Email Id already exists."}
        return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    request.session.clear()
    return redirect('home')


def user_login(request):
    context = {"form": LoginForm(), "is_login": True}
    return render(request, "login.html", context)


@require_http_methods(["POST"])
@csrf_protect
def login_submit(request):
    email = str(request.POST['email'])
    password = request.POST['password']
    try:
        custome_user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        custome_user = None
    if custome_user:
        user = authenticate(email=custome_user.email, password=password)
        if user:
            login(request, user)
            return render(request, 'user_detail.html', {"user": custome_user})
        else:
            context = {"form": LoginForm(), "is_login": True,
                       "invalid_user_pass": "Invalid Email Id or Password"}
            return render(request, "login.html", context)
    else:
        context = {"form": LoginForm(), "is_login": True,
                   "invalid_user_pass": "Invalid Email Id or Password"}
        return render(request, "login.html", context)


@login_required
def edit(request):
    user = request.user
    custome_user = CustomUser.objects.get(user=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=custome_user)
        if form.is_valid():
            form.save()
            return render(request, 'user_detail.html', {"user": custome_user})

    else:
        form = UserEditForm(instance=user)

    return render(request, 'user_detail_edit.html', {'form': form})


class CustomUserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    def post(self, request):
        custom_user_serializer = CustomUserSerializer(data=request.data)

        if custom_user_serializer.is_valid():
            custom_user_serializer.save()

            response_data = custom_user_serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        if user_id:
            user = self.get_object(user_id)
            if user is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CustomUserSerializer(user)
        else:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        custom_user = self.get_object(user_id)
        if custom_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        custom_user.company.no_of_employees -= 1
        custom_user.company.save()
        custom_user.delete()
        try:
            user = User.objects.get(id=custom_user.user_id)
        except User.DoesNotExist:
            user = None
        if user:
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, id):
        try:
            return Company.objects.get(id=id)
        except Company.DoesNotExist:
            return None

    def post(self, request):
        company_serializer = CompanySerializer(data=request.data)

        if company_serializer.is_valid():
            company_serializer.save()

            response_data = company_serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        company = self.get_object(id)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            company = self.get_object(id)
            if company is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CompanySerializer(company)
        else:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        company = self.get_object(id)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
