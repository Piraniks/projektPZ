                                                          # Projekt zaliczeniowy z Programowania Zespołowego - logowanie i rejestracja
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie 
przejrzystego i czytelnego interfejsu użytkownika, umożliwiającego 
rejestrację - stworzenie konta użytkownika, formularza logowania i 
gwarantującego sprawną nawigację po stronie i podstronach. 
Strony logowania i rejestracji są dostępne dla niezalogowanych użytkowników.

## Rejestracja
Przekierowanie na stronę rejestracji może nastąpić ze strony głównej lub 
ze strony logowania. Strona rejestracji zawiera prosty formularz
 rejestracji, w którym użytkownik musi podać login oraz hasło w postaci
 ciągów znaków, a także napisać hasło ponownie. 
 
 ### Weryfikacja i zabezpieczenia
 Dane podane przez użytkownika poddawane są weryfikacji. Podawane hasło
 oraz login muszą składać się z minimum 5 znaków. Nazwa użytkownika
 (login) musi być unikatowa w bazie danych. Dodatkowo login może 
 zawierać tylko cyfry oraz litery alfabetu angielskiego. Podczas rejestracji
 użytkownik jest zobowiązany do ponownego wpisania wybranego hasła w osobnym 
 paragrafie formularza - hasło oraz powtórzone hasło są porównywane przez 
 system i muszą być takie same, by proces rejestracji się powiódł.
 Hasło użytkownika nie jest jawne nawet dla administratorów - 
 w bazie danych znajduje się ono w postaci zaszyfrowanej. 
 
 ## Logowanie
Przekierowanie na stronę rejestracji może nastąpić ze strony głównej lub 
ze strony rejestracji po pomyślnym zarejestrowaniu się. Strona logowania
zawiera prosty formularz logowania, w którym użytkownik musi podać login
oraz hasło w postaci ciągów znaków.
 
 ### Weryfikacja i zabezpieczenia
 Dane podane przez użytkownika poddawane są weryfikacji. Użytkownik musi
  być zarejestrowany przed zalogowaniem się - nazwa użytkownika
 (login) musi się znajdować w bazie danych. Dodatkowo hasło porównywane 
 jest z hasłem użytkownika o loginie, na który podjęto próbę zalogowania 
 się - podane hasło nie może być różne od tego, znajdującego się w bazie
 danych. Hasło użytkownika nie jest jawne nawet dla administratorów - 
 w bazie danych znajduje się ono w postaci zaszyfrowanej. 