from collections import UserDict
import re


class Field: # define class Field
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)


class Name(Field): # define class Name
    pass

class Phone(Field): # define class Phone
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. It should be 10 digits.")
        super().__init__(value)
    @staticmethod
    def is_valid_phone(phone):
        return re.fullmatch(r"\d{10}", phone) is not None

class Record: # define class Record
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone {phone} not found.")
    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                found = True
                break
        if not found:
            raise ValueError(f"Phone {old_phone} not found.")
        if not Phone.is_valid_phone(new_phone):
            raise ValueError("Invalid phone number format. It should be 10 digits.")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict): # define class AddressBook
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

def parse_input(user_input): # define function for parsing user`s input
    if not user_input.strip():
        return None, []  # Handle empty input
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except ValueError:
        return None, []  # Handle cases where split fails

def input_error(func): # define function for work with exceptions
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid command format."
        except TypeError:
            return "Invalid input type."
    return inner


@input_error
def add_contact(args, book): #define function for add contacts
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    if not Phone.is_valid_phone(phone):
        raise ValueError("Invalid phone number format. It should be 10 digits.")
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book): #define function for change contacts
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def get_contact(args, book): #define function for get contacts
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    return str(record)

@input_error
def delete_contact(args, book): #define function for delete contacts
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    book.delete(name)
    return f"Contact {name} deleted."

def all_contacts(book): # define function for print list of all contacts
    if not book.data:
        print("No contacts saved yet.")
    else:
        for record in book.data.values():
            print(record)

def main(): # Define main function
    book = AddressBook()
    print(
        "Welcome to the assistant bot!\nYou can use command hello, add, change, phone, all, delete or exit/close"
    )
    while True:
        user_input = input(f"Please input command:").strip()
        if not user_input:
            print("Please enter a command.")
            continue
        command, args = parse_input(user_input)
        if command is None:
            print("Invalid input format.")
            continue
        if command == "hello":
            print(
                "How can I help you?\n You can use command hello, add, change, phone, all, delete or exit/close"
            )
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "all":
            all_contacts(book)
        elif command == "delete":
            print(delete_contact(args, book))
        elif command in ["exit", "close"]:
            print(f"Goodbye!")
            break
        else:
            print("Command not found! Please try again")

if __name__ == "__main__":
    main()