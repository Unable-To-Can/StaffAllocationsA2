# Staff Allocation Platform

*The Staff Allocation Platform CLI application is specifically designed to streamline and manage the allocation of staff, including lecturers, tutors, and teaching assistants. It enables administrators to create courses and staff profiles, as well as assign the appropriate lecturers, tutors, and teaching assistants. Additionally, the application provides functionality for administrators to terminate and remove staff as needed. This application is developed using the Python Flask MVC framework and SQLAlchemy for database management.*

### Functions:
  - Create course
  - List courses
  - Create staff: lecturer, tutor, teaching assistant
  - List staff
  - Assign staff: lecturer, tutor, teaching assistant
  - Fire/Remove staff: lecturer, tutor, teaching assistant

## CLI Commands for Flask Application

### Commands relating to Course
 
- **Create Course Command**: 
  - **Command**: `createCourse`
  - **Description**: This command creates a course, Insert the course name and faculty.
  - **Usage**: `flask createCourse <courseName> <faculty> `
  - **Example**: `flask user create SWEN FST`

- **List Courses**: 
  - **Command**: `courses`
  - **Description**: Shows the list of all courses.
  - **Usage**: `flask courses`

### Commands relating to Staff

- **List Staff**: 
  - **Command**: `staff`
  - **Description**: Shows all staff.
  - **Usage**: `flask staff `
 
- **List Staff based on Course**: 
  - **Command**: `courseStaff`
  - **Description**: Shows all staff for the course code entered.
  - **Usage**: `flask courseStaff <courseID>`
  - **Example**: `flask courseStaff 6`

### Commands relating to Lecturer

- **Create Lecturer Command**: 
  - **Command**: `createLecturer`
  - **Description**: Creates a lecturer.
  - **Usage**: `flask createLecturer <prefix> <firstName> <lastName> <faculty> `
  - **Example**: `flask createLecturer Mr. Nicholas Mendez FST`
 
- **Assign Lecturer Command**: 
  - **Command**: `assignLecturer`
  - **Description**: Assigns a lecturer to a course even if a lecturer was already assigned.
  - **Usage**: `flask assignLecturer <courseID> <lecturerID> `
  - **Example**: `flask assignLecturer 6 12`
 
- **Fire Lecturer Command**: 
  - **Command**: `fireLecturer`
  - **Description**: Removes lecturer from the database and any course that they are assigned to.
  - **Usage**: `flask fireLecturer <lecturerID>`
  - **Example**: `flask fireLecturer 12`
 
- **Remove Lecturer Command**: 
  - **Command**: `removeLecturer`
  - **Description**: This command removes a lecturer from a course. 
  - **Usage**: `flask removeLecturer <courseID> <lecturerID> `
  - **Example**: `flask removeLecturer 6 12`
 
### Commands relating to Tutor

- **Create Tutor Command**: 
  - **Command**: `createTutor`
  - **Description**: Creates a tutor.
  - **Usage**: `flask createTutor <prefix> <firstName> <lastName> <faculty> `
  - **Example**: `flask createTutor Dr. Amit Ramkisoon FST`
 
- **Assign Tutor Command**: 
  - **Command**: `assignTutor`
  - **Description**: Assigns a tutor to a course even if a tutor was already assigned.
  - **Usage**: `flask assignTutor <courseID> <tutorID> `
  - **Example**: `flask assignTutor 6 20`
 
- **Fire Tutor Command**: 
  - **Command**: `fireTutor`
  - **Description**: Removes tutor from the database and any course that they are assigned to.
  - **Usage**: `flask fireTutor <tutorID>`
  - **Example**: `flask fireTutor 20`
 
- **Remove Tutor Command**: 
  - **Command**: `removeTutor`
  - **Description**: This command removes a tutor from a course. 
  - **Usage**: `flask removeTutor <courseID> <tutorID> `
  - **Example**: `flask removeTutor 6 20`
 
### Commands relating to Teaching Assistant

- **Create Teaching Assistant Command**: 
  - **Command**: `createTA`
  - **Description**: Creates a teaching assistant.
  - **Usage**: `flask createTA <prefix> <firstName> <lastName> <faculty> `
  - **Example**: `flask createTA Mr. Devon Murray FST`
 
- **Assign Teaching Assistant Command**: 
  - **Command**: `assignTA`
  - **Description**: Assigns a teaching assistant to a course even if a teaching assistant was already assigned.
  - **Usage**: `flask assignTA <courseID> <teachingAssistantID> `
  - **Example**: `flask assignTA 6 30`
 
- **Fire Teaching Assistant Command**: 
  - **Command**: `fireTA`
  - **Description**: Removes teaching assistant from the database and any course that they are assigned to.
  - **Usage**: `flask fireTA <teachingAssistantID>`
  - **Example**: `flask fireTA 30`
 
- **Remove Teaching Assistant Command**: 
  - **Command**: `removeTA`
  - **Description**: This command removes a teaching assistant from a course. 
  - **Usage**: `flask removeTA <courseID> <teachingAssistantID> `
  - **Example**: `flask removeTA 6 30`

### Other Commands

- **Database Migration Command**: 
  - **Command**: `db`
  - **Description**: Perform database migrations.
  - **Usage**: `flask db`
 
- **Initialization Command**: 
  - **Command**: `init`
  - **Description**: Creates and initializes the database.
  - **Usage**: `flask init `
 
- **Routes Command**: 
  - **Command**: `routes`
  - **Description**: Show the routes for the app.
  - **Usage**: `flask routes`
 
- **Run Command**: 
  - **Command**: `run`
  - **Description**: Run a development server. 
  - **Usage**: `flask run`
 
- **Shell Command**: 
  - **Command**: `shell`
  - **Description**: Run a shell in the app context. 
  - **Usage**: `flask shell`




### API Testing with Postman Collection
To run API tests using the Postman collection, you must have node.js and Newman installed. 
$  npm install -g newman


Then, add a script to your package.json file for running the collection, specifying the path to which the Postman collection file is saved:

"scripts": {
  "test": "newman run ./path/to/collection.json/"
}

After adding this, you can run the API tests by executing:
$ npm test

  

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```



## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
