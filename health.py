import datetime
import time
from database_setup import connect_to_database, add_user_to_database, delete_user_from_database, search_user_from_database

def get_valid_input(prompt, input_type):
    while True:
        try:
            user_input = input(prompt)
            if input_type == "int":
                return int(user_input)
            elif input_type == "float":
                return float(user_input)
            elif input_type == "gender":
                if user_input.lower() in ["male", "female"]:
                    return user_input.lower()
                else:
                    raise ValueError("Invalid gender. Please enter 'male' or 'female'.")
            elif input_type == "activity":
                activity_factors = {1, 2, 3, 4, 5}
                user_input = int(user_input)
                if user_input in activity_factors:
                    return user_input
                else:
                    raise ValueError("Invalid activity level. Please choose from 1 to 5.")
            else:
                return user_input
        except ValueError as e:
            print("Invalid input:", e)


def calculate_maintenance_calories(weight_kg, height_cm, age, gender):
    try:
        if gender.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        elif gender.lower() == "female":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        else:
            raise ValueError("Invalid gender")
        
        activity_factors = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
        activity = get_valid_input("\nChoose from the activity levels:\n1. Sedentary (little or no exercise)\n2. Lightly active (light exercise/sports 1-3 days a week)\n3. Moderately active (moderate exercise/sports 3-5 days a week)\n4. Very active (hard exercise/sports 6-7 days a week)\n5. Extra active (very hard exercise/sports & physical job or 2x training)\nMake a choice: ", "activity")
        
        if activity not in activity_factors:
            raise ValueError("Invalid activity level")
        
        tdee = bmr * activity_factors[activity]
        return bmr, tdee
    except ValueError as ve:
        return None, str(ve)

def add_user():
    collection = connect_to_database()
    try:
        print("\n********************************************")
        print("WELCOME TO ADD USER FUNCTIONALITY")
        print("********************************************")
        username = input("Enter username:")
        weight_kg = get_valid_input("Enter weight in kilograms: ", "float")
        height_cm = get_valid_input("Enter height in centimeters: ", "float")
        age = get_valid_input("Enter age in years: ", "int")
        gender = get_valid_input("Enter gender (male/female): ", "gender")

        bmr, maintenance_calories = calculate_maintenance_calories(weight_kg, height_cm, age, gender)
        
        if bmr is None:
            print(maintenance_calories)
            return
        
        print("\nBasal Metabolic Rate (BMR):", bmr)
        print("Maintenance calories per day:", maintenance_calories)

        mild_weight_loss = maintenance_calories - (7700 * 0.25 / 7)
        moderate_weight_loss = maintenance_calories - (7700 * 0.5 / 7)
        extreme_weight_loss = maintenance_calories - (7700 * 1 / 7)

        target_weight = get_valid_input("\nEnter target weight in kilograms: ", "float")

        print("\nCalories consumed per day for:")
        print("1. Mild weight loss (0.25 kg/week):", mild_weight_loss)
        print("2. Moderate weight loss (0.5 kg/week):", moderate_weight_loss)
        print("3. Extreme weight loss (1 kg/week):", extreme_weight_loss)
        
        while True:
            try:
                strategy_choice = int(input("Enter your choice (1/2/3): "))
                if strategy_choice in [1, 2, 3]:
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a numeric choice.")

        if strategy_choice == 1:
            rate = 0.25
            strategy = "Mild"
            dailycal = mild_weight_loss
        elif strategy_choice == 2:
            rate = 0.5
            strategy = "Moderate"
            dailycal = moderate_weight_loss
        elif strategy_choice == 3:
            rate = 1.0
            strategy = "Extreme"
            dailycal = extreme_weight_loss

        weeks_to_goal = (weight_kg - target_weight) / rate
        days_to_goal = int(weeks_to_goal * 7)

        current_date = datetime.datetime.now().date()
        target_date = current_date + datetime.timedelta(days=days_to_goal)

        print(f"\nEstimated number of days to achieve the target weight goal: {days_to_goal:.2f} days")
        print(f"Target achieve date: {target_date}")
        time.sleep(2)

        user_data = {
            "username" : username,
            "current weight": weight_kg,
            "height": height_cm,
            "age": age,
            "gender": gender,
            "maintenance_calories": maintenance_calories,
            "BMR": bmr,
            "target weight": target_weight,
            "weight_loss_strategy": strategy,
            "days to achieve goal": days_to_goal,
            "target weight": target_weight,
            "calories per day": dailycal
        }
        add_user_to_database(collection, user_data)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user.")
    except ValueError as ve:
        print("Error:", ve)

