from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bets.models import Category, Event, Option

class Command(BaseCommand):
    help = 'Dodaje przykładowe dane (kategorie i wydarzenia) do bazy'

    def handle(self, *args, **kwargs):
        #kategoria
        cat, created = Category.objects.get_or_create(name="Polityka", description="Zakłady polityczne")
        
        #wydarzenie
        event, created = Event.objects.get_or_create(
            title="Kto wygra wybory prezydenckie 2026?",
            category=cat,
            description="Wybierz kandydata, który Twoim zdaniem obejmie urząd.",
            end_date=timezone.now() + timedelta(days=30)
        )
        
        #bety
        if created:
            Option.objects.create(event=event, name="Kandydat A", initial_liquidity=150)
            Option.objects.create(event=event, name="Kandydat B", initial_liquidity=100)
            self.stdout.write(self.style.SUCCESS('SUKCES: Dodano przykładowe wydarzenie polityczne!'))
        else:
            self.stdout.write(self.style.WARNING('Przykładowe dane już istnieją w bazie.'))