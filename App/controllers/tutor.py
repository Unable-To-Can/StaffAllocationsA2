from App.database import db
from App.models.tutor import *

def create_tutor(prefix, firstName, lastName, faculty):

    tutor = Tutor(prefix = prefix, firstName = firstName, lastName = lastName, faculty = faculty)
    db.session.add(tutor)
    db.session.commit()

    return tutor

def get_tutor(id):
    tutor = Tutor.query.filter_by(id = id).first()

    if tutor:
        return tutor
    
    return None

def fire_tutor(id):

    tutor = Tutor.query.filter_by(id = id).first()

    if tutor:
        db.session.delete(tutor)
        db.session.commit()
    
def assign_tutor(courseid, id):
    course = Course.query.filter_by(id=courseid).first()
    tutor = Tutor.query.filter_by(id=id).first()
    tutorCheck = StaffCourse.query.filter_by(courseID=courseid).first()
    tutorOld = Tutor.query.filter_by(id=tutorCheck.tutorID).first()

    if tutor is not None and tutorCheck.tutorID == tutor.id:
        return "Tutor already assigned to course."

    if tutorOld is not None and tutor:
        add_tutor(courseid, id)
        return f"{tutorOld.prefix} {tutorOld.firstName} {tutorOld.lastName} replaced by {tutor.prefix} {tutor.firstName} {tutor.lastName}"

    if course:
        if tutor:
            add_tutor(courseid, id)
            return f"{tutor.prefix} {tutor.firstName} {tutor.lastName} now assigned to {course.name}."
        else:
            return "Tutor does not exist."
    else:
        return "Course does not exist."
