def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Nie znaleziono użytkownika."
        except ValueError:
            return "Nieprawidłowe dane wejściowe."
        except IndexError:
            return "Wprowadź nazwę użytkownika i numer telefonu."
    return inner

contacts = {}

def add_contact(args):
    name, phone = args.split()
    contacts[name] = phone
    return f"Dodano kontakt: {name}, numer: {phone}"

def change_contact(args):
    name, phone = args.split()
    if name in contacts:
        contacts[name] = phone
        return f"Zmieniono numer dla {name} na {phone}"
    return "Nie znaleziono takiego kontaktu."

def phone_contact(args):
    return contacts.get(args, "Nie znaleziono takiego kontaktu.")

def show_all(args):
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

@input_error
def handle_command(command, args):
    if command == "add":
        return add_contact(args)
    elif command == "zmień" or command == "zmien":
        return change_contact(args)
    elif command == "phone":
        return phone_contact(args)
    elif command == "show" and args == "all":
        return show_all(args)
    elif command == "hello":
        return "How can I help you?"
    else:
        return "Nie rozpoznano polecenia."


def main():
    while True:
        user_input = input(">> ").lower()
        if user_input in ["good bye", "close", "exit", "."]:
            print("Good bye!")
            break
        if user_input:

            parts = user_input.split()
            command = parts[0]
            args = " ".join(parts[1:])
            print(handle_command(command, args))

if __name__ == "__main__":
    main()
