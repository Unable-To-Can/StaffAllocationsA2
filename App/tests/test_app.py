import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Lecturer, Tutor, TeachingAssistant, Course
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


class StaffUnitTests(unittest.TestCase):
    def test_get_staff_json(self):
        staff = Staff("johnny", "johnnypassy", "Mr.", "John", "Lip", "FOE", "Tutor")
        staff_json = staff.get_json()
        self.assertDictEqual(staff_json, {"id":None, "prefix": "Mr.",
                                          "firstName": "John",
                                          "lastName": "Lip", "faculty": "FOE",
                                          "job": "Tutor"})


class StaffCourseUnitTests(unittest.TestCase):
    def test_get_staff_course_json(self):
        staff_course = StaffCourse(1, 1, 1, 1)
        staff_course_json = staff_course.get_json()
        self.assertDictEqual(staff_course_json, {"id": None, "courseID": 1,
                                                 "lecturerID": 1,
                                                 "teachingAssistantID": 1,
                                                 "tutorID": 1})


class CourseUnitTest(unittest.TestCase):
    def test_get_course_json(self):
        course = Course("MyCourse", "FST")
        course_json = course.get_json()
        self.assertDictEqual(course_json, {"name": "MyCourse",
                                           "faculty": "FST"})



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):
# ! all user test 
    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     expected_json = [
    #         {"id": 1, "username": "bob"},
    #         {"id": 2, "prefix": "Dr.", "firstName": "John", "lastName": "Doe", "faculty": "FOE", "job": "Lecturer"},
    #         {"id": 3, "prefix": "Mr.", "firstName": "John", "lastName": "Doe", "faculty": "FOE", "job": "Teaching Assistant"},
    #         {"id": 4, "prefix": "Mr.", "firstName": "John", "lastName": "Doe", "faculty": "FOE", "job": "Tutor"},
    #         {"id": 5, "username": "rick"}
    #     ]
    #     assert users_json == expected_json, f"Expected {expected_json}, but got {users_json}"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()

        expected_json = [
            {"id": 1, "username": "bob"},
            {"id": 2, "username": "rick"}
        ]
        assert users_json == expected_json, f"Expected {expected_json}, but got {users_json}"

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


# Integration Tests for Course Creation
class CourseIntegrationTests(unittest.TestCase):
    def test_create_course(self):
        course_name = "SoftwareEngineeringII"
        faculty = "FST"

        result = create_course(course_name, faculty)

        course = Course(name=course_name, faculty=faculty)

        assert course is not None
        assert course.name == course_name
        assert course.faculty == faculty

    def test_create_course_invalid_course_faculty(self):
        course_name = "MechanicalEngineeering101"
        faculty = "FOZ"

        result = create_course(course_name, faculty)

        assert result == "Incorrect faculty selected. Please use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"


# Integration Tests for Lecturer Creation
class LecturerIntegrationTests(unittest.TestCase):
    def test_create_and_confirm_lecturer(self):
        prefix = "Dr."
        firstname = "John"
        lastname = "Doe"
        faculty = "FOE"
        username = "johndoe"
        password = "password123"

        result = create_and_confirm_lecturer(prefix, firstname, lastname, faculty, username, password)

        assert "Lecturer created: Dr. John Doe" in result

        lecturer = Lecturer.query.filter_by(username=username).first()
        assert lecturer is not None
        assert lecturer.firstName == firstname
        assert lecturer.lastName == lastname
        assert lecturer.faculty == faculty

        
    def test_create_lecturer_with_invalid_prefix(self):
        prefix = "InvalidPrefix"
        firstname = "Jane"
        lastname = "Doe"
        faculty = "FOE"
        username = "janedoe"
        password = "password123"

        result = create_and_confirm_lecturer(prefix, firstname, lastname, faculty, username, password)

        assert result == "Invalid prefix. Use: Prof., Dr., Mrs., Mr., or Ms."

    def test_create_lecturer_with_invalid_faculty(self):
        prefix = "Dr."
        firstname = "Jane"
        lastname = "Doe"
        faculty = "InvalidFaculty"
        username = "janedoe"
        password = "password123"


        result = create_and_confirm_lecturer(prefix, firstname, lastname, faculty, username, password)


        assert result == "Invalid faculty. Use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    def test_assign_lecturer(self):
        course = get_course_by_id(1)
        lecturer = create_lecturer("Mr.", "TestFirst", "TestLast", "FOE", "testname", "testpass")      

        result = assign_lecturer(course.id, lecturer.id)
        assert "Mr. TestFirst TestLast" in result

        staff_course = StaffCourse.query.filter_by(courseID=course.id, lecturerID=lecturer.id).first()
        
        assert staff_course is not None
        assert staff_course.lecturerID == lecturer.id and staff_course.courseID == course.id

    # Integration Tests for Tutor Creation
class TutorIntegrationTests(unittest.TestCase):
    def test_create_and_confirm_tutor(self):
        prefix = "Mr."
        firstname = "John"
        lastname = "Doe"
        faculty = "FOE"
        username = "johnathondoe"
        password = "password123"

        result = create_and_confirm_tutor(prefix, firstname, lastname, faculty, username, password)

        assert "Tutor created: Mr. John Doe" in result

        tutor = Tutor.query.filter_by(username=username).first()
        assert tutor is not None
        assert tutor.firstName == firstname
        assert tutor.lastName == lastname
        assert tutor.faculty == faculty

    def test_create_tutor_with_invalid_prefix(self):
            prefix = "InvalidPrefix"
            firstname = "Jane"
            lastname = "Doe"
            faculty = "FOE"
            username = "janedoe"
            password = "password123"

            result = create_and_confirm_tutor(prefix, firstname, lastname, faculty, username, password)

            assert result == "Invalid prefix. Use: Prof., Dr., Mrs., Mr., or Ms."

    def test_create_tutor_with_invalid_faculty(self):
        prefix = "Ms."
        firstname = "Jane"
        lastname = "Doe"
        faculty = "InvalidFaculty"
        username = "janedoe"
        password = "password123"


        result = create_and_confirm_tutor(prefix, firstname, lastname, faculty, username, password)


        assert result == "Invalid faculty. Use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    def test_assign_tutor(self):
        course = get_course_by_id(1)
        tutor = create_tutor("Mr.", "TestFirst", "TestLast", "FOE", "tutorname", "tutorpass")
        result = assign_tutor(course.id, tutor.id)
        assert "Mr. TestFirst TestLast now assigned to" in result

        staff_course = StaffCourse.query.filter_by(courseID=course.id, tutorID=tutor.id).first()
        assert staff_course is not None
        assert staff_course.tutorID == tutor.id and staff_course.courseID == course.id

# Integration Tests for Teaching Assisstant Creation
class TeachingAssistantIntegrationTests(unittest.TestCase):
    def test_create_and_confirm_teaching_assistant(self):
        prefix = "Mr."
        firstname = "John"
        lastname = "Doe"
        faculty = "FOE"
        username = "johnnydoe"
        password = "password123"

        result = create_and_confirm_ta(prefix, firstname, lastname, faculty, username, password)
        print(username)

        # Update the expected string to match the actual output
        assert "Teaching Assistant created Mr. John Doe." in result  # Match the actual string without the colon
        assert "ID: " in result  # Optionally check for the presence of the ID in the result

        teaching_assistant = TeachingAssistant.query.filter_by(username=username).first()
        assert teaching_assistant is not None
        assert teaching_assistant.firstName == firstname
        assert teaching_assistant.lastName == lastname
        assert teaching_assistant.faculty == faculty

    def test_create_ta_with_invalid_prefix(self):
            prefix = "InvalidPrefix"
            firstname = "Jane"
            lastname = "Doe"
            faculty = "FOE"
            username = "janedoe"
            password = "password123"

            result = create_and_confirm_ta(prefix, firstname, lastname, faculty, username, password)

            assert result == "Invalid prefix. Use: Dr., Mrs., Mr., or Ms."

    def test_create_ta_with_invalid_faculty(self):
        
        prefix = "Ms."
        firstname = "Jane"
        lastname = "Doe"
        faculty = "InvalidFaculty"
        username = "janedoe"
        password = "password123"

        
        result = create_and_confirm_ta(prefix, firstname, lastname, faculty, username, password)

        
        assert result == "Invalid faculty. Use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    def test_assign_ta(self):
        course = get_course_by_id(1)
        ta = create_teaching_assistant("Mr.", "John", "Doe", "TA", "testta", "testpass")      
        
        result = assign_ta(course.id, ta.id)
        assert "Mr. John Doe" in result

        staff_course = StaffCourse.query.filter_by(courseID=course.id, teachingAssistantID=ta.id).first()
        
        assert staff_course is not None  
        assert staff_course.teachingAssistantID == ta.id and staff_course.courseID == course.id

class StaffCourseIntegrationTests(unittest.TestCase):
    def test_show_staff_in_course(self):
        course = create_course("Object Oriented Programming I", "FST")
        
        lecturer_message = create_and_confirm_lecturer("Dr.", "Penny", "Less", "FST", "penny", "pennypass")
        lecturer = Lecturer.query.filter_by(username="penny").first() 

        teaching_assistant_message = create_and_confirm_ta("Mr.", "David", "Rules", "FST", "david", "davidpass")
        teaching_assistant = TeachingAssistant.query.filter_by(username="david").first()  

        tutor_message = create_and_confirm_tutor("Ms.", "Carol", "Taylor", "FST", "carol", "carolpass")
        tutor = Tutor.query.filter_by(username="carol").first()  

        # Assign staff to the course
        assign_lecturer(course.id, lecturer.id)
        assign_tutor(course.id, tutor.id)
        assign_ta(course.id, teaching_assistant.id)

        # Retrieve staff assigned to the course
        staff = show_staff_in_course(course.id)
        
        assert staff is not None
        assert staff.lecturerID == lecturer.id
        assert staff.tutorID == tutor.id
        assert staff.teachingAssistantID == teaching_assistant.id

