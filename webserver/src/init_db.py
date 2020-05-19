
if __name__ == '__main__':
    # Import MySQL Connector Driver
    import mysql.connector as mysql

    # Load the credentials from the secured .env file
    import os
    from dotenv import load_dotenv
    load_dotenv('credentials.env')

    db_user = os.environ['MYSQL_USER']
    db_pass = os.environ['MYSQL_PASSWORD']
    db_name = os.environ['MYSQL_DATABASE']
    db_host = '192.168.99.100'# different than inside the container and assumes default port of 3306
    #db_name = os.environ['MYSQL_HOST']


    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()

    #Uncomment and Run to clear all users
    #cursor.execute("drop table if exists Users;")

    #Uncomment and Run to clear all moves
    #cursor.execute("drop table if exists Moves;")

    # Create a TStudents table (wrapping it in a try-except is good practice)
    try:
        cursor.execute("""
        CREATE TABLE Users (
        id integer  AUTO_INCREMENT PRIMARY KEY,
        first_name  VARCHAR(30) NOT NULL,
        last_name       VARCHAR(50) NOT NULL,
        email        VARCHAR(30) NOT NULL
        );
        """)

    except:
        print("Table already exists. Not recreating it.")
    try:
        cursor.execute("""
        CREATE TABLE Coordinates (
        id integer  AUTO_INCREMENT PRIMARY KEY,
        1_lat  VARCHAR(50) NOT NULL,
        1_long  VARCHAR(50) NOT NULL,
        2_lat  VARCHAR(50) NOT NULL,
        2_long  VARCHAR(50) NOT NULL,
        3_lat  VARCHAR(50) NOT NULL,
        3_long  VARCHAR(50) NOT NULL


        );
        """)
        

    except:
        print("UH OH")
    
    

    cursor.execute("""
        INSERT INTO Users (first_name, last_name, email)
        VALUE ('admin_first','admin_last','admin_email');""")
    db.commit()
    db.close()