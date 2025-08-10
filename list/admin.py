from django.contrib import admin
from .models import Klijent, Porudzbina

@admin.register(Klijent)
class KlijentAdmin(admin.ModelAdmin):
    list_display = ('ime', 'prezime', 'email')
    search_fields = ('ime', 'prezime')

@admin.register(Porudzbina)
class PorudzbinaAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'klijent', 'datum', 'iznos')  # ← DODAT naziv
    list_filter = ('datum',)
    search_fields = ('naziv',)
