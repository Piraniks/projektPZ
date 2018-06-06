# Projekt zaliczeniowy z Programowania Zespołowego - grupy
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie 
przejrzystego i czytelnego interfejsu użytkownika, umożliwiającego tworzenie i i edycję grup urządzeń,
dodawania i usuwania urządzeń z grup, a także wyświetlenie listy grup urządzeń danego użytkownika 
przy zachowaniu sprawnej nawigacji po stronie i podstronach. 
Lista grup, formularz dodawania grup, formularz służący do edycji grupy, strona listy urządzeń
w danej grupie, a także strona dodawania urządzeń do listy i ich usuwania znajdują się na podstronach
dostępnych tylko dla zalogowanych użytkowników - próba wejścia na te strony przez osobę niezalogowaną
kończy się przekierowaniem na stronę logowania. Do strony edycji 
grupy można przejść pod warunkiem, że zalogowany użytkownik posiada ją na swojej liście - 
dostęp do edycji grupy ma użytkownik, który stworzył daną grupę. 

## Lista urządzeń użytkownika
Do podstrony można przejść po zalogowaniu się poprzez odnośnik znajdujący się na górnej 
belce - "Groups". Na ww. podstronie znajduje się lista grup urządzeń użytkownika. Każda z 
wylistowanych nazw jest zarazem odnośnikiem do strony edycji grupy urządzeń. 
Ciąg znaków pod nazwą każdego z urządzeń to wygenerowany universally unique identifier (UUID). Pod listą 
grup urządzeń znajduje się przycisk 'Add new group' będący odnośnikiem do strony dodawania nowej grupy urządzeń.
Jeżeli użytkownik nie dodał jeszcze żadnego urządzenia do swojej listy, na stronie z listą 
zamiast ww. informacji znajduje się powiadomienie "Whoops! You have no groups added yet" i 
przycisk będący odnośnikiem do strony dodawania grup.

## Dodawanie grup
Formularz dodawania urządzenia jest prosty - należy w nim podać nazwę dodawanej 
grupy, która nie może zawierać więcej niż 50 znaków, a także nie może być pusta. W chwili dodania
grupy urządzeń jest ona przypisywana do użytkownika. Zapisywana jest data 
dodania, która jest równa dacie ostatniej edycji. Generowany jest również UUID. Po dodaniu 
urządzenia następuje przekierowanie na listę grup urządzeń użytkownika.

## Edycja grupy
Na stronie edycji urządzenia znajduje się formularz edycji nazwy grupy. Na stronie listowane są informacje
o edytowanym urządzeniu - jego UUID, adres IP, data ostatniej
edycji oraz data dodania. Po zatwierdzeniu edycji data edycji za pomocą przycisku 'Save changes' 
dane zostaną zapisane. Na stronie znajduje się również odnośnik do listy wersji (przesłanych plików)
edytowanej grupy - 'Version list'. Na stronie znajduje się również 
przycisk, służący do usunięcia danej grupy urządzeń z listy - 'Delete group', a także odnośnik do strony
z listą urządzeń w edytowanej grupie oraz odnośnik do strony dodawania urządzeń do listy i ich usuwania.

## Dodawanie urządzeń do grupy
Na stronie znajduje się lista urządzeń danego użytkownika. Każda z 
wylistowanych nazw jest zarazem odnośnikiem do strony edycji urządzenia. 
Ciąg znaków pod nazwą każdego z urządzeń to wygenerowany universally unique identifier (UUID). Obok każdego
z wierszy listy znajduje się przycisk +, służący do dodawania urządzeń do grupy. Po wybraniu jednego z urządzeń
następuje przekierowanie na stronę listy urządzeń w danej grupie.


## Lista urządzeń w grupie
Na ww. podstronie znajduje się lista urządzeń użytkownika. Każda z 
wylistowanych nazw jest zarazem odnośnikiem do strony edycji urządzenia. 
Ciąg znaków pod nazwą każdego z urządzeń to wygenerowany universally unique identifier (UUID). Obok każdego z wierszy
znajduje się ikona ( - ), służąca do usuwania rządzeń z listy. Pod listą 
urządzeń znajduje się przycisk 'Add new device' będący odnośnikiem do strony dodawania nowego urządzenia.
Jeżeli użytkownik nie dodał jeszcze żadnego urządzenia do swojej listy, na stronie z listą 
zamiast ww. informacji znajduje się powiadomienie "Whoops! You have no devices added to this group yet" i 
przycisk będący odnośnikiem do strony dodawania urządzeń do grupy.

## Lista przesłanych plików (wersji) w grupie
Do podstrony można przejść za pomocą odnośnika znajdującego się na stronie edycji grupy urządzeń.
Na ww. podstronie znajduje się lista plików (wersji) przesłanych na grupę urządzeń.
Ciąg znaków pod nazwą każdego z przesłanych plików to wygenerowany universally unique identifier (UUID). Na liście można sprawdzić również kto i kiedy
przesłał dany plik na urządzenie. Pod listą
przesłanych plików znajduje się przycisk 'Add new version' będący odnośnikiem do strony przesyłania plików na grupę urządzeń.
Jeżeli użytkownik nie przekazał jeszcze żadnego pliku do danej grupy urządzeń, na stronie z listą zamiast ww. informacji znajduje się powiadomienie "Whoops! You have no versions added yet" i przycisk będący odnośnikiem do strony przesyłania plików.

## Przesyłanie pliku (wersji)
Do podstrony można przejść za pomocą przycisku 'Add new version' znajdującego się na stronie listy 
przesłanych plików (wersji) na daną grupę. Menu przesyłania pliku na urządzenie wymaga od użytkownika wpisania
nazwy pliku, a także wybrania pliku z komputera. Po wyborze pliku nazwa wybranego pliku oraz jego 
rozszerzenie są możliwe do podejrzenia w menu. Przycisk 'Create' znajdujący się pod menu zatwierdza
wybór pliku do przesłania i przekierowuje użytkownika na stronę listy przesłanych na grupę plików. 
