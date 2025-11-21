class Employee:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email = f"{first_name.lower()}.{last_name.lower()}@taitotalo.fi"


seppo = Employee("Seppo", "Suomalainen")
print(seppo.email)
