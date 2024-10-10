from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import (
    initialize,
    create_and_confirm_lecturer,
    create_and_confirm_ta,
    create_and_confirm_tutor,
    create_course,
    get_course_by_id,
    get_all_courses_json,
    get_staff_in_course_json,
    get_all_staff_json,
    assign_lecturer,
    assign_ta,
    assign_tutor,
    fire_lecturer,
    fire_teaching_assistant,
    fire_tutor
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
    return jsonify({'status': 'healthy'})


# GET METHODS

# GET /teaching_assistant - retrieves a list of teaching assistants
# @index_views.route('/staff/<int:staff_id', methods=['GET'])

@index_views.route('/get_course_staff/<int:course_id>/staff', methods=['GET'])
@jwt_required()
def get_all_course_staff(course_id):
    courses = get_course_by_id(course_id)

    if not courses:
        return jsonify({"message": "Course not found"}), 404

    staff = get_staff_in_course_json(courses.id)

    if not staff:
        return jsonify({"message": "Could not find staff for this course"}), 404

    return jsonify(staff), 200



# GET /list_courses - retrieve a list of the courses in the database
@index_views.route('/list_courses', methods=['GET'])
def get_courses():

    result = get_all_courses_json()

    if not result:
        return jsonify(({"message:", "No courses exist"})), 404

    return jsonify(result), 200


# GET /list_staff - retrieve a list of the staff in the database
@index_views.route('/list_staff', methods=['GET'])
def get_staff():
    staff = get_all_staff_json()

    if not staff:
        return jsonify(({"message:", "No courses exist"})), 404

    return jsonify(staff), 200

# POST METHODS - add data to the database by creation of a new object


# POST /courses - Create a new course
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


# POST /teaching_assistants create a TA (Admin only)
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


# POST /tutors create a tutor (Admin only)
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


# POST /courses/<int:course_id>/staff/lecturer assigns a lecturer to a course  (Admin only)
@index_views.route('/courses/<int:course_id>/staff/lecturer', methods=['POST'])
@jwt_required()
def assign_lecturer_view(course_id):
    data = request.get_json()
    lecturer_id = data.get('id')

    if not lecturer_id:
        return jsonify({"message": "Missing lecturer ID."}), 400

    result = assign_lecturer(course_id, lecturer_id)
    return jsonify({"message": result}), 200


# POST /courses/<int:course_id>/staff/ta assigns a ta to a course  (Admin only)
@index_views.route('/courses/<int:course_id>/staff/ta', methods=['POST'])
@jwt_required()
def assign_ta_view(course_id):
    data = request.get_json()
    ta_id = data.get('id')

    if not ta_id:
        return jsonify({"message": "Missing TA ID."}), 400

    result = assign_ta(course_id, ta_id)
    return jsonify({"message": result}), 200


# POST /courses/<int:course_id>/staff/tutor assigns a tutor to a course  (Admin only)
@index_views.route('/courses/<int:course_id>/staff/tutor', methods=['POST'])
@jwt_required()
def assign_tutor_view(course_id):
    data = request.get_json()
    tutor_id = data.get('id')

    if not tutor_id:
        return jsonify({"message": "Missing tutor ID."}), 400

    result = assign_tutor(course_id, tutor_id)
    return jsonify({"message": result}), 200


# POST /lecturer removes a lecturer from a course  (Admin only)
@index_views.route('/lecturer', methods=['DELETE'])
@jwt_required()
def terminate_lecturer():
    data = request.get_json()
    lecturer_id = data.get('id')

    if not lecturer_id:
        return jsonify({"message": "Missing lecturer ID."})

    result = fire_lecturer(lecturer_id)

    return jsonify({"message": result}), 200


# POST /teaching_assistant removes a teaching assistant from a course  (Admin only)
@index_views.route('/teaching_assistant', methods=['DELETE'])
@jwt_required()
def terminate_ta():
    data = request.get_json()
    ta_id = data.get('id')

    if not ta_id:
        return jsonify({"message": "Missing teaching assistant ID."})

    result = fire_teaching_assistant(ta_id)

    return jsonify({"message": result}), 200


# POST /tutor removes a tutor from a course  (Admin only)
@index_views.route('/tutor', methods=['DELETE'])
@jwt_required()
def terminate_tutor():
    data = request.get_json()
    tutor_id = data.get('id')

    if not tutor_id:
        return jsonify({"message": "Missing tutor ID."})

    result = fire_tutor(tutor_id)

    return jsonify({"message": result}), 200
