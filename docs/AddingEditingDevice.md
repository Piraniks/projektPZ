# Projekt zaliczeniowy z Programowania Zespołowego - dodawanie i edycja urządzeń
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie 
przejrzystego i czytelnego interfejsu użytkownika, umożliwiającego 
dodawanie urządzeń i ich edycję, a także wyświetlenie listy urządzeń danego użytkownika 
przy zachowaniu sprawnej nawigacji po stronie i podstronach. 
Lista urządzeń, formularz dodawania urządzenia oraz formularz służący do edycji urządzeń 
znajdują się na podstronach dostępnych tylko dla zalogowanych użytkowników - próba wejścia 
na te strony przez osobę niezalogowaną kończy się przekierowaniem na stronę logowania.

## Lista urządzeń użytkownika
Do podstrony można przejść po zalogowaniu się poprzez odnośnik znajdujący się na górnej 
belce - "Your Devices". Na ww. podstronie znajduje się lista urządzeń dodanych przez 
użytkownika. Każda z wylistowanych nazw jest zarazem odnośnikiem do strony edycji 
urządzenia. Ciąg znaków pod nazwą każdego z urządzeń to wygenerowany UID. Pod listą 
urządzeń znajduje się guzik 'Add new device' będący odnośnikiem do strony edycji.

## Dodawanie urządzenia
Formularz dodawania urządzenia jest prosty - należy w nim podać jedynie nazwę dodawanego 
urządzenia, która nie może zawierać więcej niż 50 znaków, a także nie może być pusta. 
W chwili dodania urządzenia jest ono przypisywane do użytkownika. Zapisywana jest data 
dodania, która jest równa dacie ostatniej edycji. Generowany jest również UID. Po dodaniu 
urządzenia następuje przekierowanie na listę urządzeń użytkownika.

## Edycja urządzenia
Na stronie edycji urządzenia znajduje się formularz edycji nazwy urządzenia oraz 
checkbox, za pomocą którego można oflagować urządzenie jako "Standalone". Na stronie
listowane są informacje o edytowanym urządzeniu - jego UID, data ostatniej edycji oraz data
dodania. Po zatwierdzeniu edycji data edycji za pomocą przycisku 'Save changes' zostanie
nadpisana aktualnymi danymi.