from django.db import models

from django.db import models
from django.contrib.auth.models import User

# 1. Model profilu użytkownika
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00) # (na start 1000)

    def __str__(self):
        return f"{self.user.username} - {self.balance} pkt"

# 2. Model kategorii (np. Sport, Wybory, Krypto)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 3. Model wydarzenia (np. Finał Ligi Mistrzów)
class Event(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    description = models.TextField()
    is_active = models.BooleanField(default=True) # Czy można jeszcze obstawiać?
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField() # Kiedy wydarzenie się kończy

    def __str__(self):
        return self.title

# 4. Model opcji zakładu (np. Wygra Real, Remis, Wygra Barca)
class Option(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    odds = models.DecimalField(max_digits=5, decimal_places=2, default=1.00) # Kurs (np. 1.50, 2.10)

    def __str__(self):
        return f"{self.name} (Kurs: {self.odds}) - {self.event.title}"

# 5. Model konkretnego zakładu postawionego przez użytkownika
class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Ile postawiono
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False) # Czy zakład został już rozliczony
    is_won = models.BooleanField(default=False) # Czy zakład jest wygrany

    def __str__(self):
        return f"Zakład {self.user.username} na {self.option.name} za {self.amount}"