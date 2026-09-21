import pandas as pd
import mysql.connector
import ast

# ==========================================
# 1. CONNECT TO MYSQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mansi123",
    database="hidden_india"
)

cursor = conn.cursor()

print("Connected to MySQL successfully!")


# ==========================================
# 2. LOAD CSV
# ==========================================

csv_path = r"D:\New folder (2)\hidden_india_cleaned.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully!")
print("Total destinations:", len(df))


# ==========================================
# 3. CREATE DESTINATION NAME → ID MAPPING
# ==========================================

cursor.execute("""
    SELECT id, name
    FROM destinations
""")

rows = cursor.fetchall()

destination_map = {}

for destination_id, name in rows:
    destination_map[str(name).strip().lower()] = destination_id


# ==========================================
# 4. INSERT NEARBY PLACES
# ==========================================

insert_query = """
    INSERT INTO nearby_places
    (
        destination_id,
        place_name
    )
    VALUES (%s, %s)
"""

total_inserted = 0
destinations_with_nearby = 0

for _, row in df.iterrows():

    destination_name = str(row["name"]).strip()

    nearby_value = row["nearby"]

    # Skip empty values
    if pd.isna(nearby_value):
        continue

    nearby_value = str(nearby_value).strip()

    if nearby_value == "" or nearby_value == "[]":
        continue

    # Convert string representation of list into Python list
    try:
        nearby_list = ast.literal_eval(nearby_value)
    except:
        nearby_list = [nearby_value]

    if not isinstance(nearby_list, list):
        nearby_list = [nearby_list]

    destination_id = destination_map.get(
        destination_name.lower()
    )

    if not destination_id:
        print("Destination not found:", destination_name)
        continue

    destinations_with_nearby += 1

    for place in nearby_list:

        place = str(place).strip()

        if place:

            cursor.execute(
                insert_query,
                (
                    destination_id,
                    place
                )
            )

            total_inserted += 1


# ==========================================
# 5. SAVE CHANGES
# ==========================================

conn.commit()


# ==========================================
# 6. SHOW RESULT
# ==========================================

print("\n==========================================")
print("NEARBY PLACES IMPORT COMPLETED")
print("==========================================")

print(
    "Destinations with nearby information:",
    destinations_with_nearby
)

print(
    "Nearby places inserted:",
    total_inserted
)


# ==========================================
# 7. VERIFY DATABASE
# ==========================================

cursor.execute("""
    SELECT COUNT(*)
    FROM nearby_places
""")

count = cursor.fetchone()[0]

print(
    "Total nearby_places rows in database:",
    count
)


# ==========================================
# 8. CLOSE CONNECTION
# ==========================================

cursor.close()
conn.close()

print("\nDatabase connection closed.")
print("Nearby places are ready! ✅")