from App.database import db
from App.models.lecturer import *
from sqlalchemy.exc import IntegrityError
from App.models import Lecturer, Course, StaffCourse

def create_lecturer(prefix, firstName, lastName, faculty, username, password):
    lecturer = Lecturer(
        prefix=prefix,
        firstName=firstName,
        lastName=lastName,
        faculty=faculty,
        username=username,
        password=password 
    )

    db.session.add(lecturer)
    try:
        db.session.commit()
        return lecturer
    except Exception as e:
        db.session.rollback() 
        print(f"Error creating lecturer: {e}")
        return None 

def get_lecturer(id):

    lecturer = Lecturer.query.filter_by(id = id).first()

    if lecturer:
        return lecturer

    return None


def fire_lecturer(id):

    lecturer = Lecturer.query.filter_by(id = id).first()

    if lecturer:
        name = lecturer.prefix + " " + lecturer.firstName + " " + lecturer.lastName
        db.session.delete(lecturer)
        db.session.commit()
        return "Lecturer: " + name + " fired."
    
    return "Invalid lecturer id."

def add_lecturer(courseid, lecturer_id):
    # Check if a record already exists for the given courseID
    existing_entry = StaffCourse.query.filter_by(courseID=courseid).first()

    if existing_entry:
        # Update the existing entry if necessary
        existing_entry.lecturerID = lecturer_id
        # Optionally update other fields
        existing_entry.teachingAssistantID = None  # Example of updating another field
        existing_entry.tutorID = None
    else:
        # Create a new entry since it doesn't exist
        staff_course_entry = StaffCourse(
            courseID=courseid,
            lecturerID=lecturer_id,
            teachingAssistantID=None,  # Assuming these are optional
            tutorID=None
        )
        db.session.add(staff_course_entry)

    # Commit the session
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        raise e  # Optionally raise the error for further handling

def assign_lecturer(courseid, lecturer_id):
    course = Course.query.filter_by(id=courseid).first()
    lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
    lecturerCheck = StaffCourse.query.filter_by(courseID=courseid).first()

    if lecturer is not None and lecturerCheck and lecturerCheck.lecturerID == lecturer.id:
        return "Lecturer already assigned to course."

    lecturerOld = Lecturer.query.filter_by(id=lecturerCheck.lecturerID).first() if lecturerCheck else None

    if lecturerOld and lecturer:
        add_lecturer(courseid, lecturer_id)
        return f"{lecturerOld.prefix} {lecturerOld.firstName} {lecturerOld.lastName} replaced by {lecturer.prefix} {lecturer.firstName} {lecturer.lastName}."

    if course:
        if lecturer:
            add_lecturer(courseid, lecturer_id)
            return f"{lecturer.prefix} {lecturer.firstName} {lecturer.lastName} now assigned to {course.name}."
        else:
            return "Lecturer does not exist."
    else:
        return "Course does not exist."

def validate_prefix(prefix):
    return prefix in ['Mrs.', 'Dr.', 'Mr.', 'Ms.', 'Prof.']


def validate_faculty(faculty):
    return faculty in ['FOE', 'FST', 'FSS', 'FMS', 'FHE', 'FOL', 'FFA', 'FOS']


def create_and_confirm_lecturer(prefix, firstName, lastName, faculty, username, password):
    if not validate_prefix(prefix):
        return "Invalid prefix. Use: Prof., Dr., Mrs., Mr., or Ms."

    if not validate_faculty(faculty):
        return "Invalid faculty. Use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    lecturer = create_lecturer(prefix, firstName, lastName, faculty, username, password)

    if lecturer is None:
        return "Failed to create lecturer. Please check the provided information."

    return f'Lecturer created: {lecturer.prefix} {lecturer.firstName} {lecturer.lastName}. ID: {lecturer.id}'