def delete_user():
    collection = connect_to_database()
    try:
        print("\n********************************************")
        print("WELCOME TO DELETE USER FUNCTIONALITY")
        print("********************************************")
        deleteusername = input("Enter Username to delete: ")
        time.sleep(1)
        delete_user_from_database(collection, deleteusername)        
        print("\n")
    except Exception as e:
        print("Error:", e)

def lookup_user():
    collection = connect_to_database()
    try:
        print("\n********************************************")
        print("WELCOME TO SEARCH USER FUNCTIONALITY")
        print("********************************************")
        userfind = input("Enter username to search: ")
        time.sleep(1)
        user = search_user_from_database(collection, userfind)
        if user:
            print(f"HERE ARE THE DETAILS FOR USER {user[0]['username']}")
            print(f"weight = {user[0]['current weight']}")
            print(f"height = {user[0]['height']}")
            print(f"age = {user[0]['age']}")
            print(f"gender = {user[0]['gender']}")
            print(f"maintenance_calories = {user[0]['maintenance_calories']}")
            print(f"BMR = {user[0]['BMR']}")
            print(f"target weight = {user[0]['target weight']}")
            print(f"weight_loss_strategy = {user[0]['weight_loss_strategy']}")
            print(f"days to achieve goal = {user[0]['days to achieve goal']}")
            print("\n")
            time.sleep(2)
        else:
            print("User not found.")
            time.sleep(2)
        
    except Exception as e:
        print("Error:", e)

def update_user():
    collection = connect_to_database()
    print("\n********************************************")
    print("WELCOME TO UPDATE USER FUNCTIONALITY")
    print("********************************************")
    username = input("Enter username to update: ")
    user = search_user_from_database(collection, username)

    if not user:
        print("User not found.")
        return

    print(f"\nUser found. Current details for {user[0]['username']}:")
    print("LIST OF ITEMS THAT CAN BE UPDATED")
    print(f"1. Current weight: {user[0]['current weight']}")
    print(f"2. Height: {user[0]['height']}")
    print(f"3. Age: {user[0]['age']}")
    print(f"4. Gender: {user[0]['gender']}")
    print(f"5. Target weight: {user[0]['target weight']}")
    print("")

    choice = input("Enter what you want to update: ")

    if choice == "":
        print("No updates made.")
        return

    if choice == "1":
        new_weight = float(input("Enter new weight in kilograms: "))
        collection.update_one({"username": username}, {"$set": {"current weight": new_weight}})
        print("Weight updated successfully.")
    elif choice == "2":
        new_height = float(input("Enter new height in centimeters: "))
        collection.update_one({"username": username}, {"$set": {"height": new_height}})
        print("Height updated successfully.")
        calculate_maintenance_calories()
    elif choice == "3":
        new_age = int(input("Enter new age in years: "))
        collection.update_one({"username": username}, {"$set": {"age": new_age}})
        print("Age updated successfully.")
    elif choice == "4":
        new_gender = input("Enter new gender (male/female): ")
        collection.update_one({"username": username}, {"$set": {"gender": new_gender}})
        print("Gender updated successfully.")
    elif choice == "5":
        new_target_weight = float(input("Enter new target weight in kilograms: "))
        collection.update_one({"username": username}, {"$set": {"target weight": new_target_weight}})
        print("Target weight updated successfully.")
    else:
        print("Invalid choice.")


def main():
    try:
        while True:
            
            print("********************************************")
            print("WELCOME TO OUR HEALTH APP")
            print("********************************************")
            print("HERE IS A LIST OF FUNCTIONS:")
            print("1. Add User")
            print("2. Delete User")
            print("3. Update User")
            print("4. Lookup User")
            print("5. Terminate Process")
            choice = input("Enter your choice: ")

            if choice == "1":
                add_user()
            elif choice == "2":
                delete_user()
            elif choice == "3":
                update_user()
            elif choice == "4":
                lookup_user()
            elif choice=='5':
                print("THE PROCESS HAS BEEN TERMINATED")
                return
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()