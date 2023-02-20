# Zestaw aplikacji audit_software
zestaw aplikacji do obliczania jakości działania systemu na podstawie etykiet zaznaczonych przez człowieka.
- photo_review.py - aplikacja do etykietowania zanieczyszczeń
- review_summary.py - aplikacja do obliczenia podsumowania jakości działania systemu detekcji
## Uruchomienie photo_review.py
1. W kodzie funkcji def main() wpisujemy ścierzkę z zapisanymi wynikami detekcji oraz z nazwą mięsa do analizy, np.:

data_path_main = 'C:\\Users\\linnia1\\Desktop\\test_02_22'  # początek ścieżki absolutnej
meat_type = 'Nerka wieprzowa'

2. Uruchamiamy aplikację: 
* sterowanie za pomocą klawiatury:
    - j	-poprzednie zanieczyszczenie
    - l	-następne zanieczyszczenie
    - a	-poprzedni obrazek
    - d	-następny obrazek
* sterowanie za pomocą myszki: 
    - zaznaczenie wybranego zanieczyszczenia na obrazie - podwójne kliknięcie w miejscu lewego górnego narożnika, przeciągnięcie i puszczenie klawisza w miejscu prawego dolnego narożnika zanieczyszczenia.

3. Po zakończeniu każdej serii wyniki zapisywane są w:

series_labelled_metadata.json

w katalogu 'results' odpowiedniej serii testowej.