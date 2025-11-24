from typing import Iterable


class Student:
    def __init__(self, first_name: str, last_name: str):
        self.__completed_courses: list[str] = []
        self.first_name: str = first_name
        self.last_name: str = last_name

    def add_course(self, *courses: Iterable[str]):
        self.__completed_courses.extend(courses)

    def list_courses(self):
        print("Kurssit:\n" + "\n".join(self.__completed_courses).strip())


matti = Student("Matti", "Meikäläinen")
matti.add_course("Python 101")
matti.add_course("Tietokannan perusteet")

matti.list_courses()
