from .user import create_user
from .lecturer import *
from .tutor import *
from .teaching_assistant import *
from .staff_course import *
from .course import *
from .admin import *
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()

    create_admin("bob","bobpass")

    create_course('Introduction to Psychology', 'FSS')
    create_course('Introduction to C++', 'FST')
    create_course('Psychology I', 'FSS')
    create_course('Industrial Statistics', 'FOE')
    create_course('Pharmacology II', 'FMS')

    create_lecturer('Dr.', 'Mark', 'Long', 'FMS', 'mlong', 'Markpass')
    create_lecturer('Mrs.', 'Hannah', 'Skeete', 'FSS', 'hskeete', 'Hannahpass')
    create_lecturer('Mr.', 'Gordon', 'Wallace', 'FST', 'gwallace', 'Gordonpass')
    create_lecturer('Dr.', 'Hailey', 'Singh', 'FOE', 'hsingh', 'Haileypass')
    create_lecturer('Dr.', 'Bailey', 'Wells', 'FSS', 'bwells', 'Baileypass')

    create_teaching_assistant('Mr.', 'Kim', 'Skeete', 'FSS', 'kskeete', 'Kimpass')
    create_teaching_assistant('Ms.', 'Jane', 'Good', 'FSS', 'jgood', 'Janepass')
    create_teaching_assistant('Ms.', 'Morgan', 'King', 'FMS', 'mking', 'Morganpass')
    create_teaching_assistant('Mr.', 'Brett', 'Long', 'FST', 'blong', 'Brettpass')
    create_teaching_assistant('Mrs.', 'Vikki', 'Khan', 'FOE', 'vkhan', 'Vikkipass')

    create_tutor('Mr.', 'John', 'Lip', 'FOE', 'jlip', 'Johnpass')
    create_tutor('Dr.', 'Alice', 'Brown', 'FSS', 'abrown', 'Alicepass')
    create_tutor('Ms.', 'Rachel', 'Green', 'FMS', 'rgreen', 'Rachelpass')
    create_tutor('Mr.', 'Michael', 'Smith', 'FST', 'msmith', 'Michaelpass')
    create_tutor('Mr.', 'David', 'Johnson', 'FSS', 'djohnson', 'Davidpass')

    add_staff(1, 2, 6, 12) 
    add_staff(2, 3, 9, 14)  
    add_staff(3, 5, 7, 15)  
    add_staff(4, 4, 10, 11)  
    add_staff(5, 1, 8, 13)  
