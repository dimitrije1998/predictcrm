from django.db import models

class Klijent(models.Model):
    ime = models.CharField(max_length=100)
    prezime = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.ime} {self.prezime}"

class Porudzbina(models.Model):
    klijent = models.ForeignKey(Klijent, on_delete=models.CASCADE)
    naziv = models.CharField(max_length=200)  # ← DODATO
    datum = models.DateField()
    iznos = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.naziv} ({self.klijent})"
