from collections import UserDict
from datetime import timedelta, date, datetime

import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Ім'я не знайдено")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Номер телефону повинен складати 10 цифр")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, '%d.%m.%Y').date()
            self.value = parsed_date.strftime('%d.%m.%Y')
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = None
        for p in self.phones:
            if p.value == phone:
                phone_to_remove = p
                break

        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Номер {phone} не знайдено.")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Номер {old_phone} не знайдено.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        if birthday:
            self.birthday = Birthday(birthday)


    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", День народження: {self.birthday.value}" if self.birthday else ""
        return f"Дані контактові: {self.name.value}, Телефон: {phones} {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Рекорд для {name} не знайдено.")

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday:
                try:
                    birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                    birthday_this_year = birthday_date.replace(year=today.year)

                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                    days_until_birthday = (birthday_this_year - today).days
                    if 0 <= days_until_birthday <= days:
                        congratulation_date = birthday_this_year

                        if birthday_this_year.weekday() in [5, 6]:
                            congratulation_date += timedelta(days=(7 - birthday_this_year.weekday()))

                        upcoming_birthdays.append({
                            "name": record.name.value,
                            "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                        })
                except ValueError:
                    continue
        return upcoming_birthdays


    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())