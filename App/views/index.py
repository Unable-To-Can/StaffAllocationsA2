from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import (
    create_user, initialize,
    create_and_confirm_lecturer,
    create_and_confirm_ta,
    create_and_confirm_tutor,
    create_course,
    get_course_by_id,
    get_all_courses,
    show_staff_in_course,
    get_all_staff,
    assign_lecturer,
    assign_ta,
    assign_tutor
    )
from App.controllers import *
from flask_jwt_extended import jwt_required

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


# GET METHODS

# GET /teaching_assistant - retrieves a list of teaching assistants
# @index_views.route('/staff/<int:staff_id', methods=['GET'])

@index_views.route('/get_course_staff/<int:course_id>/staff', methods=['GET'])
@jwt_required()
def get_all_course_staff(course_id):
    courses = get_course_by_id(course_id)

    if not courses:
        return jsonify({"message": "Course not found"}), 404

    staff = show_staff_in_course(courses.id)

    if not staff:
        return jsonify({"message": "Could not find staff for this course"}),404
    
    result = [staff_course.get_json() for staff_course in staff]
    return jsonify(result), 200


#GET /list_courses - retrieve a list of the courses in the database
@index_views.route('/list_courses', methods=['GET'])
def get_courses():
    courses = get_all_courses()

    if not courses:
        return jsonify(({"message:", "No courses exist"})), 404
    
    result = [course.get_json() for course in courses]
    return jsonify(result), 200

#GET /list_staff - retrieve a list of the staff in the database
@index_views.route('/list_staff', methods=['GET'])
def get_staff():
    staff = get_all_staff()

    if not staff:
        return jsonify(({"message:", "No courses exist"})), 404
    
    result = [staff_member.get_json() for staff_member in staff]
    return jsonify(result), 200

# POST METHODS - add data to the database by creation of a new object

#POST /courses - Create a new course
@index_views.route('/courses', methods=['POST'])
@jwt_required()
def create_course_view():
    data = request.get_json()
    name = data.get('name')
    faculty = data.get('faculty')

    course = create_course(name, faculty)

    if course is not None and course != "Incorrect faculty selected. Please use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS":
        course = course.get_json()
        return jsonify(course), 201
    else:
        return jsonify({"error": "Incorrect faculty selected. Please use: FOE, FST, FSS, FMS, FHE, FOL, FFA, or FOS"}), 400


# POST /lecturers – Create a lecturer (Admin only)
@index_views.route('/lecturers', methods=['POST'])
@jwt_required()  
def create_lecturer_view():
    data = request.get_json()
    prefix = data.get('prefix')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    faculty = data.get('faculty')
    username = data.get('username')
    password = data.get('password')

    result = create_and_confirm_lecturer(prefix, firstName, lastName, faculty, username, password)

    if "Lecturer created" in result:
        return jsonify({"message": result}), 201
    else:
        return jsonify({"error": result}), 400


@index_views.route('/teaching_assistants', methods=['POST'])
@jwt_required()  
def create_teaching_assisstant_view():
    data = request.get_json()
    prefix = data.get('prefix')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    faculty = data.get('faculty')
    username = data.get('username')
    password = data.get('password')

    result = create_and_confirm_ta(prefix, firstName, lastName, faculty, username, password)

    if "Teaching Assistant created" in result:
        return jsonify({"message": result}), 201
    else:
        return jsonify({"error": result}), 400


@index_views.route('/tutors', methods=['POST'])
@jwt_required()  
def create_tutors_view():
    data = request.get_json()
    prefix = data.get('prefix')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    faculty = data.get('faculty')
    username = data.get('username')
    password = data.get('password')

    result = create_and_confirm_tutor(prefix, firstName, lastName, faculty, username, password)

    if "Tutor created" in result:
        return jsonify({"message": result}), 201
    else:
        return jsonify({"error": result}), 400



@index_views.route('/courses/<int:course_id>/staff/lecturer', methods=['POST'])
def assign_lecturer_view(course_id):
    data = request.get_json()
    lecturer_id = data.get('id')
    
    if not lecturer_id:
        return jsonify({"message": "Missing lecturer ID."}), 400

    result = assign_lecturer(course_id, lecturer_id)
    return jsonify({"message": result}), 200


@index_views.route('/courses/<int:course_id>/staff/ta', methods=['POST'])
def assign_ta_view(course_id):
    data = request.get_json()
    ta_id = data.get('id')
    
    if not ta_id:
        return jsonify({"message": "Missing TA ID."}), 400

    result = assign_ta(course_id, ta_id)
    return jsonify({"message": result}), 200

@index_views.route('/courses/<int:course_id>/staff/tutor', methods=['POST'])
def assign_tutor_view(course_id):
    data = request.get_json()
    tutor_id = data.get('id')
    
    if not tutor_id:
        return jsonify({"message": "Missing tutor ID."}), 400

    result = assign_tutor(course_id, tutor_id)
    return jsonify({"message": result}), 200

