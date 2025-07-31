"""
STUDENT GRADEBOOK MANAGER
A menu-driven CLI to manage student grades, averages, and statistics.
"""
import ast
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "list_of_grades.py")

def load_gradebook():
    try:
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("{"):
                    return ast.literal_eval(line.strip())
    except Exception:
import ast
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "list_of_grades.py")

# New format: each line is 'name,[grades]'
def load_gradebook():
    gradebook = {}
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ',' in line:
                    name, grades_str = line.split(',', 1)
                    try:
                        grades = ast.literal_eval(grades_str)
                        if isinstance(grades, list):
                            gradebook[name] = grades
                    except Exception:
                        gradebook[name] = []
    except Exception:
        pass
    return gradebook

def save_gradebook(gradebook):
    with open(DATA_FILE, "w") as f:
        f.write("# Student gradebook data: each line is 'name,[grades]'\n")
        for name, grades in gradebook.items():
            f.write(f"{name},{grades}\n")
    if not gradebook:
        print("No students in gradebook.")
        return
    averages = {name: sum(grades)/len(grades) if grades else 0 for name, grades in gradebook.items()}
    class_avg = sum(averages.values()) / len(averages)
    highest = max(averages, key=averages.get)
    lowest = min(averages, key=averages.get)
    print(f"\nClass Average: {class_avg:.2f}")
    print(f"Highest: {highest} ({averages[highest]:.2f})")
    print(f"Lowest: {lowest} ({averages[lowest]:.2f})\n")

def view_student_report(gradebook):
    name = input("Enter student name: ").strip()
    if name not in gradebook:
        print(f"Student '{name}' not found.")
        return
    grades = gradebook[name]
    if grades:
        avg = sum(grades) / len(grades)
        letter = get_letter_grade(avg)
        print(f"Enter student name: {name}")
        print(f"{name}'s Average: {avg:.2f} (Grade: {letter})")
        print(f"Grades: {grades}")
    else:
        print(f"No grades for {name}.")

def add_student(gradebook):
    name = input("Enter new student name: ").strip()
    if name in gradebook:
        print("Student already exists.")
    else:
        gradebook[name] = []
        save_gradebook(gradebook)
        print(f"Added student '{name}'.")

def add_grade(gradebook):
    name = input("Enter student name: ").strip()
    if name not in gradebook:
        print(f"Student '{name}' not found.")
        return
    try:
        grade = float(input("Enter grade (0-100): "))
        if 0 <= grade <= 100:
            gradebook[name].append(grade)
            save_gradebook(gradebook)
            print(f"Added grade {grade} for {name}.")
        else:
            print("Grade must be between 0 and 100.")
    except ValueError:
        print("Invalid grade input.")

def main():
    gradebook = load_gradebook()
    while True:
        print("\n=== STUDENT GRADEBOOK MANAGER ===")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. View Student Report")
        print("4. Class Statistics")
        print("5. Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            add_student(gradebook)
        elif choice == '2':
            add_grade(gradebook)
        elif choice == '3':
            view_student_report(gradebook)
        elif choice == '4':
            class_statistics(gradebook)
        elif choice == '5':
            print("Exiting Gradebook Manager. thanks !")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
