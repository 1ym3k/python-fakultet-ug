from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# 1. Model profilu użytkownika
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00, validators=[MinValueValidator(0)]) # (na start 1000)

    def __str__(self):
        return f"{self.user.username} - {self.balance} pkt"
    def clean(self):
        if self.balance < 0:
            raise ValidationError({'balance': 'Saldo nie może być ujemne.'})
        
    def save(self, *args, **kwargs):
        self.full_clean()                    # uruchamia wszystkie walidacje
        super().save(*args, **kwargs)

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
    
    def save(self, *args, **kwargs):
        self.full_clean()                    # uruchamia wszystkie walidacje
        super().save(*args, **kwargs)

# 4. Model opcji zakładu (np. Wygra Real, Remis, Wygra Barca)
class Option(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    odds = models.DecimalField(max_digits=5, decimal_places=2, default=1.00) # Kurs (np. 1.50, 2.10)

    def __str__(self):
        return f"{self.name} (Kurs: {self.odds}) - {self.event.title}"

    def clean(self):
        # Sprawdzenie, czy suma prawdopodobieństw (1/odds) nie jest mocno przekroczona
        if self.odds < 1.01:
            raise ValidationError({'odds': 'Kurs musi być większy lub równy 1.01.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()                    # uruchamia wszystkie walidacje
        super().save(*args, **kwargs)
        
# 5. Model konkretnego zakładu postawionego przez użytkownika
class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]   # minimalna stawka 0.01
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    is_won = models.BooleanField(default=False)

    def __str__(self):
        return f"Zakład {self.user.username} na {self.option.name} za {self.amount}"

    def clean(self):
        # 1. Sprawdzenie czy wydarzenie jest jeszcze aktywne
        if not self.option.event.is_active:
            raise ValidationError({'option': 'Nie można obstawiać nieaktywnego wydarzenia.'})

        # 2. Data obstawiania musi być przed końcem wydarzenia
        if self.option.event.end_date <= timezone.now():
            raise ValidationError({'option': 'Wydarzenie już się zakończyło – nie można obstawiać.'})

        # 3. Użytkownik musi mieć wystarczające saldo
        try:
            profile = self.user.profile
            if self.amount > profile.balance:
                raise ValidationError({'amount': f'Nie masz wystarczającego salda. Masz tylko {profile.balance}.'})
        except UserProfile.DoesNotExist:
            raise ValidationError({'user': 'Użytkownik nie ma profilu.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()                    # uruchamia wszystkie walidacje
        super().save(*args, **kwargs)