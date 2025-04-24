import mysql.connector
from mysql.connector import Error

def display_menu():
    print("\n--- Academy Awards Query Menu ---")
    print("1. Register a user")
    print("2. Add a new user nomination for a staff member for a given movie")
    print("3. View existing nominations for a user")
    print("4. View top nominated movies by users in each category/year")
    print("5. Show total nominations and Oscars for a director, actor, and singer")
    print("6. Show top 5 birth countries for actors who won Best Actor")
    print("7. Show nominated staff from a country with categories, nominations, and wins")
    print("8. Dream Team - best living cast (director, actors, etc.)")
    print("9. Show top 5 production companies by won Oscars")
    print("10. List non-English movies that won an Oscar with year")
    print("0. Exit")

# Reusable query template (for simplicity, I'm using the same query across all options)
def get_nominations(query, cursor):
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    print("\nResults:\n")
    print(columns)  # Print column headers
    for row in rows:
        print(row)

def register_user(cursor):
    user_name = input("\nEnter your username: ").strip()
    email_address = input("Enter your email address: ").strip()
    birth_date = input("Enter your birthdate (YYYY-MM-DD): ").strip()

    # Calculate age based on birth year and the current year (2024)
    birth_year = int(birth_date.split('-')[0])
    age = 2024 - birth_year

    gender = input("Enter your gender: ").strip()
    country = input("Enter your country: ").strip()

    query = """
        INSERT INTO user (Username, EmailAddress, BirthDate, Age, Gender, Country)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (user_name, email_address, birth_date, age, gender, country))
    print(f"User {user_name} registered successfully!")
    
def add_nomination(cursor):
    email = input("\nEnter your email address: ").strip()

    # Query to check if the user exists based on the email
    check_user_query = """
        SELECT *
        FROM user
        WHERE EmailAddress = %s;
    """
    cursor.execute(check_user_query, (email,))
    user_exists = cursor.fetchone()

    # If the user doesn't exist, print a message and exit
    if not user_exists:
        print(f"No user found with the email '{email}'. Please ensure your email is correct.")
        return

    movie_name = input("\nEnter the movie name: ").strip()
    release = input ("Enter the release year of the movie: ").strip()

    category = input("Enter the nomination category: ").strip()
    staff_fname = input("Enter the staff first name: ").strip()
    staff_lname = input("Enter the staff last name: ").strip()
    # Query to check if the movie exists
    check_movie_query = """
    SELECT Movie
    FROM movies
    WHERE Movie = %s AND ReleaseYear = %s;
"""

    cursor.execute(check_movie_query, (movie_name, release))
    movie_exists = cursor.fetchone()

    # If the movie doesn't exist, print an error and exit
    if not movie_exists:
        print(f"Error: The movie '{movie_name}' does not exist in the database. Nomination not added.")
        return

    # Fetch all results (even if it's just one row)
    cursor.fetchall()

    # Query to check if the staff exists
    check_staff_query = """
        SELECT firstName, lastName
        FROM staff
        WHERE firstName LIKE %s and lastName LIKE %s;
    """
    cursor.execute(check_staff_query, (staff_fname, staff_lname))
    staff_exists = cursor.fetchone()

    # If the staff doesn't exist, print an error and exit
    if not staff_exists:
        print(f"Error: The staff '{staff_lname}' does not exist in the database. Nomination not added.")
        return

    # Fetch all results (even if it's just one row)
    cursor.fetchall()

    # Query to check if the category exists
    check_category_query = """
        SELECT Category
        FROM oscarnominates
        WHERE Category = %s;
    """
    cursor.execute(check_category_query, (category,))
    category_exists = cursor.fetchone()

    # If the category doesn't exist, print an error and exit
    if not category_exists:
        print(f"Error: The category '{category}' does not exist. Nomination not added.")
        return

    # Fetch all results (even if it's just one row)
    cursor.fetchall()

    # Add the nomination entry
    add_nomination_query = """
        INSERT INTO usernominations (MovieName, Category, sFirstName, sLastNAme, ReleaseYear, EmailAddress)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(add_nomination_query, (movie_name, category, staff_fname, staff_lname,release ,email))

    print(f"Nomination for '{movie_name}' in category '{category}' added successfully.")


def view_user_nominations(cursor):
    email_address = input("\nEnter your email address: ").strip()

    # Query to fetch nominations for the given email address
    query = """
        SELECT MovieName, Category, ReleaseYear
        FROM usernominations
        WHERE EmailAddress = %s;
    """
    cursor.execute(query, (email_address,))
    rows = cursor.fetchall()

    if rows:
        # Get column names
        columns = [desc[0] for desc in cursor.description]

        print("\nUser Nominations:\n")
        print(columns)  # Print column headers
        for row in rows:
            # Convert ReleaseYear to int
            row_with_int_year = (row[0], row[1], int(row[2]))  # row[2] is ReleaseYear
            print(row_with_int_year)
    else:
        print(f"No nominations found for user with email: {email_address}")


