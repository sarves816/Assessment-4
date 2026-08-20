class CourseRegistration:
    def __init__(self, student_id, program, semester, max_credits=24):
        self.student_id = student_id
        self.program = program
        self.semester = semester
        self.max_credits = max_credits

        self.registered_courses = []
        self.registered_credits = 0

        # Course: credits, prerequisite, capacity, semester
        self.courses = {
            "DBMS": {
                "credits": 4,
                "prerequisite": "Programming",
                "capacity": 2,
                "semester": 3,
                "time": "10:00-11:00"
            },
            "AI": {
                "credits": 4,
                "prerequisite": "Data Structures",
                "capacity": 2,
                "semester": 5,
                "time": "11:00-12:00"
            },
            "ML": {
                "credits": 3,
                "prerequisite": "Statistics",
                "capacity": 2,
                "semester": 5,
                "time": "10:00-11:00"
            },
            "Cloud": {
                "credits": 3,
                "prerequisite": "Networking",
                "capacity": 2,
                "semester": 6,
                "time": "12:00-13:00"
            }
        }

        # Subjects already completed by the student
        self.completed_courses = {
            "Programming",
            "Data Structures",
            "Statistics",
            "Networking"
        }

        # Number of students currently registered
        self.course_enrollment = {
            "DBMS": 0,
            "AI": 0,
            "ML": 0,
            "Cloud": 0
        }

    def calculate_total_credits(self):
        return self.registered_credits

    def register_course(self, course):

        # 1. Invalid course
        if course not in self.courses:
            return "ERROR: Invalid course."

        course_info = self.courses[course]

        # 2. Duplicate registration
        if course in self.registered_courses:
            return "ERROR: Duplicate registration."

        # 3. Semester restriction
        if self.semester != course_info["semester"]:
            return "ERROR: Semester restriction."

        # 4. Prerequisite check
        prerequisite = course_info["prerequisite"]

        if prerequisite not in self.completed_courses:
            return "ERROR: Missing prerequisite."

        # 5. Credit limit check
        credits = course_info["credits"]

        if self.registered_credits + credits > self.max_credits:
            return "ERROR: Credit limit exceeded."

        # 6. Course capacity check
        if self.course_enrollment[course] >= course_info["capacity"]:
            return "ERROR: Course is full."

        # 7. Timetable conflict
        new_time = course_info["time"]

        for registered_course in self.registered_courses:
            if self.courses[registered_course]["time"] == new_time:
                return "ERROR: Timetable conflict."

        # Register course
        self.registered_courses.append(course)
        self.registered_credits += credits
        self.course_enrollment[course] += 1

        return "SUCCESS: Course registered."

    def get_registered_courses(self):
        return self.registered_courses

    def get_total_credits(self):
        return self.registered_credits


if __name__ == "__main__":
    # Manual execution
    student_id = input("Enter Student ID: ")
    program = input("Enter Program: ")
    semester = int(input("Enter Semester: "))

    student = CourseRegistration(student_id, program, semester)

    print("\nAvailable Courses:")
    print("DBMS - 4 credits")
    print("AI - 4 credits")
    print("ML - 3 credits")
    print("Cloud - 3 credits")

    course = input("\nEnter course to register: ")

    result = student.register_course(course)

    print(result)
    print("Registered courses:", student.get_registered_courses())
    print("Total credits:", student.get_total_credits())
