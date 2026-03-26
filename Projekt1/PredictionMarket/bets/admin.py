from django.contrib import admin
from .models import UserProfile, Category, Event, Option, Bet

#rejestracja modeli
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Option)
admin.site.register(Bet)