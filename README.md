# Treniņu un Fitnesa Datubāzes Sistēma

Skolas projekts, kas izveidots, izmantojot Python, SQLite un tkinter.

## Projekta faili

Projekts sastāv no šādām komponentēm:
- **main.py** — programmas palaišanas fails. Tas sagatavo datubāzi, izveido galveno logu un palaiž lietotni.
- **app.py** — galvenā loga izskats un uzbūve. Tajā tiek iestatīts loga nosaukums un izmērs, kā arī izveidotas lietotnes cilnes.
- **tabs.py** — katras cilnes iestatījumi: tās nosaukums, ievades lauki, datubāzes vaicājums un datu tabulas kolonnu virsraksti.
- **tab_view.py** — kopīgā cilņu darbība. Tas izveido ievades formu un datu tabulu, kā arī apstrādā ierakstu saglabāšanu un saraksta atjaunošanu.
- **database.py** — funkcijas savienojumam ar SQLite datubāzi, SQL vaicājumu izpildei un tabulu izveidei.
- **gym.db** — pati SQLite datubāze, kurā tiek glabāti lietotnes dati.
- **README.md** — projekta apraksta un lietošanas instrukciju fails.

## Datubāzes tabulas

Datubāzē ir 8 tabulas:
- `users`
- `exercises`
- `workouts`
- `workout_sets`
- `personal_records`
- `meal_logs`
- `user_profiles`
- `body_measurements`

## Lietošana

1. Pārliecinies, ka datorā ir uzstādīts Python.
2. Atver mapi terminālī. 
3. Palaid programmu ar komandu:
   ```bash
   python main.py