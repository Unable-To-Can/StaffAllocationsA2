from App.models import StaffCourse, Lecturer, Tutor, TeachingAssistant, Course
from App.database import db
from sqlalchemy.exc import IntegrityError


def add_course_only(course):
    courseOnly = StaffCourse(courseID=course.id, lecturerID=None, teachingAssistantID=None, tutorID=None)
    
    if course and courseOnly:
        print("Course", course.name, "created. Faculty:", course.faculty)
        try:
            db.session.add(courseOnly)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(e.orig)
            return
    else:
        print('Course not created')
    return courseOnly


def add_staff(courseID, lecturerID, teachingAssistantID, tutorID):
    staffCourse = StaffCourse(courseID = courseID, lecturerID = lecturerID, teachingAssistantID = teachingAssistantID, tutorID= tutorID)

    try:
        db.session.add(staffCourse)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(e.orig)
    return staffCourse

def show_staff_in_course(courseID):

    staff_in_course = StaffCourse.query.filter_by(courseID = courseID).first()

    if staff_in_course:
        return staff_in_course
    
    return None

def get_staff_in_course_json(course_id):
    staff_c = StaffCourse.query.filter_by(courseID=course_id).all()  
    staff_list = []
    for staff_cs in staff_c:
        staff_list.append({
            "id": staff_cs.id,  
            "lecturerID": staff_cs.lecturerID,  
            "teachingAssistantID": staff_cs.teachingAssistantID,  
            "tutorID": staff_cs.tutorID  
        })
    return staff_list



def print_staff_info(staff_course):
    if staff_course:
        lecturer =  Lecturer.query.filter_by(id = staff_course.lecturerID).first()
        teaching_assistant = TeachingAssistant.query.filter_by(id = staff_course.teachingAssistantID).first()
        tutor = Tutor.query.filter_by(id = staff_course.tutorID).first()

        if lecturer:
            print(f"Lecturer: {lecturer.id}, {lecturer.prefix} {lecturer.firstName} {lecturer.lastName}, Faculty: {lecturer.faculty}, Job: {lecturer.job}")
        else:
            print("No lecturer assigned to this course.")

        if teaching_assistant:
            print(f"Teaching Assistant: {teaching_assistant.id}, {teaching_assistant.prefix} {teaching_assistant.firstName} {teaching_assistant.lastName}, Faculty: {teaching_assistant.faculty}, Job: {teaching_assistant.job}")
        else:
            print("No teaching assistant assigned to this course.")

        if tutor:
            print(f"Tutor: {tutor.id}, {tutor.prefix} {tutor.firstName} {tutor.lastName}, Faculty: {tutor.faculty}, Job: {tutor.job}")
        else:
            print("No tutor assigned to this course.")
    else:
        print("No staff information available for this course.")


def add_lecturer(courseID, id):

    lecturer = Lecturer.query.filter_by(id = id).first()

    if lecturer:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse:
            staffCourse.lecturerID = id
            db.session.commit()
            return staffCourse
        
    else:
        return None

def add_teachingAssistant(courseID, id):

    teachingAssistant = TeachingAssistant.query.filter_by(id = id).first()

    if teachingAssistant:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse:
            staffCourse.teachingAssistantID = id
            db.session.commit()
            return staffCourse
        
    else:
        return None

def add_tutor(courseID, id):

    tutor = Tutor.query.filter_by(id = id).first()

    if tutor:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse:
            staffCourse.tutorID = id
            db.session.commit()
            return staffCourse
        
        
    else:
        return None
    
def remove_lecturer_from_course(courseID, id):

    lecturer = Lecturer.query.filter_by(id = id).first()

    if lecturer:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse and staffCourse.lecturerID == lecturer.id:
            staffCourse.lecturerID = None
            db.session.commit()
            return "Lecturer removed."
        else:
            return "Lecturer not assigned to selected course."
        
        
    else:
        return None
    
def remove_teachingAssistant_from_course(courseID, id):

    teachingAssistant = TeachingAssistant.query.filter_by(id = id).first()

    if teachingAssistant:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse and staffCourse.teachingAssistantID == teachingAssistant.id:
            staffCourse.teachingAssistantID = None
            db.session.commit()
            return "Teaching assistant removed."
        else:
            return "Teaching assistant not assigned to selected course."
        
        
    else:
        return None

def remove_tutor_from_course(courseID, id):

    tutor = Tutor.query.filter_by(id = id).first()

    if tutor:
        staffCourse = StaffCourse.query.filter_by(courseID = courseID).first()

        if staffCourse and staffCourse.tutorID == tutor.id:
            staffCourse.tutorID = None
            db.session.commit()
            return "Tutor removed."
        else:
            return "Tutor not assigned to selected course."
        
        
    else:
        return None
    
def remove_course_record(courseID):

    course  = Course.query.filter_by(id = courseID).first()

    if course:
        staffCourse = StaffCourse.query.filter_by(courseID = course.id).first()
        if staffCourse:
            db.session.delete(staffCourse)
            db.session.commit()
            return "Course record removed."
        else:
            return "Course not in record."
    else:
        return "Course does not exist."
