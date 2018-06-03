# Projekt zaliczeniowy z Programowania Zespołowego - przesyłanie plików
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie
przejrzystego i czytelnego interfejsu użytkownika, umożliwiającego
przesyłanie plików na urządzenia, a także wyświetlenie listy przesłanych plików (wersji)
przy zachowaniu sprawnej nawigacji po stronie i podstronach.
Lista przesłanych plików i menu przesyłania pliku
znajdują się na podstronach dostępnych tylko dla zalogowanych użytkowników, posiadających na swojej liście urządzenie,
do którego podjęto próbę przesłania pliku lub wyświetlenia listy wersji.

## Lista przesłanych plików (wersji)
Do podstrony można przejść za pomocą odnośnika znajdującego się na stronie edycji urządzenia.
Na ww. podstronie znajduje się lista plików (wersji) przesłanych na urządzenie.
Ciąg znaków pod nazwą każdego z przesłanych plików to wygenerowany universally unique identifier (UUID). Na liście można sprawdzić również kto i kiedy
przesłał dany plik na urządzenie. Pod listą
przesłanych plików znajduje się przycisk 'Add new version' będący odnośnikiem do strony przesyłania urządzenia.
Jeżeli użytkownik nie przekazał jeszcze żadnego pliku do danego urządzenia, na stronie z listą zamiast ww. informacji znajduje się powiadomienie "Whoops! You have no versions added yet" i przycisk będący odnośnikiem do strony przesyłania plików.

## Przesyłanie pliku (wersji)
Do podstrony można przejść za pomocą przycisku 'Add new version' znajdującego się na stronie listy 
przesłanych plików (wersji). Menu przesyłania pliku na urządzenie wymaga od użytkownika wpisania
nazwy pliku, a także wybrania pliku z komputera. Po wyborze pliku nazwa wybranego pliku oraz jego 
rozszerzenie są możliwe do podejrzenia w menu. Przycisk 'Create' znajdujący się pod menu zatwierdza
wybór pliku do przesłania i przekierowuje użytkownika na stronę listy przesłanych plików. 
