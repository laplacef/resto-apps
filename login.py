import string
import random


class Employee:
    """An approximate representation of an employee."""

    def __init__(self, first_name: str, last_name: str) -> None:
        """Initialize employee attributes."""

        self.first_name = first_name.lower()
        self.last_name = last_name.lower()
        self.username = self.__update_username(self.first_name, self.last_name)
        self.__password = self.__get_random_password()
        self.__hourly_payrate = 12
        self.__timesheet = {
            "sunday": 0,
            "monday": 0,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
        }
        self.__welcome_employee(self.first_name, self.username, self.__password)

    def __welcome_employee(self, first_name: str, username: str, password: str) -> None:
        """Welcomes newly created employee."""

        print(f"Welcome {first_name.title()}! Your login info is below:")
        print(f"Username: {username}\nDefault password: {password}")

    def __update_username(self, new_first_name: str, new_last_name: str) -> str:
        """Returns updated employee username."""

        if len(new_last_name) >= 3:
            username = f"{new_first_name[0]}_{new_last_name[0:3]}"
        else:
            username = f"{new_first_name[0]}_{new_last_name[0:len(new_first_name)]}"

        return username

    def __get_random_password(self) -> str:
        """Returns randomly generated password that meets security criteria."""

        random_password = ""
        while not self.__validate_password_strength(random_password):
            random_password = random.choices(
                string.ascii_letters + string.digits, k=random.randint(8, 16)
            )

        return "".join(random_password)

    def __validate_current_password(self) -> bool:
        """Returns True if passed argument equals employee password."""

        current_password = input(f"Please enter current employee password: ")

        return current_password == self.__password

    def __validate_password_strength(self, password: str) -> bool:
        """Returns True if password meets minimum security criteria."""

        meets_criteria = set()
        if (len(password) >= 8 and len(password) <= 16) and (
            "length" not in meets_criteria
        ):
            meets_criteria.add("length")
        else:
            return False
        for char in password:
            if (char in string.ascii_uppercase) and ("upper" not in meets_criteria):
                meets_criteria.add("upper")
            elif (char in string.ascii_lowercase) and ("lower" not in meets_criteria):
                meets_criteria.add("lower")
            elif (char in string.digits) and ("digits" not in meets_criteria):
                meets_criteria.add("digits")
            else:
                continue
        if len(meets_criteria) == 4:
            return True
        else:
            return False

    def __get_day_worked(self) -> str:
        """Returns day worked based on user input."""

        days_index = {
            1: "monday",
            2: "tuesday",
            3: "wednesday",
            4: "thursday",
            5: "friday",
            6: "saturday",
            7: "sunday",
        }
        while True:
            try:
                day_worked = int(
                    input(f"Enter the number for the day to update time worked:")
                )
            except ValueError:
                print(f"Please select a number choice between 1 and 7.")
            else:
                if day_worked not in range(1, 8):
                    print(f"Please select a number choice between 1 and 7.")
                else:
                    return days_index[day_worked]

    def __get_time_worked(self) -> int:
        """Returns time worked in minuntes based on user input."""

        while True:
            try:
                time_worked = int(input(f"Enter time worked in minutes: "))
            except ValueError:
                print(f"Please enter a number between 0 and 1440 (max per day).")
            else:
                if time_worked not in range(0, 1441):
                    print(f"Please select a number between 0 and 1440 (max per day).")
                else:
                    return time_worked

    def __get_hourly_conversion(self, minutes) -> str:
        """Returns conversion from minutes to hours."""

        hours = int(minutes / 60)
        minutes = int(round(60 * ((minutes / 60) - (int(minutes / 60))), 0))
        if hours + minutes != 0:
            return f"{hours} hrs {minutes} min"
        else:
            return f"No hours reported."

    def __get_total_pay(self) -> float:
        """Returns total pay based on employee timesheet."""

        total_pay = 0
        for minutes in self.__timesheet.values():
            total_pay += minutes * (self.__hourly_payrate / 60)

        return round(total_pay, 2)

    def update_names(self) -> None:
        """Updates employee first and last names."""

        new_first_name = input(f"Please enter first name: ").lower()
        new_last_name = input(f"Please enter last name: ").lower()
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.username = self.__update_username(new_first_name, new_last_name)
        new_username = self.username
        print(
            f"Employee name was updated successfully. New username is: {new_username}"
        )

    def update_password(self) -> None:
        """Updates employee password."""

        while True:
            if self.__validate_current_password():
                print(
                    f"New password requirements:\n\t* Characters (8-16)\n\t* An uppercase letter\n\t* A lowercase letter\n\t* A number"
                )
                while True:
                    new_password = input(f"Please enter new password: ")
                    if self.__validate_password_strength(new_password):
                        self.__password = new_password
                        print(
                            f"Successfully updated password.\nNew password is: {new_password}"
                        )
                        break
                    else:
                        print(
                            f"Password does not meet security criteria, it must contain 8-16 characters, at least an uppercase letter, a lowercase letter, and a number."
                        )
                break
            else:
                print(
                    f"The password you entered does not match current password. Please Try again."
                )

    def update_timesheet(self) -> None:
        """Updates employee timesheet based on input."""

        print(
            f"Choose from list below:\n\t1 - Monday\n\t2 - Tuesday\n\t3 - Wednesday\n\t4 - Thursday\n\t5 - Friday\n\t6 - Saturday\n\t7 - Sunday"
        )
        ask_again = True
        while ask_again:
            day_worked = self.__get_day_worked()
            self.__timesheet[day_worked] = self.__get_time_worked()
            print(f"Successfully updated timesheet.")
            while True:
                add_another = input(f"Update another day? (Y or N): ")
                if add_another.lower() in ["yes", "y"]:
                    ask_again = True
                    break
                elif add_another.lower() in ["no", "n"]:
                    ask_again = False
                    break
                else:
                    print(f"Please enter yes or no (Y or N).")
                    continue

    def view_timesheet(self) -> None:
        """Print current timesheet to screen."""

        employee_name = f"{self.first_name} {self.last_name}"
        user_name = self.username
        print(f"{employee_name.upper()}'S TIMESHEET.\nUsername: {user_name}")
        print(f"-" * 50)
        for day, mins in self.__timesheet.items():
            print(f"{day.title()}: {self.__get_hourly_conversion(mins)}")
        print(f"-" * 50)
        print(f"TOTAL PAY: ${format(self.__get_total_pay(),'.2f')}")

    def clear_timesheet(self) -> None:
        """Reset employee timesheet to 0."""

        for key in self.__timesheet:
            self.__timesheet[key] = 0
        print(f"Successfully reset timesheet.")


