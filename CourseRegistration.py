class CourseRegistration:

    def __init__(self, student_id, program, semester, max_credits=24):
        self.student_id = student_id
        self.program = program
        self.semester = semester
        self.max_credits = max_credits

        self.registered_courses = []
        self.registered_credits = 0

        self.completed_courses = {
            "Programming",
            "Data Structures",
            "Statistics",
            "Networking"
        }

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

        self.course_enrollment = {
            "DBMS": 0,
            "AI": 0,
            "ML": 0,
            "Cloud": 0
        }

    def calculate_total_credits(self):
        return self.registered_credits

    def register_course(self, course):

        # Invalid course
        if course not in self.courses:
            return "ERROR: Invalid course."

        info = self.courses[course]

        # Duplicate registration
        if course in self.registered_courses:
            return "ERROR: Duplicate registration."

        # Semester restriction
        if self.semester != info["semester"]:
            return "ERROR: Semester restriction."

        # Prerequisite
        if info["prerequisite"] not in self.completed_courses:
            return "ERROR: Missing prerequisite."

        # Credit limit
        if self.registered_credits + info["credits"] > self.max_credits:
            return "ERROR: Credit limit exceeded."

        # Course capacity
        if self.course_enrollment[course] >= info["capacity"]:
            return "ERROR: Course is full."

        # Timetable clash
        for registered_course in self.registered_courses:
            if self.courses[registered_course]["time"] == info["time"]:
                return "ERROR: Timetable conflict."

        # Register
        self.registered_courses.append(course)
        self.registered_credits += info["credits"]
        self.course_enrollment[course] += 1

        return "SUCCESS: Course registered."

    def get_registered_courses(self):
        return self.registered_courses

    def get_total_credits(self):
        return self.registered_credits
