from rest_framework import serializers
from .models import Player, Wallet
from django.contrib.auth.hashers import make_password, check_password

class PlayerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'phone', 'password']

    def create(self, validated_data):
        request = self.context.get('request')
        ip_address = request.META.get('REMOTE_ADDR')
        origin_url = request.META.get('HTTP_REFERER', '')

        # Generate unique player_id
        import random, string
        while True:
            player_id = ''.join(random.choices(string.ascii_lowercase, k=5)) + ''.join(random.choices(string.digits, k=5))
            if not Player.objects.filter(player_id=player_id).exists():
                break

        # Create player
        player = Player.objects.create(
            player_id=player_id,
            name=validated_data['name'],
            phone=validated_data['phone'],
            password=make_password(validated_data['password']),
            ip_address=ip_address,
            origin_url=origin_url,
        )

        # Create wallet
        Wallet.objects.create(player=player)

        return player

class PlayerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            player = Player.objects.get(phone=data['phone'])
        except Player.DoesNotExist:
            raise serializers.ValidationError("Invalid phone or password")

        if not check_password(data['password'], player.password):
            raise serializers.ValidationError("Invalid phone or password")

        return {
            'message': 'Login successful',
            'player_id': player.player_id,
            'name': player.name
        }
