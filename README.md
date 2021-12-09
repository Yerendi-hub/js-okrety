# Okręty
## Opis zadania 
- Okno z dwoma planszami 10x10 pól (np. siatki przycisków) oraz przyciskiem rozpoczęcia gry i przyciskiem reset. 
- Na początku gracz rozmieszcza okręty (1x czteromasztowiec, 2x trójmasztowiec, 3x dwumasztowiec, 4x jednomasztowiec). 
- Po rozmieszczeniu okrętów przez gracza i wciśnięciu przycisku nowej gry przeciwnik komputerowy losowo rozmieszcza swoje okręty. 
- Okręty nie mogą się dotykać ani bokami ani rogami. 
- Po rozmieszczeniu okrętów przez obu graczy jeden z nich wykonuje pierwszy ruch (losowo gracz lub komputer). 
- Wybór celu przez gracza następuje przez kliknięcie pola, w razie trafienia przycisk staje się czerwony, w przeciwnym razie niebieski (nie można strzelić dwa razy w to samo pole). 
- Komputer strzela w losowe, nie wybrane wcześniej pole. Po trafieniu próba znalezienia orientacji statku i zestrzelenie go do końca. 
- Gra kończy się gdy któryś gracz straci ostatni okręt, wyświetlane jest okno z informacją o zwycięzcy (np. "Wygrana!", "Przegrana!”). 
- Opcjonalnie: bardziej zaawansowana sztuczna inteligencja omijająca pola na których na pewno nie może znaleźć się okręt gracza. 
## Testy:
- Próba niepoprawnego ustawienia okrętu (stykanie się bokami lub rogami). Oczekiwana informacja o błędzie 
- Poprawne rozmieszczenie wszystkich okrętów przez gracza i wciśnięcie przycisku rozpoczęcia gry. 
- Strzelenie w puste pole. 
- Trafienie w okręt przeciwnika. 
- Próba zestrzelenia swojego okrętu - oczekiwane niepowodzenie. 
- Próba ponownego strzelenia w puste pole - oczekiwane niepowodzenie. 
- Próba ponownego strzelenia w okręt przeciwnika - oczekiwane niepowodzenie. 
- Rozmieszczenie części okrętów, wciśnięcie przycisku reset - oczekiwany reset plansz. 
- Poprawne rozmieszczenie wszystkich okrętów, oddanie kilku strzałów, rozpoczęcie nowej gry, ponowne poprawne rozmieszczenie okrętów, oddanie strzałów w te same pola.
- Wygranie gry (np. Przez pokazanie okrętów przeciwnika). Rozpoczęcie nowej. gry bez ponownego uruchamiania programu. 
- Przegranie gry (np. Przez aktywację super-instynktu gracza komputera). Rozpoczęcie nowej gry bez ponownego uruchamiania programu.
