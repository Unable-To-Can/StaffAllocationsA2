from App.database import db
from App.models import Course
from sqlalchemy.exc import IntegrityError



def create_course(name, faculty):
    valid_faculties = ['FOE', 'FST', 'FSS', 'FMS', 'FHE', 'FOL', 'FFA', 'FOS']
    if faculty not in valid_faculties:
        return "Incorrect faculty selected. Please use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"

    course = Course(name=name, faculty=faculty)
    try:
        db.session.add(course)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
    return course


def get_course_by_name(name):
    course = Course.query.filter_by(name=name).first()

    if course:
        return course
    
    return None 

def get_course_by_id(id):
    course = Course.query.filter_by(id = id).first()

    if course:
        return course
    
    return None

def get_all_courses():

    courses = Course.query.all()

    if courses:
        print('Course list: \n')
        for course in courses:
            print(course.id, course.name, course.faculty)
        return courses

    else:
        print('No courses available.')    
    return None

def get_all_courses_json():
    courses = get_all_courses()
    if not courses:
        return []
    result = [course.get_json() for course in courses]
    return result

def delete_course(id):

    course = get_course_by_id(id)

    if course: 
        db.session.delete(course)
        db.session.commit()
        return "Course removed."
    else:
        return None