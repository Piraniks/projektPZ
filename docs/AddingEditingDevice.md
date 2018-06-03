# Projekt zaliczeniowy z Programowania Zespołowego - dodawanie i edycja urządzeń
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie 
przejrzystego i czytelnego interfejsu użytkownika, umożliwiającego 
dodawanie urządzeń i ich edycję, a także wyświetlenie listy urządzeń danego użytkownika 
przy zachowaniu sprawnej nawigacji po stronie i podstronach. 
Lista urządzeń, formularz dodawania urządzenia oraz formularz służący do edycji urządzeń 
znajdują się na podstronach dostępnych tylko dla zalogowanych użytkowników - próba wejścia 
na te strony przez osobę niezalogowaną kończy się przekierowaniem na stronę logowania. Do strony edycji 
urządzenia można przejść pod warunkiem, że zalogowany użytkownik posiada je na swojej liście - 
dostęp do edycji urządzenia ma użytkownik, do którego przypisano dane urządzenie.

## Lista urządzeń użytkownika
Do podstrony można przejść po zalogowaniu się poprzez odnośnik znajdujący się na górnej 
belce - "Your Devices". Na ww. podstronie znajduje się lista urządzeń użytkownika. Każda z 
wylistowanych nazw jest zarazem odnośnikiem do strony edycji urządzenia. 
Ciąg znaków pod nazwą każdego z urządzeń to wygenerowany universally unique identifier (UUID). Pod listą 
urządzeń znajduje się przycisk 'Add new device' będący odnośnikiem do strony dodawania nowego urządzenia.
Jeżeli użytkownik nie dodał jeszcze żadnego urządzenia do swojej listy, na stronie z listą 
zamiast ww. informacji znajduje się powiadomienie "Whoops! You have no devices added yet" i 
przycisk będący odnodo dodawania urządzenia.

## Dodawanie urządzenia
Formularz dodawania urządzenia jest prosty - należy w nim podać nazwę dodawanego 
urządzenia, która nie może zawierać więcej niż 50 znaków, a także nie może być pusta oraz adres IP
z puli adresów IPv4 lub IPv6. W chwili dodania urządzenia jest ono przypisywane do użytkownika. Zapisywana jest data 
dodania, która jest równa dacie ostatniej edycji. Generowany jest również UUID. Po dodaniu 
urządzenia następuje przekierowanie na listę urządzeń użytkownika.

## Edycja urządzenia
Na stronie edycji urządzenia znajduje się formularz edycji nazwy urządzenia oraz 
. Na stronie listowane są informacje o edytowanym urządzeniu - jego UUID, adres IP, data ostatniej
edycji oraz data dodania. Po zatwierdzeniu edycji data edycji za pomocą przycisku 'Save changes' 
zostanie nadpisana aktualnymi danymi. Na stronie znajduje się również odnośnik do listy wersji
edytowanego urządzenia - 'Version list'. Na stronie znajduje się również 
przycisk, służący do usunięcia danego urządzenia z listy - 'Delete device'. 