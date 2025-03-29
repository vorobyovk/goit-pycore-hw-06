
def parse_input(user_input):
    if not user_input.strip():
        return None, []  # Handle empty input
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except ValueError:
        return None, [] # Handle cases where split fails


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
        except TypeError:
            return "Invalid input type."
    return inner


@input_error
def add_contact(args, CONTACTS):
    if len(args) > 2:
        raise ValueError
    elif len(args) == 2:
        name, phone = args
    elif len(args) == 1:
            name = args[0]
            phone = input("Please input phone: ").strip().lower()
    else:
        raise ValueError
    if not name or not phone:
        raise ValueError
    if not phone.isdigit():
        raise ValueError    
    print(f"Added Name: {name}, Phone: {phone}")
    CONTACTS[name] = phone
    return "Contact added."


@input_error
def change_contact(args, CONTACTS):
    if len(args) > 2:
        raise ValueError
    if len(args) == 2:
        name, phone = args
    else:
        if len(args) == 1:
            name = args[0]
            phone = input("Please input phone: ").strip().lower()
        else:
            name = input("Please input name: ").strip().lower()
            phone = input("Please input phone: ").strip().lower()
    if not name or not phone:
        raise ValueError
    if not phone.isdigit():
        raise ValueError
    if name in CONTACTS:
        CONTACTS[name] = phone
        return "Contact updated."
    else:
        raise KeyError


@input_error
def get_contact(args, CONTACTS):
    if len(args) == 1:
        name = args[0]
    else:
        name = input("Please input name: ").strip().lower()
    if not name:
        raise ValueError
    if name in CONTACTS:
        return f"Phone: {CONTACTS[name]}"
    else:
        raise KeyError


def all_contacts(CONTACTS):
    if not CONTACTS:
        print("No contacts saved yet.")
    else:
        for name, phone in CONTACTS.items():
            print(f"{name}: {phone}")


def main():
    CONTACTS = {}
    print("Welcome to the assistant bot!\nYou can use command hello, add, change, phone, all or exit/close")
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
            print("How can I help you?\n You can use command hello, add, change, phone, all or exit/close")
        elif command == "add":
            print(add_contact(args, CONTACTS))
        elif command == "change":
            print(change_contact(args, CONTACTS))
        elif command == "phone":
            print(get_contact(args, CONTACTS))
        elif command == "all":
            all_contacts(CONTACTS)
        elif command in ["exit", "close"]:
            print(f"Goodbye!")
            break
        else:
            print("Command not found! Please try again")


if __name__ == "__main__":
    main()