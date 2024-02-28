from collections import UserDict
import re

class Field:
    """Klasa bazowa dla pól wpisu."""
    def __init__(self, value):
        self.value = value

class Name(Field):
    """Klasa imienia i nazwiska."""
    pass

class Phone(Field):
    """Klasa numeru telefonu z walidacją."""
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Niepoprawny numer telefonu")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        """Sprawdza, czy numer telefonu jest prawidłowy (9 cyfr, format 123456789)."""
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None

class Email(Field):
    """Klasa adresu email z walidacją."""
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Niepoprawny adres email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        """Sprawdza, czy email jest prawidłowy."""
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None

class Record:
    """Klasa wpisu w książce adresowej."""
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.emails = []

    def add_phone(self, phone: Phone):
        """Dodaje numer telefonu."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Usuwa numer telefonu."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Zmienia numer telefonu."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Dodaje adres email."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Usuwa adres email."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Zmienia adres email."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def edit_name(self, new_name: Name):
        """Zmienia imię i nazwisko."""
        self.name = new_name

    def __str__(self):
        """Zwraca string wpisu."""
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        return f"Imię i nazwisko: {self.name.value}, Telefony: {phones}, Email: {emails}"

class AddressBook(UserDict):
    """Klasa książki adresowej."""
    def add_record(self, record: Record):
        """Dodaje wpis do książki adresowej."""
        self.data[record.name.value] = record
        print(f"Dodano wpis.")

    def find_record(self, search_term):
        """Znajduje wpisy zawierające dokładną podaną frazę."""
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
        """Usuwa rekord o podanej nazwie."""
        if name in self.data:
            del self.data[name]
            print(f"Usunięto wpis: {name}.")
        else:
            print(f"Wpis o nazwie {name} nie istnieje.")

# Funkcje input do interakcji z użytkownikiem
def input_phone():
    """Prosi użytkownika o podanie numeru telefonu."""
    while True:
        try:
            number = input("Podaj numer telefonu w formacie '123456789' (naciśnij Enter, aby pominąć): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)

def input_email():
    """Prosi użytkownika o podanie adresu email."""
    while True:
        try:
            address = input("Podaj adres email (naciśnij Enter, aby pominąć): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)

def create_record():
    """Tworzy wpis do książki na podstawie danych wprowadzonych przez użytkownika."""
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
    """Główna funkcja programu."""
    book = AddressBook()
    while True:
        action = input("Wybierz akcję: dodaj (d), znajdź (z), usuń (u), koniec (q): ")
        if action in ['dodaj', 'd']:
            record = create_record()
            book.add_record(record)
        elif action in ['znajdź', 'znajdz', 'z']:
            search = input("Wpisz szukaną frazę: ")
            found = book.find_record(search)
            for record in found:
                print(record)
        elif action in ['usun', 'usuń', 'u']:
            name = input("Podaj imię i nazwisko do usunięcia: ")
            book.delete_record(name)
        elif action in ['koniec', 'q']:
            break

if __name__ == "__main__":
    main()
