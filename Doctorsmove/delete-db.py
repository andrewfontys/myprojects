import pymysql

# Google Cloud Connection
db = pymysql.connect()

try:
    with db.cursor() as cursor:
        # Drop 'patients' database if it exists
        drop_db_query = "DROP DATABASE IF EXISTS patients"
        cursor.execute(drop_db_query)

    # Commit changes
    db.commit()
    print("Database 'patients' dropped successfully!")

except pymysql.Error as e:
    print(f"Error: {e}")

finally:
    db.close()
