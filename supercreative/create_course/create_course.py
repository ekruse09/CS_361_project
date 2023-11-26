from supercreative.models import (Course, Section)


def create_course(id, name, description, code, role):

    # check to see if the id, name, description, code, and role are valid
    if not (isinstance(id, int) and id > 0):
        return False, "Invalid Course ID"

    if not (isinstance(name, str)):
        return False, "Invalid Course Name"

    if not isinstance(description, str):
        return False, "Invalid Course Description"

    if not (isinstance(code, str)):
        return False, "Invalid Course Code"

    if role != "administrator":
        return False, "Insufficient privileges"

    # check database for duplicate courses
    if Course.objects.filter(course_id=id).exists() or Course.objects.filter(course_name=name).exists() or Course.objects.filter(course_code=code).exists():
        return False, "Duplicate values found"

    # create the course
    new_course = Course(
        course_id=id,
        course_name=name,
        course_description=description,
        course_code=code
    )
    new_course.save()

    return True, "Course created successfully"

'''
Course.Create(p1, p2, p3, p4, p5, p6)
Preconditions:
CourseID is a non-null and unique integer
Course Name is a non-null and unique string
Course Description is a non-null string
Course Code is a non-null, unique, and properly formatted string (i.e. COMPSCI-361)
Active user role is Administrator
Postconditions: 
Return false if the CourseID, Course Name, or Course Code already exists in the Courses table or Archived Courses table and indicate duplicated value
Return false if active user role is not Administrator
Return true if input was valid, create an entry in the Courses table with the input information, and go to the Course Details Page for the new course.
Side-effects: none
p1: courseID input
p2: courseName input
p3: courseDescription input
p4: courseCode input
p5: role of active user
p6: boolean output


'''