def main() -> None:
    """Runs employee portal app."""

    employee_database = {}
    print(
        f"Select an option:\n\t0 - View all choices\n\t1 - Add new employee\n\t2 - Update employee name\n\t3 - Update employee password\n\t4 - Update employee timesheet\n\t5 - View employee timesheet\n\t6 - Clear employee timesheet\n\t7 - View all usernames\n\t8 - Exit program"
    )
    while True:
        try:
            user_choice = int(input(f"Enter number (0 to view choices): "))
        except ValueError:
            print(f"Please enter a choice from the list (0 - 8)")
        else:
            if user_choice not in range(0, 9):
                print(f"Please enter a choice from the list (0 - 8)")
                continue
            elif user_choice == 0:
                print(
                    f"Select an option:\n\t0 - View all choices\n\t1 - Add new employee\n\t2 - Update employee name\n\t3 - Update employee password\n\t4 - Update employee timesheet\n\t5 - View employee timesheet\n\t6 - Clear employee timesheet\n\t7 - View all usernames\n\t8 - Exit program"
                )
            elif user_choice == 1:
                first_name = input("Enter new employee's first name: ")
                last_name = input("Enter new employee's last name: ")
                new_user = Employee(first_name, last_name)
                employee_database[new_user.username] = new_user
            elif user_choice == 2:
                employee_username = input(f"Enter employee username")
                try:
                    employee_database[employee_username]
                except KeyError:
                    print(f"That user does not exist.")
                else:
                    # TODO: Review this part so that a change in names updates employee database key for that employee
                    emp_id = id(employee_database[employee_username])
                    employee_database[employee_username].update_names()
                    for k, v in employee_database.items():
                        if id(v) == emp_id:
                            employee_database[k] = employee_database[
                                employee_username
                            ].username
            elif user_choice == 3:
                employee_username = input(f"Enter employee username")
                try:
                    employee_database[employee_username]
                except KeyError:
                    print(f"That user does not exist.")
                else:
                    employee_database[employee_username].update_password()
            elif user_choice == 4:
                employee_username = input(f"Enter employee username")
                try:
                    employee_database[employee_username]
                except KeyError:
                    print(f"That user does not exist.")
                else:
                    employee_database[employee_username].update_timesheet()
            elif user_choice == 5:
                employee_username = input(f"Enter employee username")
                try:
                    employee_database[employee_username]
                except KeyError:
                    print(f"That user does not exist.")
                else:
                    employee_database[employee_username].view_timesheet()
            elif user_choice == 6:
                employee_username = input(f"Enter employee username")
                try:
                    employee_database[employee_username]
                except KeyError:
                    print(f"That user does not exist.")
                else:
                    employee_database[employee_username].clear_timesheet()
            elif user_choice == 7:
                employee_username = input(f"Enter employee username")
                emp_list = [key for key in employee_database.keys()]
                if emp_list:
                    print(emp_list)
                else:
                    print(
                        f"No employees in database. Choose option 1 to add a new employee."
                    )
            else:
                break


if __name__ == "__main__":
    main()
