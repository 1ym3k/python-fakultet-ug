from django.core.management.base import BaseCommand
from bets.models import Bet, UserProfile

class Command(BaseCommand):
    help = 'Usuwa wszystkie zakłady z bazy i przywraca każdemu użytkownikowi 1000 euro'

    def handle(self, *args, **kwargs):
        deleted_count, _ = Bet.objects.all().delete()
        
        profiles = UserProfile.objects.all()
        for p in profiles:
            p.balance = 1000.00
            p.save()
            
        self.stdout.write(self.style.SUCCESS(f'SUKCES: Usunięto {deleted_count} zakładów. Zresetowano salda do 1000 euro.'))