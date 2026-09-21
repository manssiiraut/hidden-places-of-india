password="mansi123",

csv_path = r"D:\New folder (2)\hidden_india_cleaned.csv"


import pandas as pd
import mysql.connector
import ast
import json


# ============================================================
# 1. CONNECT TO MYSQL
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mansi123",
    database="hidden_india"
)

cursor = conn.cursor()

print("Connected to MySQL successfully!")


# ============================================================
# 2. LOAD CSV FILE
# ============================================================

csv_path = r"D:\New folder (2)\hidden_india_cleaned.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. FUNCTION TO CONVERT CSV LIST VALUES
# ============================================================

def convert_to_list(value):

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    value = str(value).strip()

    if value == "" or value == "[]":
        return []

    try:
        result = ast.literal_eval(value)

        if isinstance(result, list):
            return result

        return [str(result)]

    except:

        try:
            result = json.loads(value)

            if isinstance(result, list):
                return result

            return [str(result)]

        except:

            return [value]


# ============================================================
# 4. INSERT DESTINATIONS
# ============================================================

print("\n------------------------------------------")
print("INSERTING DESTINATIONS")
print("------------------------------------------")

destination_query = """
INSERT IGNORE INTO destinations
(
    id,
    slug,
    name,
    state,
    region,
    tagline,
    overview,
    why_visit,
    type,
    budget,
    budget_label,
    duration_days,
    best_season,
    difficulty,
    crowd,
    alternative_to,
    latitude,
    longitude
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

for _, row in df.iterrows():

    values = (
        row["id"],
        row["slug"],
        row["name"],
        row["state"],
        row["region"],
        row["tagline"],
        row["overview"],
        row["why_visit"],
        row["type"],

        int(row["budget"])
        if pd.notna(row["budget"])
        else None,

        row["budget_label"],

        int(row["duration_days"])
        if pd.notna(row["duration_days"])
        else None,

        row["best_season"],
        row["difficulty"],
        row["crowd"],
        row["alternative_to"],

        float(row["latitude"])
        if pd.notna(row["latitude"])
        else None,

        float(row["longitude"])
        if pd.notna(row["longitude"])
        else None
    )

    cursor.execute(destination_query, values)

conn.commit()

print("Destinations processed:", len(df))


# ============================================================
# 5. INSERT STYLES
# ============================================================

print("\n------------------------------------------")
print("INSERTING STYLES")
print("------------------------------------------")

for _, row in df.iterrows():

    styles = convert_to_list(row["styles"])

    for style in styles:

        style = str(style).strip()

        if style:

            cursor.execute(
                """
                INSERT IGNORE INTO styles
                (style_name)
                VALUES (%s)
                """,
                (style,)
            )

conn.commit()

print("Styles inserted.")


# ============================================================
# 6. DESTINATION - STYLE RELATIONSHIP
# ============================================================

print("Creating destination-style relationships...")

for _, row in df.iterrows():

    destination_id = row["id"]

    styles = convert_to_list(row["styles"])

    for style in styles:

        style = str(style).strip()

        if not style:
            continue

        cursor.execute(
            """
            SELECT style_id
            FROM styles
            WHERE style_name = %s
            """,
            (style,)
        )

        result = cursor.fetchone()

        if result:

            style_id = result[0]

            cursor.execute(
                """
                INSERT IGNORE INTO destination_styles
                (
                    destination_id,
                    style_id
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    style_id
                )
            )

conn.commit()

print("Destination-style relationships created.")


# ============================================================
# 7. INSERT SEASONS
# ============================================================

print("\n------------------------------------------")
print("INSERTING SEASONS")
print("------------------------------------------")

for _, row in df.iterrows():

    seasons_list = convert_to_list(row["seasons"])

    for season in seasons_list:

        season = str(season).strip()

        if season:

            cursor.execute(
                """
                INSERT IGNORE INTO seasons
                (season_name)
                VALUES (%s)
                """,
                (season,)
            )

conn.commit()

print("Seasons inserted.")


# ============================================================
# 8. DESTINATION - SEASON RELATIONSHIP
# ============================================================

print("Creating destination-season relationships...")

for _, row in df.iterrows():

    destination_id = row["id"]

    seasons_list = convert_to_list(row["seasons"])

    for season in seasons_list:

        season = str(season).strip()

        if not season:
            continue

        cursor.execute(
            """
            SELECT season_id
            FROM seasons
            WHERE season_name = %s
            """,
            (season,)
        )

        result = cursor.fetchone()

        if result:

            season_id = result[0]

            cursor.execute(
                """
                INSERT IGNORE INTO destination_seasons
                (
                    destination_id,
                    season_id
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    season_id
                )
            )

conn.commit()

print("Destination-season relationships created.")


# ============================================================
# 9. INSERT ACTIVITIES
# ============================================================

print("\n------------------------------------------")
print("INSERTING ACTIVITIES")
print("------------------------------------------")

for _, row in df.iterrows():

    activities = convert_to_list(row["things_to_do"])

    for activity in activities:

        activity = str(activity).strip()

        if activity:

            cursor.execute(
                """
                INSERT IGNORE INTO activities
                (activity_name)
                VALUES (%s)
                """,
                (activity,)
            )

conn.commit()

print("Activities inserted.")


# ============================================================
# 10. DESTINATION - ACTIVITY RELATIONSHIP
# ============================================================

print("Creating destination-activity relationships...")

for _, row in df.iterrows():

    destination_id = row["id"]

    activities = convert_to_list(row["things_to_do"])

    for activity in activities:

        activity = str(activity).strip()

        if not activity:
            continue

        cursor.execute(
            """
            SELECT activity_id
            FROM activities
            WHERE activity_name = %s
            """,
            (activity,)
        )

        result = cursor.fetchone()

        if result:

            activity_id = result[0]

            cursor.execute(
                """
                INSERT IGNORE INTO destination_activities
                (
                    destination_id,
                    activity_id
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    activity_id
                )
            )