def get_top_nominated_movies_per_year(cursor):
    year = input("\nEnter the year (YYYY): ").strip()

    # Query to fetch the top nominated movies for a specific year
    query = """
        SELECT MovieName, Category, COUNT(*) AS NominationCount
        FROM usernominations
        WHERE ReleaseYear = %s
        GROUP BY MovieName, Category
        ORDER BY NominationCount DESC
        LIMIT 20;
    """
    cursor.execute(query, (year,))
    rows = cursor.fetchall()

    if rows:
        columns = [desc[0] for desc in cursor.description]

        print("\nTop Nominated Movies for Year", year, ":\n")
        print(columns)  # Print column headers
        for row in rows:
            print(row)
    else:
        print(f"No nominations found for the year {year}.")

def get_top_nominated_movies_per_category(cursor):
    category = input("\nEnter the category: ").strip()

    # Query to fetch the top nominated movies for a specific category
    query = """
        SELECT MovieName, CAST(ReleaseYear AS UNSIGNED) AS ReleaseYear, COUNT(*) AS NominationCount
        FROM usernominations
        WHERE Category LIKE %s
        GROUP BY MovieName, ReleaseYear
        ORDER BY NominationCount DESC
        LIMIT 20;
    """
    cursor.execute(query, (category,))
    rows = cursor.fetchall()

    if rows:
        columns = [desc[0] for desc in cursor.description]

        print("\nTop Nominated Movies for Category:", category, ":\n")
        print(columns)  # Print column headers
        for row in rows:
            print(row)
    else:
        print(f"No nominations found for the category {category}.")

def get_top_nominated_movies(cursor):
    print("\n--- Top Nominated Movies ---")
    print("1. Top nominations per year")
    print("2. Top nominations per category")
    print("0. Back to main menu")

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        get_top_nominated_movies_per_year(cursor)
    elif choice == '2':
        get_top_nominated_movies_per_category(cursor)
    elif choice == '0':
        return
    else:
        print("Invalid option. Please try again.")

def show_total_nominations(cursor):
    print("\n--- Show Total Nominations and Oscars ---")
    print("1. Directors")
    print("2. Actors")
    print("3. Singers")
    print("0. Back to main menu")

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        first_name = input("Enter the director's first name: ").strip()
        last_name = input("Enter the director's last name: ").strip()

        # Check if the occupation contains 'Director'
        occupation_check_query = """
            SELECT firstName, lastName 
            FROM staffroles 
            WHERE occupations LIKE %s AND firstName = %s AND lastName = %s;
        """
        cursor.execute(occupation_check_query, ('%Director%', first_name, last_name))
        occupation = cursor.fetchone()

        if occupation:  # If the director exists
            # Get total nominations for the director
            nominations_query = """
                SELECT e.firstName, e.lastName, COUNT(*) AS TotalNominations
                FROM oscarnominates o
                JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND e.category = o.category
                WHERE e.firstName = %s AND e.lastName = %s 
                GROUP BY e.firstName, e.lastName;
            """
            cursor.execute(nominations_query, (first_name, last_name))
            rows = cursor.fetchall()

            if rows:
                columns = [desc[0] for desc in cursor.description]
                print("\nDirector's Total Nominations:\n")
                print(columns)
                for row in rows:
                    print(row)
            else:
                print(f"No nominations found for the director: {first_name} {last_name}")
        else:
            print(f"The director {first_name} {last_name} does not exist or occupation does not match.")

    elif choice == '2':
        first_name = input("Enter the actor's first name: ").strip()
        last_name = input("Enter the actor's last name: ").strip()

        # Check if the occupation contains 'Actor'
        occupation_check_query = """
            SELECT firstName, lastName 
            FROM staffroles 
            WHERE occupations LIKE %s AND firstName = %s AND lastName = %s;
        """
        cursor.execute(occupation_check_query, ('%Actor%', first_name, last_name))
        occupation = cursor.fetchone()

        if occupation:  # If the actor exists
            # Get total nominations for the actor
            nominations_query = """
                SELECT e.firstName, e.lastName, COUNT(*) AS TotalNominations
                FROM oscarnominates o
                JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND e.category = o.category
                WHERE e.firstName = %s AND e.lastName = %s 
                GROUP BY e.firstName, e.lastName;
            """
            cursor.execute(nominations_query, (first_name, last_name))
            rows = cursor.fetchall()

            if rows:
                columns = [desc[0] for desc in cursor.description]
                print("\nActor's Total Nominations:\n")
                print(columns)
                for row in rows:
                    print(row)
            else:
                print(f"No nominations found for the actor: {first_name} {last_name}")
        else:
            print(f"The actor {first_name} {last_name} does not exist or occupation does not match.")

    elif choice == '3':
        first_name = input("Enter the singer's first name: ").strip()
        last_name = input("Enter the singer's last name: ").strip()

        # Check if the occupation contains 'Singer'
        occupation_check_query = """
            SELECT firstName, lastName 
            FROM staffroles 
            WHERE occupations LIKE %s AND firstName = %s AND lastName = %s;
        """
        cursor.execute(occupation_check_query, ('%Singer%', first_name, last_name))
        occupation = cursor.fetchone()

        if occupation:  # If the singer exists
            # Get total nominations for the singer
            nominations_query = """
                SELECT e.firstName, e.lastName, COUNT(*) AS TotalNominations
                FROM oscarnominates o
                JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND e.category = o.category
                WHERE e.firstName = %s AND e.lastName = %s 
                GROUP BY e.firstName, e.lastName;
            """
            cursor.execute(nominations_query, (first_name, last_name))
            rows = cursor.fetchall()

            if rows:
                columns = [desc[0] for desc in cursor.description]
                print("\nSinger's Total Nominations:\n")
                print(columns)
                for row in rows:
                    print(row)
            else:
                print(f"No nominations found for the singer: {first_name} {last_name}")
        else:
            print(f"The singer {first_name} {last_name} does not exist or occupation does not match.")

    elif choice == '0':
        return
    else:
        print("Invalid option. Please try again.")




