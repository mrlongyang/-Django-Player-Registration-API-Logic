from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlayerRegistrationSerializer, PlayerLoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = PlayerRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            player = serializer.save()
            return Response({'message': 'Registration successful', 'player_id': player.player_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = PlayerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
