# ==========================================================
# STUDENT PERFORMANCE ANALYTICS SYSTEM
# Python + NumPy + Pandas + Matplotlib + Seaborn
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
import time

# ==========================================================
# GLOBAL CONFIG
# ==========================================================

DATA_FILE = "students_data.csv"
students = []

sns.set()  # seaborn style

# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def line():
    print("=" * 60)

# ==========================================================
# DATA GENERATION
# ==========================================================


def generate_dummy_students(n=50):
    names = [
        "Ali", "Ahmed", "Sara", "Ayesha", "Hassan", "Zain",
        "Umar", "Fatima", "Hina", "Bilal", "Usman", "Noor"
    ]

    data = []

    for i in range(n):
        student = {
            "ID": f"S{i+1:03}",
            "Name": random.choice(names),
            "Age": random.randint(18, 25),
            "Math": random.randint(40, 100),
            "Physics": random.randint(40, 100),
            "Chemistry": random.randint(40, 100),
            "English": random.randint(40, 100)
        }
        data.append(student)

    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)
    print("Dummy student data generated.")

# ==========================================================
# DATA LOADING
# ==========================================================


def load_data():
    if not os.path.exists(DATA_FILE):
        generate_dummy_students()

    df = pd.read_csv(DATA_FILE)
    return df

# ==========================================================
# DATA PROCESSING
# ==========================================================


def add_calculated_columns(df):
    marks = ["Math", "Physics", "Chemistry", "English"]

    df["Total"] = df[marks].sum(axis=1)
    df["Average"] = df[marks].mean(axis=1)

    conditions = [
        df["Average"] >= 85,
        df["Average"] >= 70,
        df["Average"] >= 50
    ]

    grades = ["A", "B", "C"]

    df["Grade"] = np.select(conditions, grades, default="F")
    return df

# ==========================================================
# STUDENT CRUD
# ==========================================================


def add_student(df):
    clear()
    line()
    print("ADD NEW STUDENT")
    line()

    sid = f"S{len(df)+1:03}"
    name = input("Name: ")
    age = int(input("Age: "))

    marks = {}
    for sub in ["Math", "Physics", "Chemistry", "English"]:
        marks[sub] = int(input(f"{sub} marks: "))

    new_row = {
        "ID": sid,
        "Name": name,
        "Age": age,
        **marks
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    print("Student added successfully.")
    pause()
    return df


def delete_student(df):
    clear()
    sid = input("Enter Student ID to delete: ")
    df = df[df["ID"] != sid]
    df.to_csv(DATA_FILE, index=False)
    print("Student deleted.")
    pause()
    return df

# ==========================================================
# ANALYTICS FUNCTIONS
# ==========================================================


def show_summary(df):
    clear()
    line()
    print("DATA SUMMARY")
    line()
    print(df.describe())
    pause()


def top_students(df, n=5):
    clear()
    top = df.sort_values("Average", ascending=False).head(n)
    print(top[["ID", "Name", "Average", "Grade"]])
    pause()


def subject_statistics(df):
    clear()
    subjects = ["Math", "Physics", "Chemistry", "English"]

    for sub in subjects:
        print(f"\n{sub}")
        print("Mean:", df[sub].mean())
        print("Max:", df[sub].max())
        print("Min:", df[sub].min())

    pause()

# ==========================================================
# VISUALIZATION
# ==========================================================


def plot_average_distribution(df):
    clear()
    plt.figure()
    sns.histplot(df["Average"], bins=10)
    plt.title("Average Marks Distribution")
    plt.show()


def plot_subject_means(df):
    clear()
    subjects = ["Math", "Physics", "Chemistry", "English"]
    means = df[subjects].mean()

    plt.figure()
    means.plot(kind="bar")
    plt.title("Average Marks per Subject")
    plt.show()


def plot_grade_count(df):
    clear()
    plt.figure()
    sns.countplot(x="Grade", data=df)
    plt.title("Grade Distribution")
    plt.show()


def plot_heatmap(df):
    clear()
    plt.figure()
    sns.heatmap(
        df[["Math", "Physics", "Chemistry", "English"]].corr(), annot=True)
    plt.title("Subject Correlation Heatmap")
    plt.show()

# ==========================================================
# ADVANCED ANALYSIS
# ==========================================================


def numpy_analysis(df):
    clear()
    arr = df[["Math", "Physics", "Chemistry", "English"]].values

    print("NumPy Analysis")
    line()
    print("Overall Mean:", np.mean(arr))
    print("Overall Std Dev:", np.std(arr))
    print("Highest Mark:", np.max(arr))
    print("Lowest Mark:", np.min(arr))
    pause()

# ==========================================================
# MENU SYSTEM
# ==========================================================


def analytics_menu(df):
    while True:
        clear()
        line()
        print("ANALYTICS MENU")
        line()
        print("1. Data Summary")
        print("2. Top Students")
        print("3. Subject Statistics")
        print("4. NumPy Analysis")
        print("0. Back")

        ch = input("Choice: ")

        if ch == "1":
            show_summary(df)
        elif ch == "2":
            top_students(df)
        elif ch == "3":
            subject_statistics(df)
        elif ch == "4":
            numpy_analysis(df)
        elif ch == "0":
            break


def visualization_menu(df):
    while True:
        clear()
        line()
        print("VISUALIZATION MENU")
        line()
        print("1. Average Distribution")
        print("2. Subject Mean Bar Chart")
        print("3. Grade Count")
        print("4. Heatmap")
        print("0. Back")

        ch = input("Choice: ")

        if ch == "1":
            plot_average_distribution(df)
        elif ch == "2":
            plot_subject_means(df)
        elif ch == "3":
            plot_grade_count(df)
        elif ch == "4":
            plot_heatmap(df)
        elif ch == "0":
            break

# ==========================================================
# MAIN PROGRAM
# ==========================================================


def main():
    df = load_data()
    df = add_calculated_columns(df)

    while True:
        clear()
        line()
        print("STUDENT PERFORMANCE ANALYTICS SYSTEM")
        line()
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Analytics")
        print("4. Visualization")
        print("5. Reload Data")
        print("0. Exit")

        choice = input("Choice: ")

        if choice == "1":
            df = add_student(df)
            df = add_calculated_columns(df)
        elif choice == "2":
            df = delete_student(df)
            df = add_calculated_columns(df)
        elif choice == "3":
            analytics_menu(df)
        elif choice == "4":
            visualization_menu(df)
        elif choice == "5":
            df = load_data()
            df = add_calculated_columns(df)
        elif choice == "0":
            print("Exiting...")
            time.sleep(1)
            break


if __name__ == "__main__":
    main()
