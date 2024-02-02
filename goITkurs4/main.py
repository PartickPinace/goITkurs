from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Niepoprawny numer telefonu")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None

class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Niepoprawny adres email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None

class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.emails = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        self.emails.append(email)

    def remove_email(self, email: Email):
        self.emails.remove(email)
        print(f"Usunięto email.")

    def edit_email(self, old_email: Email, new_email: Email):
        self.remove_email(old_email)
        self.add_email(new_email)
        print(f"Zmieniono email na: {new_email}.")

    def edit_name(self, new_name: Name):
        self.name = new_name
        print(f"Zmieniono imię na: {new_name}.")

    def __str__(self):
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        return f"Imię i nazwisko: {self.name.value},\nTelefony: {phones},\nEmail: {emails}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        print(f"Dodano wpis.")

    def find_record(self, search_term):
        found_records = []
        for record in self.data.values():
            if search_term.lower() == record.name.value.lower():
                found_records.append(record)
                continue

            for phone in record.phones:
                if search_term == phone.value:
                    found_records.append(record)
                    break

            for email in record.emails:
                if search_term == email.value:
                    found_records.append(record)
                    break

        return found_records

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Usunięto wpis: {name}.")
        else:
            print(f"Wpis o nazwie {name} nie istnieje.")


def input_phone():
    while True:
        try:
            number = input("Podaj numer telefonu w formacie '123456789' (naciśnij Enter, aby pominąć): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)

def input_email():
    while True:
        try:
            address = input("Podaj adres email (naciśnij Enter, aby pominąć): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)

def create_record():
    while True:
        name_input = input("Podaj imię i nazwisko: ")
        if name_input.strip():
            name = Name(name_input)
            break
        else:
            print("Pole imię i nazwisko jest wymagane.")

    record = Record(name)

    while True:
        phone = input_phone()
        if phone:
            record.add_phone(phone)
            decision = input("Dodać kolejny numer? (tak/nie) ").lower()
            if decision not in ["tak", "t"]:
                break
        else:
            break

    while True:
        email = input_email()
        if email:
            record.add_email(email)
            decision = input("Dodać kolejny email? (tak/nie) ").lower()
            if decision not in ["tak", "t"]:
                break
        else:
            break

    return record


def main():
    book = AddressBook()
    while True:
        action = input("Wybierz akcję: dodaj (d), znajdź (z), usuń (u), koniec (q): ")
        if action == "dodaj" or action == "d":
            record = create_record()
            book.add_record(record)
        elif action == 'znajdź' or action == "z":
            search = input("Wpisz szukaną frazę: ")
            found = book.find_record(search)
            for record in found:
                print(record)
        elif action == 'usuń'or action == "u":
            name = input("Podaj imię i nazwisko do usunięcia: ")
            book.delete_record(name)
        elif action == 'koniec'or action == "q":
            break

if __name__ == "__main__":
    main()
