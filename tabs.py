TABS = [
    {
        "title": "Lietotāji",
        "table": "users",
        "labels": ["Lietotājvārds", "E-pasts", "Parole"],
        "fields": ["username", "email", "password_hash"],
        "passwords": [False, False, True],
        "query": "SELECT id, username, email FROM users ORDER BY id",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājvārds", 160),
            ("email", "E-pasts", 260),
        ],
    },
    {
        "title": "Vingrinājumi",
        "table": "exercises",
        "labels": ["Nosaukums", "Apraksts", "Muskuļu grupa"],
        "fields": ["name", "description", "muscle_group"],
        "passwords": [False, False, False],
        "query": "SELECT id, name, description, muscle_group FROM exercises ORDER BY name",
        "columns": [
            ("id", "Nr.", 55),
            ("name", "Vingrinājums", 180),
            ("description", "Apraksts", 320),
            ("muscle_group", "Muskuļu grupa", 160),
        ],
    },
    {
        "title": "Treniņi",
        "table": "workouts",
        "labels": ["Lietotāja ID", "Treniņa nosaukums", "Piezīmes"],
        "fields": ["user_id", "session_name", "notes"],
        "passwords": [False, False, False],
        "query": """SELECT w.id, COALESCE(u.username, 'Nezināms lietotājs'),
                           w.session_name, w.workout_date, w.notes
                    FROM workouts AS w
                    LEFT JOIN users AS u ON u.id = w.user_id
                    ORDER BY w.workout_date DESC""",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājs", 145),
            ("session_name", "Treniņš", 180),
            ("workout_date", "Datums", 165),
            ("notes", "Piezīmes", 250),
        ],
    },
    {
        "title": "Piegājieni",
        "table": "workout_sets",
        "labels": [
            "Treniņa ID",
            "Vingrinājuma ID",
            "Piegājiena Nr.",
            "Svars (kg)",
            "Atkārtojumi",
        ],
        "fields": ["workout_id", "exercise_id", "set_number", "weight_kg", "reps"],
        "passwords": [False] * 5,
        "query": """SELECT s.id, COALESCE(w.session_name, 'Treniņš #' || s.workout_id),
                           COALESCE(e.name, 'Vingrinājums #' || s.exercise_id),
                           s.set_number, s.weight_kg, s.reps
                    FROM workout_sets AS s
                    LEFT JOIN workouts AS w ON w.id = s.workout_id
                    LEFT JOIN exercises AS e ON e.id = s.exercise_id
                    ORDER BY w.workout_date DESC, s.set_number""",
        "columns": [
            ("id", "Nr.", 55),
            ("session_name", "Treniņš", 170),
            ("exercise", "Vingrinājums", 180),
            ("set_number", "Piegājiens", 95),
            ("weight_kg", "Svars (kg)", 100),
            ("reps", "Atkārtojumi", 105),
        ],
    },
    {
        "title": "Rekordi",
        "table": "personal_records",
        "labels": ["Lietotāja ID", "Vingrinājuma ID", "Svars (kg)", "Atkārtojumi"],
        "fields": ["user_id", "exercise_id", "weight_kg", "reps"],
        "passwords": [False] * 4,
        "query": """SELECT r.id, COALESCE(u.username, 'Nezināms lietotājs'),
                           COALESCE(e.name, 'Vingrinājums #' || r.exercise_id),
                           r.weight_kg, r.reps, r.achieved_at
                    FROM personal_records AS r
                    LEFT JOIN users AS u ON u.id = r.user_id
                    LEFT JOIN exercises AS e ON e.id = r.exercise_id
                    ORDER BY r.achieved_at DESC""",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājs", 145),
            ("exercise", "Vingrinājums", 190),
            ("weight_kg", "Svars (kg)", 100),
            ("reps", "Atkārtojumi", 110),
            ("achieved_at", "Rekorda datums", 165),
        ],
    },
    {
        "title": "Uzturs",
        "table": "meal_logs",
        "labels": [
            "Lietotāja ID",
            "Ēdienreize",
            "Kalorijas (kcal)",
            "Olbaltumvielas (g)",
            "Ogļhidrāti (g)",
            "Tauki (g)",
        ],
        "fields": ["user_id", "meal_name", "calories", "protein_g", "carbs_g", "fats_g"],
        "passwords": [False] * 6,
        "query": """SELECT m.id, COALESCE(u.username, 'Nezināms lietotājs'),
                           m.meal_name, m.calories, m.protein_g, m.carbs_g, m.fats_g,
                           m.logged_date
                    FROM meal_logs AS m
                    LEFT JOIN users AS u ON u.id = m.user_id
                    ORDER BY m.logged_date DESC""",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājs", 140),
            ("meal_name", "Ēdiens", 170),
            ("calories", "Kalorijas (kcal)", 130),
            ("protein_g", "Olbaltumvielas (g)", 155),
            ("carbs_g", "Ogļhidrāti (g)", 145),
            ("fats_g", "Tauki (g)", 100),
            ("logged_date", "Datums", 165),
        ],
    },
    {
        "title": "Profili",
        "table": "user_profiles",
        "labels": ["Lietotāja ID", "Augums (cm)", "Mērķa svars (kg)", "Mērķi"],
        "fields": ["user_id", "height_cm", "target_weight_kg", "fitness_goals"],
        "passwords": [False] * 4,
        "query": """SELECT p.id, COALESCE(u.username, 'Nezināms lietotājs'),
                           p.height_cm, p.target_weight_kg, p.fitness_goals
                    FROM user_profiles AS p
                    LEFT JOIN users AS u ON u.id = p.user_id
                    ORDER BY u.username""",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājs", 150),
            ("height_cm", "Augums (cm)", 110),
            ("target_weight_kg", "Mērķa svars (kg)", 145),
            ("fitness_goals", "Fitnesa mērķi", 280),
        ],
    },
    {
        "title": "Mērījumi",
        "table": "body_measurements",
        "labels": [
            "Lietotāja ID",
            "Svars (kg)",
            "Tauku %",
            "Krūšu apkārtmērs (cm)",
            "Viduklis (cm)",
            "Gurnu apkārtmērs (cm)",
        ],
        "fields": [
            "user_id",
            "weight_kg",
            "body_fat_pct",
            "chest_cm",
            "waist_cm",
            "hips_cm",
        ],
        "passwords": [False] * 6,
        "query": """SELECT b.id, COALESCE(u.username, 'Nezināms lietotājs'),
                           b.weight_kg, b.body_fat_pct, b.chest_cm, b.waist_cm,
                           b.hips_cm, b.measured_at
                    FROM body_measurements AS b
                    LEFT JOIN users AS u ON u.id = b.user_id
                    ORDER BY b.measured_at DESC""",
        "columns": [
            ("id", "Nr.", 55),
            ("username", "Lietotājs", 145),
            ("weight_kg", "Svars (kg)", 105),
            ("body_fat_pct", "Tauku īpatsvars (%)", 150),
            ("chest_cm", "Krūšu apkārtmērs (cm)", 175),
            ("waist_cm", "Vidukļa apkārtmērs (cm)", 175),
            ("hips_cm", "Gurnu apkārtmērs (cm)", 165),
            ("measured_at", "Mērījuma datums", 165),
        ],
    },
]
