
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class AcademyAwardsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academy Awards Database")
        self.root.geometry("800x600")
        
        # Database connection
        self.connection = None
        self.cursor = None
        self.connect_to_database()
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Notebook for different tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_register_tab()
        self.create_nomination_tab()
        self.create_view_nominations_tab()
        self.create_statistics_tab()

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="sql7.freesqldatabase.com",
                user="sql7774986",
                password="qGIlVa7ysQ",
                database="sql7774986",
                port=3306
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")

    def create_register_tab(self):
        register_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(register_frame, text="Register User")
        
        # User registration form
        ttk.Label(register_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.username).grid(row=0, column=1, pady=5)
        
        ttk.Label(register_frame, text="Email:").grid(row=1, column=0, pady=5)
        self.email = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.email).grid(row=1, column=1, pady=5)
        
        ttk.Label(register_frame, text="Birth Date (YYYY-MM-DD):").grid(row=2, column=0, pady=5)
        self.birth_date = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.birth_date).grid(row=2, column=1, pady=5)
        
        ttk.Label(register_frame, text="Gender:").grid(row=3, column=0, pady=5)
        self.gender = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.gender).grid(row=3, column=1, pady=5)
        
        ttk.Label(register_frame, text="Country:").grid(row=4, column=0, pady=5)
        self.country = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.country).grid(row=4, column=1, pady=5)
        
        ttk.Button(register_frame, text="Register", command=self.register_user).grid(row=5, column=0, columnspan=2, pady=20)

    def create_nomination_tab(self):
        nomination_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(nomination_frame, text="Add Nomination")
        
        # Nomination form
        ttk.Label(nomination_frame, text="Email:").grid(row=0, column=0, pady=5)
        self.nom_email = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.nom_email).grid(row=0, column=1, pady=5)
        
        ttk.Label(nomination_frame, text="Movie Name:").grid(row=1, column=0, pady=5)
        self.movie_name = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.movie_name).grid(row=1, column=1, pady=5)
        
        ttk.Label(nomination_frame, text="Release Year:").grid(row=2, column=0, pady=5)
        self.release_year = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.release_year).grid(row=2, column=1, pady=5)
        
        ttk.Label(nomination_frame, text="Category:").grid(row=3, column=0, pady=5)
        self.category = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.category).grid(row=3, column=1, pady=5)
        
        ttk.Label(nomination_frame, text="Staff First Name:").grid(row=4, column=0, pady=5)
        self.staff_fname = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.staff_fname).grid(row=4, column=1, pady=5)
        
        ttk.Label(nomination_frame, text="Staff Last Name:").grid(row=5, column=0, pady=5)
        self.staff_lname = tk.StringVar()
        ttk.Entry(nomination_frame, textvariable=self.staff_lname).grid(row=5, column=1, pady=5)
        
        ttk.Button(nomination_frame, text="Add Nomination", command=self.add_nomination).grid(row=6, column=0, columnspan=2, pady=20)

    def create_view_nominations_tab(self):
        view_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(view_frame, text="View Nominations")
        
        ttk.Label(view_frame, text="Email:").grid(row=0, column=0, pady=5)
        self.view_email = tk.StringVar()
        ttk.Entry(view_frame, textvariable=self.view_email).grid(row=0, column=1, pady=5)
        
        ttk.Button(view_frame, text="View Nominations", command=self.view_nominations).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Treeview for nominations
        self.nominations_tree = ttk.Treeview(view_frame, columns=("Movie", "Category", "Year"), show="headings")
        self.nominations_tree.heading("Movie", text="Movie")
        self.nominations_tree.heading("Category", text="Category")
        self.nominations_tree.heading("Year", text="Year")
        self.nominations_tree.grid(row=2, column=0, columnspan=2, pady=10)

    def create_statistics_tab(self):
        stats_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(stats_frame, text="Statistics")
        
        buttons = [
            ("Top Nominated Movies", self.show_top_nominations),
            ("Birth Countries Stats", self.show_birth_countries),
            ("Staff by Country", self.show_staff_by_country),
            ("Dream Team", self.show_dream_team),
            ("Top Production Companies", self.show_top_companies),
            ("Non-English Winners", self.show_non_english_winners)
        ]
        
        for i, (text, command) in enumerate(buttons):
            ttk.Button(stats_frame, text=text, command=command).grid(row=i, column=0, pady=5, padx=5, sticky="ew")

    def register_user(self):
        try:
            birth_year = int(self.birth_date.get().split('-')[0])
            age = 2024 - birth_year
            
            query = """
                INSERT INTO user (Username, EmailAddress, BirthDate, Age, Gender, Country)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (
                self.username.get(),
                self.email.get(),
                self.birth_date.get(),
                age,
                self.gender.get(),
                self.country.get()
            ))
            self.connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")

    def add_nomination(self):
        try:
            # Check if user exists
            self.cursor.execute("SELECT * FROM user WHERE EmailAddress = %s", (self.nom_email.get(),))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "User not found!")
                return
            
            # Add nomination logic
            query = """
                INSERT INTO usernominations (MovieName, Category, sFirstName, sLastName, ReleaseYear, EmailAddress)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (
                self.movie_name.get(),
                self.category.get(),
                self.staff_fname.get(),
                self.staff_lname.get(),
                self.release_year.get(),
                self.nom_email.get()
            ))
            self.connection.commit()
            messagebox.showinfo("Success", "Nomination added successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Error adding nomination: {e}")

    def view_nominations(self):
        try:
            query = """
                SELECT MovieName, Category, ReleaseYear
                FROM usernominations
                WHERE EmailAddress = %s;
            """
            self.cursor.execute(query, (self.view_email.get(),))
            nominations = self.cursor.fetchall()
            
            # Clear existing items
            for item in self.nominations_tree.get_children():
                self.nominations_tree.delete(item)
            
            # Add new items
            for nom in nominations:
                self.nominations_tree.insert("", "end", values=nom)
                
        except Error as e:
            messagebox.showerror("Error", f"Error viewing nominations: {e}")

    def show_top_nominations(self):
        try:
            query = """
                SELECT MovieName, Category, COUNT(*) as Count
                FROM usernominations
                GROUP BY MovieName, Category
                ORDER BY Count DESC
                LIMIT 10;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.show_results("Top Nominated Movies", results)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching top nominations: {e}")

    def show_birth_countries(self):
        try:
            query = """
                SELECT s.CountryOfBirth, COUNT(*) AS WinCount
                FROM oscarnominates o
                JOIN employs e ON o.MovieName = e.movieName 
                JOIN staff s ON e.firstName = s.firstName 
                WHERE o.Category = 'Best Actor' AND o.isWon = 1
                GROUP BY s.CountryOfBirth
                ORDER BY WinCount DESC
                LIMIT 5;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.show_results("Top Birth Countries", results)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching birth countries: {e}")

    def show_staff_by_country(self):
        country = tk.simpledialog.askstring("Input", "Enter country name:")
        if country:
            try:
                query = """
                    SELECT firstName, lastName, COUNT(*) as Nominations
                    FROM staff s
                    JOIN employs e ON s.firstName = e.firstName
                    WHERE s.CountryOfBirth LIKE %s
                    GROUP BY firstName, lastName;
                """
                self.cursor.execute(query, (f"%{country}%",))
                results = self.cursor.fetchall()
                self.show_results(f"Staff from {country}", results)
            except Error as e:
                messagebox.showerror("Error", f"Error fetching staff: {e}")

    def show_dream_team(self):
        try:
            query = """
                SELECT s.firstName, s.lastName, sr.occupations, COUNT(*) as Wins
                FROM staff s
                JOIN staffroles sr ON s.firstName = sr.firstName
                JOIN employs e ON s.firstName = e.firstName
                JOIN oscarnominates o ON e.movieName = o.MovieName
                WHERE o.isWon = 1 AND s.DeathDate IS NULL
                GROUP BY s.firstName, s.lastName, sr.occupations
                ORDER BY Wins DESC;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.show_results("Dream Team", results)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching dream team: {e}")

    def show_top_companies(self):
        try:
            query = """
                SELECT pr.ProductionCompany, COUNT(*) AS Wins
                FROM produces pr
                JOIN oscarnominates o ON pr.Movie = o.MovieName
                WHERE o.isWon = 1
                GROUP BY pr.ProductionCompany
                ORDER BY Wins DESC
                LIMIT 5;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.show_results("Top Production Companies", results)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching top companies: {e}")

    def show_non_english_winners(self):
        try:
            query = """
                SELECT m.Movie, m.Language, m.ReleaseYear
                FROM movies m
                JOIN oscarnominates o ON m.Movie = o.MovieName
                WHERE o.isWon = 1 AND m.Language != 'English'
                GROUP BY m.Movie, m.Language, m.ReleaseYear;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.show_results("Non-English Winners", results)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching non-English winners: {e}")

    def show_results(self, title, results):
        # Create a new window for results
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("600x400")
        
        # Create Treeview
        tree = ttk.Treeview(result_window)
        tree["columns"] = tuple(range(len(results[0]))) if results else ()
        
        # Configure columns
        for i in range(len(tree["columns"])):
            tree.column(f"#{i}", width=100)
            tree.heading(f"#{i}", text=f"Column {i+1}")
        
        # Add data
        for row in results:
            tree.insert("", "end", values=row)
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

def main():
    root = tk.Tk()
    app = AcademyAwardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
