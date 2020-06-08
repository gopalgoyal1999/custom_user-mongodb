from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_mongoengine.generics import CreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .models import User
from .serializers import UserLoginSerializer, UserCreateSerializer

#User = get_user_model()

class UserRegister(CreateAPIView):
    serializer_class=UserCreateSerializer
    queryset= User.objects.all()

class UserLogin(GenericAPIView):
    serializer_class=UserLoginSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self,request, *args, **kwargs):
        data = request.data
        username = request.data.get('username')
        try:
            instance = User.objects.get(username=username)
            print(instance)
        except User.DoesNotExist:
            instance = None
        serializer = UserLoginSerializer(instance, data=data)
        print(serializer)
        if serializer.is_valid():
            request.session.set_expiry(3600000)
            return Response(serializer.validated_data(data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    def post(self,request):
        request.session.flush()
        return redirect('/loginapi/')
