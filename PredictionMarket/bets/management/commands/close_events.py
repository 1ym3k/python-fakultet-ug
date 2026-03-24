from django.core.management.base import BaseCommand
from django.utils import timezone
from bets.models import Event

class Command(BaseCommand):
    help = 'Zamyka wydarzenia, których czas dobiegł końca'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        # Znajdź aktywne wydarzenia, których data końca już minęła
        expired_events = Event.objects.filter(is_active=True, end_date__lte=now)
        
        count = expired_events.count()
        for event in expired_events:
            event.is_active = False
            event.save()

        self.stdout.write(self.style.SUCCESS(f'SUKCES: Zamknięto {count} przestarzałych wydarzeń.'))