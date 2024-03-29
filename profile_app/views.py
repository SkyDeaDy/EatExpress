from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, ProfileSerializer, CourierSerializer
from .utils import get_profile_or_courier


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

            if 'status' in request.data:
                group_name = 'CouriersGroup'
            else:
                group_name = 'ProfilesGroup'

            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            return Response({"message": "You have successfully registered"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response['Access-Token'] = access_token
            response['Refresh-Token'] = str(refresh)
            return response  # or HttpResponseRedirect('/')
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        profile, is_courier = get_profile_or_courier(slug)
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer_class = CourierSerializer if is_courier else ProfileSerializer
        serializer = serializer_class(profile)

        if request.user != profile.user:
            return Response({'error': 'You do not have permission to view this profile'},
                            status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        profile, is_courier = get_profile_or_courier(slug)
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer_class = CourierSerializer if is_courier else ProfileSerializer
        serializer = serializer_class(profile, data=request.data)

        if request.user != profile.user:
            return Response({'error': 'You do not have permission to update this profile'},
                            status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        profile, is_courier = get_profile_or_courier(slug)
        if not profile:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != profile.user:
            return Response({'error': 'You do not have permission to delete this profile'},
                            status=status.HTTP_403_FORBIDDEN)

        profile.user.delete()
        return Response({'message': 'Profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class SignOutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response