from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bets.urls')), 
]

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'