conn.commit()

print("Destination-activity relationships created.")


# ============================================================
# 11. INSERT FOODS
# ============================================================

print("\n------------------------------------------")
print("INSERTING FOODS")
print("------------------------------------------")

for _, row in df.iterrows():

    destination_id = row["id"]

    foods = convert_to_list(row["food"])

    for food in foods:

        food = str(food).strip()

        if food:

            cursor.execute(
                """
                INSERT INTO foods
                (
                    destination_id,
                    food_name
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    food
                )
            )

conn.commit()

print("Foods inserted.")


# ============================================================
# 12. INSERT CAFES
# ============================================================

print("\n------------------------------------------")
print("INSERTING CAFES")
print("------------------------------------------")

for _, row in df.iterrows():

    destination_id = row["id"]

    cafes = convert_to_list(row["cafes"])

    for cafe in cafes:

        cafe = str(cafe).strip()

        if cafe:

            cursor.execute(
                """
                INSERT INTO cafes
                (
                    destination_id,
                    cafe_name
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    cafe
                )
            )

conn.commit()

print("Cafes inserted.")


# ============================================================
# 13. INSERT IMAGES
# ============================================================

print("\n------------------------------------------")
print("INSERTING IMAGES")
print("------------------------------------------")

for _, row in df.iterrows():

    destination_id = row["id"]

    # -------------------------
    # COVER IMAGE
    # -------------------------

    cover = row["cover"]

    if pd.notna(cover):

        cover = str(cover).strip()

        if cover:

            cursor.execute(
                """
                INSERT INTO destination_images
                (
                    destination_id,
                    image_url,
                    image_type
                )
                VALUES (%s, %s, %s)
                """,
                (
                    destination_id,
                    cover,
                    "cover"
                )
            )

    # -------------------------
    # GALLERY IMAGES
    # -------------------------

    gallery = convert_to_list(row["gallery"])

    for image in gallery:

        image = str(image).strip()

        if image:

            cursor.execute(
                """
                INSERT INTO destination_images
                (
                    destination_id,
                    image_url,
                    image_type
                )
                VALUES (%s, %s, %s)
                """,
                (
                    destination_id,
                    image,
                    "gallery"
                )
            )

conn.commit()

print("Images inserted.")


# ============================================================
# 14. INSERT PHOTO SPOTS
# ============================================================

print("\n------------------------------------------")
print("INSERTING PHOTO SPOTS")
print("------------------------------------------")

for _, row in df.iterrows():

    destination_id = row["id"]

    spots = convert_to_list(row["photo_spots"])

    for spot in spots:

        spot = str(spot).strip()

        if spot:

            cursor.execute(
                """
                INSERT INTO photo_spots
                (
                    destination_id,
                    spot_name
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    spot
                )
            )

conn.commit()

print("Photo spots inserted.")


# ============================================================
# 15. CREATE DESTINATION NAME → ID MAPPING
# ============================================================

print("\n------------------------------------------")
print("CREATING DESTINATION MAPPING")
print("------------------------------------------")

cursor.execute(
    """
    SELECT id, name
    FROM destinations
    """
)

destination_rows = cursor.fetchall()

destination_map = {}

for destination_id, name in destination_rows:

    destination_map[
        str(name).strip().lower()
    ] = destination_id

print(
    "Destination mapping created:",
    len(destination_map)
)


# ============================================================
# 16. INSERT NEARBY DESTINATIONS
# ============================================================

print("\n------------------------------------------")
print("INSERTING NEARBY DESTINATIONS")
print("------------------------------------------")

nearby_count = 0

for _, row in df.iterrows():

    destination_id = row["id"]

    nearby_list = convert_to_list(row["nearby"])

    for nearby_name in nearby_list:

        nearby_name = str(nearby_name).strip()

        if not nearby_name:
            continue

        nearby_id = destination_map.get(
            nearby_name.lower()
        )

        if nearby_id:

            cursor.execute(
                """
                INSERT IGNORE INTO nearby_destinations
                (
                    destination_id,
                    nearby_destination_id
                )
                VALUES (%s, %s)
                """,
                (
                    destination_id,
                    nearby_id
                )
            )

            nearby_count += 1

conn.commit()

print(
    "Nearby destination relationships inserted:",
    nearby_count
)


# ============================================================
# 17. FINAL DATABASE CHECK
# ============================================================

print("\n==========================================")
print("DATABASE IMPORT COMPLETED")
print("==========================================")

tables = [
    "destinations",
    "styles",
    "destination_styles",
    "seasons",
    "destination_seasons",
    "activities",
    "destination_activities",
    "foods",
    "cafes",
    "destination_images",
    "photo_spots",
    "nearby_destinations"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count} rows")


# ============================================================
# 18. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("\n==========================================")
print("      HIDDEN INDIA DATABASE READY! 🌄")
print("==========================================")