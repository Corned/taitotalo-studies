class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self) -> str:
        return f"<Person {self.first_name} {self.last_name}>"


class Student(Person):
    id_counter = 0

    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        Student.id_counter += 1
        self.id = Student.id_counter

    @property
    def email(self) -> str:
        return f"{self.first_name.lower()[0]}{self.last_name.lower()[0]}{str(self.id).rjust(6, '0')}@edu.taitotalo.fi"

    def __str__(self) -> str:
        return f"<Student {self.first_name} {self.last_name} ({self.id})>"


class Teacher(Person):
    def __init__(self, first_name: str, last_name: str, subject: str = "Unknown"):
        super().__init__(first_name, last_name)

    @property
    def email(self) -> str:
        return f"{self.first_name.lower()}.{self.last_name.lower()}@edu.taitotalo.fi"

    def __str__(self) -> str:
        return f"<Teacher {self.first_name} {self.last_name}>"


mika = Person("Mika", "Suomalainen")
print(mika)

seppo = Student("Seppo", "Suomalainen")
print(f"{seppo} - Email: {seppo.email}")

chrisu = Teacher("Christian", "Finnberg", "Python")
print(f"{chrisu} - Email: {chrisu.email}")


teijo = Student("Teijo", "Tehokas")
print(f"{teijo} - Email: {teijo.email}")
