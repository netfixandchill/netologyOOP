class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.lecturer_grades = {}  # Для оценок лекторам

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self._calculate_avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return round(total / count, 1)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._calculate_avg_grade() < other._calculate_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self._calculate_avg_grade()
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade}")

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        total = sum(sum(grades) for grades in self.grades.values())
        count = sum(len(grades) for grades in self.grades.values())
        return round(total / count, 1)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._calculate_avg_grade() < other._calculate_avg_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"



def calculate_avg_hw_grade(students, course):
    total = 0
    count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return round(total / count, 1) if count else 0



def calculate_avg_lecture_grade(lecturers, course):
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return round(total / count, 1) if count else 0



student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Anna', 'Smith', 'female')
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ['Введение в программирование']


lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Another', 'Lecturer')
lecturer2.courses_attached += ['Python']


reviewer1 = Reviewer('John', 'Doe')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Jane', 'Smith')
reviewer2.courses_attached += ['Python']


reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student1, 'Python', 8)

reviewer1.rate_hw(student2, 'Python', 7)
reviewer1.rate_hw(student2, 'Python', 6)
reviewer2.rate_hw(student2, 'Python', 5)

student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Python', 9)
student2.rate_lecturer(lecturer1, 'Python', 8)

student1.rate_lecturer(lecturer2, 'Python', 7)
student1.rate_lecturer(lecturer2, 'Python', 6)
student2.rate_lecturer(lecturer2, 'Python', 5)


print("=== Проверяющие ===")
print(reviewer1)
print()
print(reviewer2)
print("\n=== Лекторы ===")
print(lecturer1)
print()
print(lecturer2)
print("\n=== Студенты ===")
print(student1)
print()
print(student2)


print("\n=== Сравнение лекторов ===")
print(f"lecturer1 > lecturer2: {lecturer1 > lecturer2}")
print("\n=== Сравнение студентов ===")
print(f"student1 > student2: {student1 > student2}")


print("\n=== Средние оценки ===")
students = [student1, student2]
lecturers = [lecturer1, lecturer2]
print(f"Средняя оценка студентов по Python: {calculate_avg_hw_grade(students, 'Python')}")
print(f"Средняя оценка лекторов по Python: {calculate_avg_lecture_grade(lecturers, 'Python')}")
