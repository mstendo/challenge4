# student_fee_system.py
import json
import os

# Store our data
students = []
fees = []
payments = []

# Login function
def login():
    print("\nAdmin Login")
    user = input("Username: ")
    pwd = input("Password: ")
    
    if user == "admin" and pwd == "admin123":
        print("Login ok!")
        return True
    else:
        print("Wrong login")
        return False

# Student functions
def add_student():
    print("\nAdd Student")
    
    # Get student ID
    while True:
        id = input("Student ID: ")
        if not id:
            print("Need ID")
            continue
            
        # Check if ID exists
        found = False
        for s in students:
            if s["id"] == id:
                found = True
                break
                
        if found:
            print("ID taken, try another")
        else:
            break
    
    name = input("Name: ")
    if not name:
        print("Need name")
        return
        
    program = input("Program: ")
    campus = input("Campus: ")
    
    # Get year
    while True:
        yr = input("Year (1-5): ")
        if yr in ['1','2','3','4','5']:
            year = int(yr)
            break
        else:
            print("Enter 1-5")
    
    # Add student
    student = {
        "id": id,
        "name": name,
        "program": program,
        "campus": campus,
        "year": year
    }
    students.append(student)
    print(f"Added {name}")

def show_students():
    print("\nAll Students")
    if not students:
        print("No students")
        return
        
    for i, s in enumerate(students, 1):
        paid, bal, stat = get_balance(s["id"])
        print(f"{i}. {s['name']} ({s['id']}) - {s['program']} - Balance: {bal:,} - {stat}")

def update_student():
    show_students()
    if not students:
        return
        
    try:
        num = int(input("Student number to edit: ")) - 1
        if num < 0 or num >= len(students):
            print("Bad number")
            return
            
        s = students[num]
        print(f"Editing {s['name']}")
        
        new_name = input(f"New name [{s['name']}]: ") or s['name']
        new_prog = input(f"New program [{s['program']}]: ") or s['program']
        new_camp = input(f"New campus [{s['campus']}]: ") or s['campus']
        
        s['name'] = new_name
        s['program'] = new_prog
        s['campus'] = new_camp
        
        print("Updated!")
        
    except:
        print("Enter a number")

def remove_student():
    show_students()
    if not students:
        return
        
    try:
        num = int(input("Student number to delete: ")) - 1
        if num < 0 or num >= len(students):
            print("Bad number")
            return
            
        s = students[num]
        sure = input(f"Delete {s['name']}? (y/n): ")
        if sure == 'y':
            students.pop(num)
            print("Deleted")
        else:
            print("Cancelled")
            
    except:
        print("Enter a number")

# Fee functions
def add_fee():
    print("\nAdd Fee")
    program = input("Program: ")
    
    while True:
        yr = input("Year (1-5): ")
        if yr in ['1','2','3','4','5']:
            year = int(yr)
            break
        else:
            print("Enter 1-5")
    
    while True:
        try:
            amount = float(input("Fee amount: "))
            if amount > 0:
                break
            else:
                print("Must be positive")
        except:
            print("Enter number")
    
    fee = {
        "program": program,
        "year": year,
        "amount": amount
    }
    fees.append(fee)
    print("Fee added")

def show_fees():
    print("\nFee List")
    if not fees:
        print("No fees")
        return
        
    for f in fees:
        print(f"{f['program']} Year {f['year']}: {f['amount']:,}")

# Payment functions
def get_student_fee(student_id):
    # Find student first
    for s in students:
        if s["id"] == student_id:
            # Find matching fee
            for f in fees:
                if f["program"] == s["program"] and f["year"] == s["year"]:
                    return f["amount"]
            return 0
    return 0

def get_balance(student_id):
    total_paid = 0
    for p in payments:
        if p["student_id"] == student_id:
            total_paid += p["amount"]
            
    student_fee = get_student_fee(student_id)
    balance = student_fee - total_paid
    status = "Cleared" if balance <= 0 else "Not Cleared"
    
    return total_paid, balance, status

def add_payment():
    print("\nRecord Payment")
    if not students:
        print("No students")
        return
        
    show_students()
    
    try:
        num = int(input("Student number: ")) - 1
        if num < 0 or num >= len(students):
            print("Bad number")
            return
            
        s = students[num]
        paid, bal, stat = get_balance(s["id"])
        fee = get_student_fee(s["id"])
        
        print(f"\n{s['name']} - Fee: {fee:,} - Paid: {paid:,} - Balance: {bal:,}")
        
        # Get payment amount
        while True:
            try:
                amt = float(input("Payment amount: "))
                if amt <= 0:
                    print("Must be positive")
                    continue
                if amt > bal:
                    print(f"Too much! Balance is {bal:,}")
                    continue
                break
            except:
                print("Enter number")
        
        # Add payment
        payment = {
            "student_id": s["id"],
            "amount": amt,
            "date": input("Date (YYYY-MM-DD) [today]: ") or "2024-01-01"
        }
        payments.append(payment)
        
        # Show new balance
        new_paid, new_bal, new_stat = get_balance(s["id"])
        print(f"New balance: {new_bal:,} - {new_stat}")
        
    except:
        print("Enter number")

