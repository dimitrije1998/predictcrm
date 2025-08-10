import openai
from django.conf import settings
from django.shortcuts import render
from .models import Klijent, Porudzbina
from django.db.models import Count, Sum
import openai
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Klijent, Porudzbina
openai.api_key = settings.OPENAI_API_KEY



def index(request):
    return render(request, 'list/index.html')  # Pretpostavljam da imaš ovaj template


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'list/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'list/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def index(request):
    klijenti = Klijent.objects.all()
    porudzbine = Porudzbina.objects.all()
    odgovor = ""

    # Priprema detaljnog konteksta za OpenAI
    kontekst_lista = []
    for klijent in klijenti:
        porudzbine_klijenta = klijent.porudzbina_set.all()
        porudzbine_info = []
        for p in porudzbine_klijenta:
            porudzbine_info.append(f"Naziv: {p.naziv}, Iznos: {p.iznos}, Datum: {p.datum.strftime('%Y-%m-%d')}")
        
        klijent_info = (
            f"Klijent ID: {klijent.id}, Ime: {klijent.ime} {klijent.prezime}, Email: {klijent.email}\n"
            f"Porudžbine ({len(porudzbine_klijenta)}): "
        )
        if porudzbine_info:
            klijent_info += "; ".join(porudzbine_info)
        else:
            klijent_info += "Nema porudžbina."
        kontekst_lista.append(klijent_info)
    
    detaljni_kontekst = "\n\n".join(kontekst_lista)

    if request.method == "POST":
        pitanje = request.POST.get("pitanje", "").strip()
        if pitanje:
            try:
                prompt = (
                    f"Ti si analitički asistent. Koristiš detaljne podatke o klijentima i njihovim porudžbinama. "
                    f"Evo podataka:\n\n{detaljni_kontekst}\n\n"
                    f"Pitanje korisnika: {pitanje}\n"
                    f"Analiziraj podatke i pruži precizan i koristan odgovor. "
                    f"Ako je moguće, daj preporuke ili predviđanja na osnovu istorije porudžbina."
                )
                
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Ti si pomoćnik za analizu klijenata i porudžbina."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=250,
                    temperature=0.7,
                )
                odgovor = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                odgovor = f"Došlo je do greške: {e}"

    # Provera da li je korisnik ulogovan da bi prikazao username u template
    username = request.user.username if request.user.is_authenticated else None

    return render(request, 'list/index.html', {
        'klijenti': klijenti,
        'porudzbine': porudzbine,
        'odgovor': odgovor,
        'username': username,
    })