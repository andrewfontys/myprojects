import mysql.connector

# create a connection to the "doctors" database
conn = mysql.connector.connect(
)
cursor = conn.cursor()

# create a table for doctors with columns for email and password
cursor.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (email VARCHAR(255) UNIQUE, password VARCHAR(255))''')

# insert test data 
cursor.execute("INSERT INTO doctors VALUES ('director@example.com', 'password1')")
cursor.execute("INSERT INTO doctors VALUES ('msmith@example.com', 'password2')")
cursor.execute("INSERT INTO doctors VALUES ('rjohnson@example.com', 'password3')")

# Create a table to store submissions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255),
        company_mail VARCHAR(255) UNIQUE,
        region VARCHAR(255),
        continent VARCHAR(255)
    )
''')

# save the changes and close the connection
conn.commit()
conn.close()