def show_payments():
    print("\nPayment History")
    if not payments:
        print("No payments")
        return
        
    for p in payments:
        # Find student name
        name = "Unknown"
        for s in students:
            if s["id"] == p["student_id"]:
                name = s["name"]
                break
        print(f"{name} - {p['amount']:,} - {p['date']}")

# Reports
def student_report():
    print("\nStudent Report")
    if not students:
        print("No students")
        return
        
    for s in students:
        paid, bal, stat = get_balance(s["id"])
        fee = get_student_fee(s["id"])
        print(f"{s['name']} - {s['program']} - Fee: {fee:,} - Paid: {paid:,} - Balance: {bal:,} - {stat}")

def program_report():
    print("\nProgram Report")
    if not fees:
        print("No fees set")
        return
        
    total_expected = 0
    total_collected = 0
    
    for f in fees:
        # Count students in this program/year
        count = 0
        collected = 0
        
        for s in students:
            if s["program"] == f["program"] and s["year"] == f["year"]:
                count += 1
                paid, _, _ = get_balance(s["id"])
                collected += paid
                
        expected = count * f["amount"]
        total_expected += expected
        total_collected += collected
        
        print(f"\n{f['program']} Year {f['year']}:")
        print(f"Students: {count}")
        print(f"Expected: {expected:,}")
        print(f"Collected: {collected:,}")
        print(f"Outstanding: {expected - collected:,}")
    
    print(f"\nTOTALS:")
    print(f"Expected: {total_expected:,}")
    print(f"Collected: {total_collected:,}")
    print(f"Outstanding: {total_expected - total_collected:,}")

def search_students():
    print("\nSearch Students")
    print("1. By Program")
    print("2. By Status")
    
    choice = input("Choice: ")
    
    if choice == "1":
        program = input("Program: ")
        found = []
        for s in students:
            if s["program"] == program:
                found.append(s)
                
        if found:
            print(f"\nFound {len(found)} students:")
            for s in found:
                paid, bal, stat = get_balance(s["id"])
                print(f"{s['name']} - Balance: {bal:,} - {stat}")
        else:
            print("None found")
            
    elif choice == "2":
        status = input("Status (Cleared/Not Cleared): ")
        found = []
        for s in students:
            _, _, stat = get_balance(s["id"])
            if stat == status:
                found.append(s)
                
        if found:
            print(f"\nFound {len(found)} students:")
            for s in found:
                print(f"{s['name']} - {s['program']}")
        else:
            print("None found")

# File operations
def save_all():
    try:
        with open('students.json', 'w') as f:
            json.dump(students, f)
        with open('fees.json', 'w') as f:
            json.dump(fees, f)
        with open('payments.json', 'w') as f:
            json.dump(payments, f)
        print("Saved!")
    except:
        print("Save error")

def load_all():
    global students, fees, payments
    try:
        if os.path.exists('students.json'):
            with open('students.json', 'r') as f:
                students = json.load(f)
        if os.path.exists('fees.json'):
            with open('fees.json', 'r') as f:
                fees = json.load(f)
        if os.path.exists('payments.json'):
            with open('payments.json', 'r') as f:
                payments = json.load(f)
        print("Loaded data")
    except:
        print("No saved data")

# Menus
def student_menu():
    while True:
        print("\nStudent Menu")
        print("1. Add Student")
        print("2. View Students")
        print("3. Edit Student")
        print("4. Delete Student")
        print("5. Back")
        
        choice = input("Choose: ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            remove_student()
        elif choice == "5":
            break
        else:
            print("Pick 1-5")

def fee_menu():
    while True:
        print("\nFee Menu")
        print("1. Add Fee")
        print("2. View Fees")
        print("3. Back")
        
        choice = input("Choose: ")
        
        if choice == "1":
            add_fee()
        elif choice == "2":
            show_fees()
        elif choice == "3":
            break
        else:
            print("Pick 1-3")

def payment_menu():
    while True:
        print("\nPayment Menu")
        print("1. Record Payment")
        print("2. View Payments")
        print("3. Back")
        
        choice = input("Choose: ")
        
        if choice == "1":
            add_payment()
        elif choice == "2":
            show_payments()
        elif choice == "3":
            break
        else:
            print("Pick 1-3")

def report_menu():
    while True:
        print("\nReports")
        print("1. Student Report")
        print("2. Program Report")
        print("3. Search")
        print("4. Back")
        
        choice = input("Choose: ")
        
        if choice == "1":
            student_report()
        elif choice == "2":
            program_report()
        elif choice == "3":
            search_students()
        elif choice == "4":
            break
        else:
            print("Pick 1-4")

# Main program
def main():
    load_all()
    
    while True:
        print("\n" + "="*40)
        print("STUDENT FEE SYSTEM")
        print("="*40)
        print("1. Students")
        print("2. Fees")
        print("3. Payments")
        print("4. Reports")
        print("5. Save")
        print("6. Exit")
        
        choice = input("\nChoose: ")
        
        if choice == "1":
            student_menu()
        elif choice == "2":
            fee_menu()
        elif choice == "3":
            payment_menu()
        elif choice == "4":
            report_menu()
        elif choice == "5":
            save_all()
        elif choice == "6":
            save_all()
            print("\nBye!")
            break
        else:
            print("Pick 1-6")

if __name__ == "__main__":
    print("Student Fee System")
    use_login = input("Login? (y/n): ")
    if use_login == 'y':
        if login():
            main()
    else:
        main()