from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_mongoengine.generics import CreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserLoginSerializer, UserCreateSerializer
from django.contrib.auth import login,logout
from .auth import IsAuthenticated
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
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if password == user['password']:
                try:
                    instance = User.objects.get(username=username)
                except User.DoesNotExist:
                    instance = None
                serializer = UserLoginSerializer(instance, data=data)
                if serializer.is_valid():
                    user.backend = 'django_mongoengine.mongo_auth.backends.MongoEngineBackend'
                    login(request, user, backend=user.backend)
                    result = {'message': 'you are logged In'}
                    return Response(data=result, status=status.HTTP_200_OK)
                result = {'error': True, 'message': 'Invalid credentials'}
                return Response(data=result,status=status.HTTP_404_NOT_FOUND)
            result = {'error': True, 'message': 'Invalid credentials'}
            return Response(data=result, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            result = {'error': True, 'message': 'Invalid credentials'}
            return Response(data=result,status=status.HTTP_401_UNAUTHORIZED)

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        logout(request)
        response = redirect('/logoutapi/')
        response.delete_cookie('loginapi')
        return response


        # try:
        #     instance = User.objects.get(username=username)
        #     print(instance)
        # except User.DoesNotExist:
        #     instance = None
        # serializer = UserLoginSerializer(instance, data=data)
        # if serializer.is_valid():
        #     # request.session.set_expiry(3600000)
        #     return Response(serializer.validated_data(data), status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)