from rest_framework import generics,status
from .serializers import RegisterUserSerializer,RegisterMessSerializer
from rest_framework.response import Response
from .models import User,Mess
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth import authenticate
import jwt
from django.conf import settings
import datetime 
from django.http import JsonResponse

class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if "@" in email and User.objects.filter(email=email).exists():
                return Response({"message": "Email Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
            elif "@" not in email:
                return Response({"message": "Please enter correct Email ID"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.validated_data['password'] = make_password(password)
                serializer.save()
                return Response({"message": "User Register Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterMessView(generics.GenericAPIView):
    serializer_class = RegisterMessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            contact_no = serializer.validated_data['contact_no']
            password = serializer.validated_data['password']
            name = serializer.validated_data['name']

            if User.objects.filter(contact_no=contact_no).exists():
                return Response({"message": "Contact Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(name=name).exists():
                return Response({"message": "Name Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.validated_data['password'] = make_password(password)
                serializer.save()
                return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def make_password_helper(password):
    return make_password(password)


def get_user_from_token(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    if not authorization_header:
        return Response({"error": "Authorization header is missing"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = authorization_header.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        # Extract the id from the payload
        user_id = payload.get('user_id')
        # Return the id
        return user_id
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    except IndexError:
        return Response({"error": "Invalid token format"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)



class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                token = generate_jwt_token(user)
                return Response({'token': token}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class LoginMessView(APIView):
    def post(self, request):
        contact_no = request.data.get('contact_no')
        password = request.data.get('password')
        try:
            user = Mess.objects.get(contact_no=contact_no)
            if check_password(password, user.password):
                token = generate_jwt_token(user)
                return Response({'token': token}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Mess does not exist'}, status=status.HTTP_400_BAD_REQUEST)

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
