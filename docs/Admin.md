# Projekt zaliczeniowy z Programowania Zespołowego - panel administratora
Jednym z pobocznych celów realizowanych podczas projektu było stworzenie
przejrzystego i czytelnego interfejsu administratora, umożliwiającego
zarządzanie użytkownikami, urządzeniami i przesłanymi plikami. Na stronę można przejść poprzez link
https://127.0.0.1:8000/admin/ . Dostęp do panelu administratora ma jedynie administrator - w przypadku, 
gdy na stronę próbuje uzyskać dostęp zwykły użytkownik lub ktoś niezalogowany, następuje przekierowanie
na stronę logowania z szablonem zastosowanym w panelu administratora. 


## Strona główna 
Na stronie głównej panelu administratora znajdują się odnośniki do podstron z listami: użytkowników (Users), 
urządzeń (Devices), przesłanych plików (Versions). Ponadto na górnej belce znajdują się odnośniki na stronę główną, 
do strony zmiany hasła i do wylogowania się.


## Lista użytkowników
Lista użytkowników to spis wszystkich użytkowników. Administrator może usuwać użytkowników pojedynczo 
lub masowo, zaznaczając checkboxy przy ich loginach i wybierając z menu rozwijanego opcję 'Delete selected users' lub
zedytować jednego z użytkowników, poprzez wybranie go z listy za pomocą kliknięcia na jego login. Administrator
może sprawdzić datę i godzinę ostatniego zalogowania się użytkownika, zmienić jego login (nazwę), zmienić jego 
uprawnienia, a także nadać mu rangę administratora poprzez zaznaczenie checkboxów 'is staff' i 'Superuser status'.
Może również usunąć użytkownika z poziomu strony edycji.

## Lista urządzeń
Lista urządzeń to spis wszystkich urządzeń. Administrator może usuwać urządzenia pojedynczo 
lub masowo, zaznaczając checkboxy przy ich nazwach i wybierając z menu rozwijanego opcję 'Delete selected devices' lub
zedytować jedno z urządzeń, poprzez wybranie go z listy za pomocą kliknięcia na jego nazwę. Administrator
może zmienić UUID urządzenia, nazwę, właściciela. Ponadto umożliwia otwarcie nowego okna służącego do stworzenia nowego 
użytkownika, usunięcie lub edycję wybranego użytkownika z listy rozwijanej. Co więcej, umożliwia otwarcie nowego okna 
służącego do przesłania pliku na urządzenie, zedytowania już istniejącego i wybranego lub usunięcia go.
Administrator może również usunąć urządzenie z poziomu strony edycji.

## Lista plików
Lista plików to spis wszystkich przesłanych plików. Administrator może usuwać pliki pojedynczo 
lub masowo, zaznaczając checkboxy przy ich nazwach i wybierając z menu rozwijanego opcję 'Delete selected versions' lub
zedytować jeden z plików, poprzez wybranie go z listy za pomocą kliknięcia na jego nazwę. Administrator może zmienić 
UUID pliku, jego nazwę, właściciela i zmienić jego kolejność na liście.