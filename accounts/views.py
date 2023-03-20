from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserUpdateSerializer,UserRegister
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

class Register(APIView):
    
    def post(self,request,format=None):
        serializer = UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response']='registered'
            data['username']=account.username
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            data=serializer.errors
        return Response(data)
    
class Welcome(APIView):
    permission_classes = (IsAuthenticated,)

    
    def get(self,request):
        content={'user':str(request.user),'userid':(request.user.id)}
        return Response(content)

class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.copy()  # make a copy of the request data
        data.setdefault('username', user.username)  # set a default value for username if it's missing
        data.setdefault('email', user.email)  # set a default value for email if it's missing
        serializer = UserUpdateSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

