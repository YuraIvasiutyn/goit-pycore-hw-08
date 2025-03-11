from abc import ABC, abstractmethod
import pickle
from controller import AddressBook, Record


class UserView(ABC):
    """Абстрактний клас для представлення користувацького інтерфейсу."""

    @abstractmethod
    def display_message(self, message: str):
        pass

    @abstractmethod
    def get_user_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def display_contacts(self, book: AddressBook):
        pass

    @abstractmethod
    def display_birthdays(self, birthdays):
        pass


class ConsoleView(UserView):
    """Консольна реалізація інтерфейсу."""

    def display_message(self, message: str):
        print(message)

    def get_user_input(self, prompt: str) -> str:
        return input(prompt).strip()

    def display_contacts(self, book: AddressBook):
        print(book if book.data else "No contacts found.")

    def display_birthdays(self, birthdays):
        if birthdays:
            for entry in birthdays:
                print(f"{entry['name']}: {entry['congratulation_date']}")
        else:
            print("No upcoming birthdays.")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please try again."
        except IndexError:
            return "Incomplete command. Please try again."

    return inner


@input_error
def add_contact(args, book: AddressBook, view: UserView):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    if phone:
        record.add_phone(phone)

    view.display_message(message)


@input_error
def change_contact(args, book: AddressBook, view: UserView):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        view.display_message("Contact not found.")
        return
    record.edit_phone(old_phone, new_phone)
    view.display_message("Contact updated.")


@input_error
def find_phone(args, book: AddressBook, view: UserView):
    name, *_ = args
    record = book.find(name)
    if record is None:
        view.display_message("Contact not found.")
        return
    phones = "; ".join(p.value for p in record.phones)
    view.display_message(f"Phone number(s) for {name}: {phones}")


@input_error
def add_birthday(args, book: AddressBook, view: UserView):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        view.display_message("Contact not found.")
        return
    record.add_birthday(birthday)
    view.display_message("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook, view: UserView):
    name, *_ = args
    record = book.find(name)
    if record is None:
        view.display_message("Contact not found.")
        return
    view.display_message(
        f"{record.name.value}'s birthday is on {record.birthday.value}" if record.birthday else "Birthday not set.")


def main():
    book = load_data()
    view = ConsoleView()
    view.display_message("Welcome to the assistant bot!")

    while True:
        user_input = view.get_user_input("Enter a command: ")
        command, *args = user_input.split()
        command = command.lower()

        if command in ["close", "exit"]:
            save_data(book)
            view.display_message("Good bye!")
            break
        elif command == "hello":
            view.display_message("How can I help you?")
        elif command == "add":
            add_contact(args, book, view)
        elif command == "change":
            change_contact(args, book, view)
        elif command == "phone":
            find_phone(args, book, view)
        elif command == "all":
            view.display_contacts(book)
        elif command == "add-birthday":
            add_birthday(args, book, view)
        elif command == "show-birthday":
            show_birthday(args, book, view)
        elif command == "birthdays":
            view.display_birthdays(book.get_upcoming_birthdays())
        else:
            view.display_message("Invalid command")

        save_data(book)


if __name__ == "__main__":
    main()
