class Student:
    def __init__(self, first_name: str, last_name: str):
        self.__completed_courses: list[str] = []
        self.first_name: str = first_name
        self.last_name: str = last_name

    def add_course(self, course_str):
        self.__completed_courses.append(course_str)

    def list_courses(self):
        print("\n".join(self.__completed_courses).strip())


matti = Student("Matti", "Meikäläinen")
matti.add_course("Python 101")
matti.add_course("Tietokannan perusteet")

matti.list_courses()

print(matti.__completed_courses)
