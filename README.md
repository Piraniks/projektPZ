# Projekt zaliczeniowy z Programowania Zespołowego - instalacja

Projekt zakłada, że użytkownik posiada zainstalowany język [Python 3.6](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe)
Przy instalacji najlepiej zaznaczyć opcję z dodaniem do systemowego PATH.

## Przygotowanie do wdrożenia projektu
### Pobranie repozytorium w projektem

Należy pobrać to repozytorium by móc uruchomić projekt.

### (niewymagane) Stworzenie wirtualnego środowiska na potrzeby projektu

Posiadając klon repozytorium należy stworzyć w nim wirtualne środowisko. 
By to zrobić należy w konsoli systemowej przejść do katalogu z projektem a następnie
wpisać następującą komendę:

```bash
python -m venv venv
```

Stworzy to w projekcie katalog o nazwie `venv`. Następnie należy aktywować stworzone środowisko.

Windows PowerShell:
```
venv\Scripts\activate
```

Bash:
```
source venv/Scripts/activate
```

### Instalacja wymaganych pakietów

Wymagane pakiety znajdują się w pliku `requirements.txt`. 
By je zainstalować w konsoli systemowej należy przejść do katalogu z projektem i wpisać:

```
python -m pip install -r requirements.txt
```

### Zastosowanie migracji na lokalnej bazie danych

Ostatnim krokiem ustawiania środowiska jest zastosowanie migracji stworzonych w projekcie.
W tym celu należy w konsoli systemowej przejść do katalogu z projektem i wpisać:

```
python manage.py migrate
```

### Włączenie projektu

By włączyć projekt należy będąc w katalogu z projektem w konsoli systemowej wpisać:

``` 
python manage.py runserver
```

Sprawi ono, iż pod adresem [http://localhost:8000](http://localhost:8000) będzie dostępny projekt.


Jeśli chce się wykorzystać HTTPS należy zamiast tego użyć komendy:

```
python manage.py runsslserver
```

Sprawi ono, iż pod adresem [https://localhost:8080](https://localhost:8080) będzie dostępny projekt.

Jeśli wszystko się udało, powinien pojawić się ekran powitalny.
Dodatkowo w katalogu z projektem powinien pojawić się plik z bazą danych o nazwie `db.sqlite3`.


