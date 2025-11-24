import sqlite3


def main():
    # Connect to the database
    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()

    while True:
        user_input = input("Enter person ID (-1 to exit): ")

        try:
            person_id = int(user_input)
        except ValueError:
            print("Please enter a valid number.\n")
            continue

        if person_id == -1:
            print("Goodbye!")
            break

        cursor.execute("""
            SELECT first_name, last_name, age 
            FROM person 
            WHERE id = ?;
        """, (person_id,))

        person = cursor.fetchone()

        if person is None:
            print("Person not found. Try again.\n")
            continue

        first_name, last_name, age = person
        print(f"\n{first_name} {last_name}, {age} years old")

        # Look up the person's pets
        cursor.execute("""
            SELECT pet.name, pet.breed, pet.age, pet.dead
            FROM pet
            JOIN person_pet ON pet.id = person_pet.pet_id
            WHERE person_pet.person_id = ?;
        """, (person_id,))

        pets = cursor.fetchall()

        if pets:
            for pet in pets:
                name, breed, pet_age, dead = pet
                status = "who is deceased" if dead == 1 else "who is still alive"
                print(f" - Owned {name}, a {breed}, {pet_age} years old, {status}.")
        else:
            print("This person does not own any pets.")

        print()

    conn.close()


if __name__ == "__main__":
    main()

