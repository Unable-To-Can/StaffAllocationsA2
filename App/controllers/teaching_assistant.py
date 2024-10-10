from App.database import db
from App.models.teaching_assistant import *
from sqlalchemy.exc import IntegrityError
from App.models import TeachingAssistant, Course, StaffCourse


def create_teaching_assistant(prefix, firstName, lastName, faculty, username, password):
    teachingAssistant = TeachingAssistant(
        prefix=prefix,
        firstName=firstName,
        lastName=lastName,
        faculty=faculty,
        username=username,
        password=password
    )

    db.session.add(teachingAssistant)
    try:
        db.session.commit()
        return teachingAssistant
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating TA: {e}")
        return None

def get_teachingAssistant(id):

    teachingAssistant = TeachingAssistant.query.filter_by(id=id).first()

    if teachingAssistant:
        return teachingAssistant
    
    return None

def fire_teaching_assistant(id):

    teachingAssistant = TeachingAssistant.query.filter_by(id = id).first()

    if teachingAssistant:
        name = teachingAssistant.prefix + " " + teachingAssistant.firstName + " " + teachingAssistant.lastName
        db.session.delete(teachingAssistant)
        db.session.commit()
        return "Teaching assistant: " + name +  " fired."
    
    return "Invalid teaching assistant id."

def add_teachingAssistant(courseid, ta_id):
    # Check if a record for the course already exists
    staff_course_entry = StaffCourse.query.filter_by(courseID=courseid).first()

    if staff_course_entry:
        # Update the existing entry with the new teaching assistant ID
        staff_course_entry.teachingAssistantID = ta_id
    else:
        # If no entry exists, create a new one
        staff_course_entry = StaffCourse(
            courseID=courseid,
            teachingAssistantID=ta_id,
            lecturerID=None,  # Assuming these fields can be set to None or some default value
            tutorID=None
        )
        db.session.add(staff_course_entry)

    # Commit the session
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        raise e  # Optionally raise the error for further handling


def validate_prefix(prefix):
    return prefix in ['Mrs.', 'Dr.', 'Mr.', 'Ms.']


def validate_faculty(faculty):
    return faculty in ['FOE', 'FST', 'FSS', 'FMS', 'FHE', 'FOL', 'FFA', 'FOS']


def create_and_confirm_ta(prefix, firstName, lastName, faculty, username, password):
    if not validate_prefix(prefix):
        return "Invalid prefix. Use: Dr., Mrs., Mr., or Ms."

    if not validate_faculty(faculty):
        return "Invalid faculty. Use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    ta = create_teaching_assistant(prefix, firstName, lastName, faculty, username, password)

    if ta is None:
        return f'Teaching assistant could not be created'
    
    return f'Teaching Assistant created {ta.prefix} {ta.firstName} {ta.lastName}. ID: {ta.id}'


def assign_ta(courseid, ta_id):
    course = Course.query.filter_by(id=courseid).first()
    ta = TeachingAssistant.query.filter_by(id=ta_id).first()
    taCheck = StaffCourse.query.filter_by(courseID=courseid).first()

    if ta is not None and taCheck and taCheck.teachingAssistantID == ta.id:
        return "Teaching assistant already assigned to course."

    taOld = TeachingAssistant.query.filter_by(id=taCheck.teachingAssistantID).first() if taCheck else None

    if taOld and ta:
        add_teachingAssistant(courseid, ta_id)
        return f"{taOld.prefix} {taOld.firstName} {taOld.lastName} replaced by {ta.prefix} {ta.firstName} {ta.lastName}."

    if course:
        if ta:
            add_teachingAssistant(courseid, ta_id)
            return f"{ta.prefix} {ta.firstName} {ta.lastName} now assigned to {course.name}."
        else:
            return "Teaching assistant does not exist."
    else:
        return "Course does not exist."
