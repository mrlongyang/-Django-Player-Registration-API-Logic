from django.db import models

class Player(models.Model):
    player_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    ip_address = models.GenericIPAddressField()
    origin_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Wallet(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.player.name}'s Wallet"
