# Koristi zvanični Python 3.10 image
FROM python:3.10-slim

# Postavi radni direktorijum u kontejneru
WORKDIR /app

# Kopiraj fajl sa zavisnostima
COPY requirements.txt .

# Ažuriraj pip i instaliraj zavisnosti
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kopiraj ostatak koda u kontejner
COPY . .

# Izloži port 8000 (Heroku će preusmeriti na svoj PORT)
EXPOSE 8000

# Pokreni Gunicorn server, imaj na umu da je ime projekta 'ClientsList'
CMD ["gunicorn", "ClientsList.wsgi:application", "--bind", "0.0.0.0:8000"]
