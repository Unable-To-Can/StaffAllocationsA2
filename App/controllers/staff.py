from App.database import db
from App.models import Staff


def get_all_staff(): 
    staff = Staff.query.all()
    if staff:
        return staff
    return None

def get_all_staff_json():
    staff = get_all_staff()

    if not staff:
        return []
    
    staff = [staff_temp.get_json() for staff_temp in staff]
    return staff

def get_staff_by_faculty(faculty):
    staff = Staff.query.filter_by(faculty = faculty).first()
    if staff:
        return staff
    return None

def print_staff_list(staff):
    if staff:
        print('Full Staff List:')
        for member in staff:
            print(member.id, member.prefix, member.firstName, member.lastName, member.faculty, member.job)
    else:
        print('No Staff Present.')