def top_birth_countries(cursor):
    print("\n--- Show Top 5 Birth Countries for Actors Who Won Best Actor ---")
    
    # SQL Query to get top 5 countries by actor wins
    query = """
    SELECT s.CountryOfBirth, COUNT(*) AS WinCount
    FROM oscarnominates o
    JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
    JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
    WHERE (o.Category = 'Best Actor' or o.Category = 'Best Actor in a Leading Role') AND o.isWon = 1 AND s.CountryOfBirth is NOT NULL
    GROUP BY s.CountryOfBirth
    ORDER BY WinCount DESC
    LIMIT 5;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    print("\nTop 5 Birth Countries for Best Actor Winners:\n")
    print(columns)  # Print column headers
    for row in rows:
        print(row)
def nominated_staff_by_country(cursor):
    country = input("\nEnter the country to see nominated staff: ").strip()

    # Ask if the user wants to include categories
    include_categories = input("Do you want to include categories? (yes/no): ").strip().lower()

    # Add % to the country to enable LIKE pattern matching
    country_pattern = f"%{country}%"

    # Modify query based on the user's choice to include categories or not
    if include_categories == 'yes':
        query = """
        SELECT s.firstName, s.lastName, e.category, isWon As Won
        FROM oscarnominates o
        JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
        JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
        WHERE s.CountryOfBirth LIKE %s
        """
    else:
        query = """
        SELECT s.firstName, s.lastName, 
               COUNT(*) AS TotalNominations, 
               SUM(CASE WHEN o.isWon = 1 THEN 1 ELSE 0 END) AS TotalWins
        FROM oscarnominates o
        JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
        JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
        WHERE s.CountryOfBirth LIKE %s
        GROUP BY s.firstName, s.lastName
        ORDER BY TotalNominations DESC;
        """
    
    cursor.execute(query, (country_pattern,))
    rows = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    print("\nNominated Staff from countries containing", country, "with Categories, Nominations, and Wins:\n")
    print(columns)  # Print column headers

    for row in rows:
        # Check how many columns are returned
        if include_categories == 'yes':
            # For results including categories
            firstName, lastName, category, Won = row
            print(f"{firstName} {lastName} - Category: {category}, Won: {Won}")
        else:
            # For results without categories
            firstName, lastName, totalNominations, totalWins = row
            totalNominations = int(totalNominations)  # Convert Decimal to int (TotalNominations)
            totalWins = int(totalWins)  # Convert Decimal to int (TotalWins)
            print(f"{firstName} {lastName} - Nominations: {totalNominations}, Wins: {totalWins}")



def dream_team_best_cast(cursor):
    # Define the SQL queries for each category
    queries = {
        'director': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Directing' OR o.Category LIKE 'Best Director' )
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """,
        'actor': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Actor' OR o.Category LIKE 'Best Actor in a Leading Role%')
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """,
        'actress': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Actress%' OR o.Category LIKE 'Best Actress in a Leading Role%')
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """,
        'supporting_actor': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Supporting Actor%' OR o.Category LIKE 'Best Actor in a Supporting Role%')
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """,
        'supporting_actress': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Supporting Actress%' OR o.Category LIKE 'Best Actress in a Supporting Role%')
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """,
        'producer': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE (o.Category LIKE '%Best Picture%' or o.Category LIKE '%Outstanding Picture%') 
              AND o.isWon = 1
              AND s.DeathDate IS NULL
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;  
        """,
        'score_singer': """
            SELECT s.firstName, s.lastName, COUNT(*) AS TotalWins
            FROM oscarnominates o
            JOIN employs e ON o.MovieName = e.movieName AND o.Iteration = e.Iteration AND o.Category = e.category
            JOIN staff s ON e.firstName = s.firstName AND e.lastName = s.lastName
            WHERE s.DeathDate IS NULL
              AND (o.Category LIKE 'Best Music (Original Song)' or o.Category LIKE 'Best Music (Song%' )
              AND o.isWon = 1
            GROUP BY s.firstName, s.lastName
            ORDER BY TotalWins DESC
            LIMIT 1;
        """
    }

    # Initialize dictionary to store the Dream Team results
    dream_team = {}

    # Execute each query sequentially
    for role, query in queries.items():
        try:
            cursor.execute(query)
            row = cursor.fetchone()  # Fetch only the top result (1 row)
            if row:
                if role == 'producer':  # For the producer, handle it differently
                    firstName, lastName, total_wins = row
                    total_wins = int(total_wins)  # Convert Decimal to int (TotalWins)
                    dream_team[role] = f"{firstName} {lastName} - Wins: {totalWins}"
                else:
                    firstName, lastName, totalWins = row
                    totalWins = int(totalWins)  # Convert Decimal to int (TotalWins)
                    dream_team[role] = f"{firstName} {lastName} - Wins: {totalWins}"
            else:
                dream_team[role] = "No winner found"
        except Exception as e:
            print(f"Error processing query for {role}: {e}")

    # Print the Dream Team output
    print("\nDream Team - Best Cast Members for the Best Movie Ever:")
    for role, member in dream_team.items():
        print(f"{role.capitalize()}: {member}")


def top_production_companies(cursor):
    query = """
        SELECT pr.ProductionCompany, COUNT(*) AS TotalWins
            FROM produces pr
            JOIN oscarnominates o ON pr.Movie = o.MovieName AND pr.OrdinalYear = o.Iteration
            WHERE (o.Category LIKE '%Best Picture%' or o.Category LIKE '%Outstanding Picture%') 
              AND o.isWon = 1
            GROUP BY pr.ProductionCompany
            ORDER BY TotalWins DESC
            LIMIT 5;  -- Top Production Company with most wins
    """
    get_nominations(query, cursor)

def list_non_english_movies(cursor):
    query = """
        SELECT Distinct o.MovieName, o.Iteration, m.Language
        FROM oscarnominates o
        JOIN movies m ON o.MovieName = m.Movie and o.Iteration = m.OrdinalYear
        WHERE o.isWon = 1 AND m.Language != NULL
        AND m.Language != 'English';

    """
    get_nominations(query, cursor)

try:
    connection = mysql.connector.connect(
        host="sql7.freesqldatabase.com",
        user="sql7774986",
        password="qGIlVa7ysQ",
        database="sql7774986",
        port=3306
    )

    if connection.is_connected():
        cursor = connection.cursor()

        while True:
            # Display the menu
            display_menu()

            # Get user choice
            choice = input("\nEnter the number of your choice: ").strip()

            if choice == '1':
                register_user(cursor)
                connection.commit()  # Commit the changes after registering a user
            elif choice == '2':
                add_nomination(cursor)
            elif choice == '3':
                view_user_nominations(cursor)
            elif choice == '4':
                get_top_nominated_movies(cursor)
            elif choice == '5':
                show_total_nominations(cursor)
            elif choice == '6':
                top_birth_countries(cursor)
            elif choice == '7':
                nominated_staff_by_country(cursor)
            elif choice == '8':
                dream_team_best_cast(cursor)
            elif choice == '9':
                top_production_companies(cursor)
            elif choice == '10':
                list_non_english_movies(cursor)
            elif choice == '0':
                print("Exiting program.")
                connection.commit()  # Commit any changes before exiting
                break
            else:
                print("Invalid option. Please try again.")

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed.")
