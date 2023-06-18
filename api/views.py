from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import UserSerializer, PostSerializer
from .models import User, Post
from django.conf import settings
import requests
import re
from datetime import date
from django.utils import timezone
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

class MainView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the main view!"})


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            
            # Enrich User with geolocation data asynchronously
            geolocation = enrich_user_geolocation(email, request.META.get('REMOTE_ADDR'))
            print(geolocation)
            
            # Check if signup coincides with a holiday
            bool_holiday = check_holiday_signup(email,geolocation)
            print(bool_holiday)
            # Create User
            user = User.objects.create_user(email=email, password=password,username=username,geolocation=geolocation,is_holiday=bool_holiday)
            
            return Response({"message": "User signed up successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate User
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login User and generate JWT tokens
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)})
        
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

class GetUserDataView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostLikeView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.likes += 1
        post.save()
        return Response({"message": "Post liked"})

class PostUnlikeView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.likes -= 1
        post.save()
        return Response({"message": "Post unliked"})


def is_valid_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def enrich_user_geolocation(email, ip_address):
    url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY}&ip_address={ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        geolocation = response.json().get("country_code",None)
        return geolocation
    else:
        return None

def check_holiday_signup(email,geolocation):
    # Get today's date
    if geolocation:
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day
        url = f"https://holidays.abstractapi.com/v1/?api_key=dc3283fcf6a24e179124907dcd757374&country={geolocation}&year={year}&month={month}&day={day}"
        response = requests.get(url)
        if response.status_code == 200:
            if response.json():
                return True
            else:
                return False
    else:
        return None
