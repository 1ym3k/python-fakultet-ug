from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Event, Option, Bet, UserProfile
from decimal import Decimal
from django.utils import timezone
import datetime

class PredictionMarketTests(TestCase):

    def setUp(self):
        self.client = Client()
        
        # Przygotowanie użytkownika i profilu
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user, balance=Decimal('1000.00'))
        
        # Dane strukturalne dla wydarzeń
        self.category = Category.objects.create(name="Sport", description="Kategoria testowa")
        
        self.aware_end_date = timezone.make_aware(datetime.datetime(2026, 12, 31, 23, 59, 59))
        
        self.event = Event.objects.create(
            title="Final Champions League",
            category=self.category,
            description="Kto wygra mecz finałowy?",
            end_date=self.aware_end_date
        )
        
        self.option_yes = Option.objects.create(
            event=self.event, 
            name="Tak", 
            initial_liquidity=Decimal('100.00')
        )
        self.option_no = Option.objects.create(
            event=self.event, 
            name="Nie", 
            initial_liquidity=Decimal('100.00')
        )

    #LOGIKA BIZNESOWA
    def test_initial_balance(self):
        """Sprawdza czy profil użytkownika ma domyślne saldo 1000 euro"""
        self.assertEqual(self.profile.balance, Decimal('1000.00'))

    def test_dynamic_odds_calculation(self):
        """Sprawdza czy kursy startują od 2.00 przy równej płynności (100/100)"""
        self.assertEqual(self.option_yes.odds, Decimal('2.00'))
        self.assertEqual(self.option_no.odds, Decimal('2.00'))

    def test_bet_affects_odds(self):
        """Sprawdza czy postawienie zakładu zmienia kursy dynamicznie"""
        Bet.objects.create(user=self.user, option=self.option_yes, amount=Decimal('100.00'))
        # Pula Tak: 100+100=200, Pula Nie: 100, Suma: 300. Kurs Tak: 300/200 = 1.5
        self.assertEqual(self.option_yes.odds, Decimal('1.50'))
        self.assertEqual(self.option_no.odds, Decimal('3.00'))

    def test_insufficient_funds(self):
        """Sprawdza czy walidacja blokuje zakład powyżej salda użytkownika"""
        from django.core.exceptions import ValidationError
        invalid_bet = Bet(user=self.user, option=self.option_yes, amount=Decimal('2000.00'))
        with self.assertRaises(ValidationError):
            invalid_bet.full_clean()

    #WIDOKI I INTERAKCJE
    def test_index_page_status_code(self):
        """Sprawdza czy strona główna ładuje się poprawnie (Kod 200)"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Sprawdza czy dostęp do Dashboardu wymaga zalogowania (przekierowanie 302)"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_event_detail_page_content(self):
        """Sprawdza czy strona wydarzenia wyświetla poprawny tytuł (wymaga logowania)"""
        # aby ominąć @login_required
        self.client.login(username='testuser', password='password123')
        
        url = reverse('event_detail', args=[self.event.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Final Champions League")