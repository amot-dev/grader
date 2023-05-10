import os
import sys
import argparse
import click
from pathlib import Path
from glob import glob
from lxml import etree
from fractions import Fraction

working_folder = "./courses"

def add_course(course_name):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if os.path.exists(course_file):
        sys.exit("Error: Course already exists.")
        
    course = etree.Element("course")
    course.set("name", course_name)
    etree.ElementTree(course).write(course_file, pretty_print=True)
    print("Course added.")
    return

def remove_course(course_name):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if not os.path.exists(course_file):
        sys.exit("Error: Course does not exist.")
        
    if click.confirm("Are you sure you want to remove" + course_name + "?", default=False):
        os.remove(course_file)
        print("Course removed.")
    return


def add_assignment_type(course_name, type_name, type_weight):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if not os.path.exists(course_file):
        sys.exit("Error: Course does not exist.")
    course = etree.parse(course_file).getroot()
    for assignment_type in course:
        if (assignment_type.get("name") == type_name):
            sys.exit("Error: Assignment Type already exists.")
            
    assignment_type = etree.SubElement(course, "type")
    assignment_type.set("name", type_name)
    assignment_type.set("weight", str(type_weight))
    etree.ElementTree(course).write(course_file, pretty_print=True)
    print("Assignment Type added.")


def remove_assignment_type(course_name, type_name):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if not os.path.exists(course_file):
        sys.exit("Error: Course does not exist.")
    course = etree.parse(course_file).getroot()
    current_type = None
    for assignment_type in course:
            if (assignment_type.get("name") == type_name):
                current_type = assignment_type
    if current_type is None:
        sys.exit("Error: Assignment Type does not exist")
        
    if click.confirm("Are you sure you want to remove " + type_name + " from " + course_name + "?", default=False):
        current_type.getparent().remove(current_type)
        etree.ElementTree(course).write(course_file, pretty_print=True)
        print("Assignment Type removed.")
    return


def add_assignment(course_name, type_name, assignment_name, grade):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if not os.path.exists(course_file):
        sys.exit("Error: Course does not exist.")
    course = etree.parse(course_file).getroot()
    current_type = None
    for assignment_type in course:
            if (assignment_type.get("name") == type_name):
                current_type = assignment_type
    if current_type is None:
        sys.exit("Error: Assignment Type does not exist")
    for assignment in current_type:
        if (assignment.get("name") == assignment_name):
            sys.exit("Error: Assignment already exists.")
    assignment = etree.SubElement(current_type, "assignment")
    assignment.set("name", assignment_name)
    assignment.set("score", str(grade.numerator))
    assignment.set("total", str(grade.denominator))
    etree.ElementTree(course).write(course_file, pretty_print=True)
    print("Assignment added.")


def remove_assignment(course_name, type_name, assignment_name):
    course_file = os.path.join(working_folder, course_name + ".xml")
    if not os.path.exists(course_file):
        sys.exit("Error: Course does not exist.")
    course = etree.parse(course_file).getroot()
    current_type = None
    for assignment_type in course:
            if (assignment_type.get("name") == type_name):
                current_type = assignment_type
    if current_type is None:
        sys.exit("Error: Assignment Type does not exist")
    current_assignment = None
    for assignment in current_type:
            if (assignment.get("name") == assignment_name):
                current_assignment = assignment
    if current_assignment is None:
        sys.exit("Error: Assignment does not exist")
        
    if click.confirm("Are you sure you want to remove " + assignment_name + " from " + course_name + " " + type_name + "?", default=False):
        current_assignment.getparent().remove(current_assignment)
        etree.ElementTree(course).write(course_file, pretty_print=True)
        print("Assignment removed.")
    return


def list_grades(course_name, verbose):
    course_list = []
    if course_name is None:
        for file in glob(os.path.join(working_folder, "*.xml")):
            course_list.append(file)
        if not course_list:
            sys.exit("Error: No courses found.")
    else:
        course_file = os.path.join(working_folder, course_name + ".xml")
        if not os.path.exists(course_file):
            sys.exit("Error: Course does not exist.")
        course_list.append(course_file)
        
    for current_course in course_list:
        course_grade = 0.0
        type_grades = {}
        course = etree.parse(current_course).getroot()
        for current_type in course:
            type_score = 0
            type_total = 0
            for current_assignment in current_type:
                type_score += int(current_assignment.get("score"))
                type_total += int(current_assignment.get("total"))
            type_grade = 0.0
            if (type_total != 0):
                type_grade = type_score / type_total
            course_grade += type_grade * float(current_type.get("weight"))
            type_grades[current_type.get("name")] = type_grade
        
        print(Path(current_course).stem + " -> " + f"{course_grade:.0%}")
        for current_type in course:
            type_grade = type_grades[current_type.get("name")]
            print("    " + current_type.get("name") + " -> " + f"{type_grade:.0%}")
            if verbose:
                for current_assignment in current_type:
                    assignment_grade = 0.0
                    if (int(current_assignment.get("total")) != 0):
                        assignment_grade = int(current_assignment.get("score")) / int(current_assignment.get("total"))
                    print("        " + current_assignment.get("name") + " -> " + f"{assignment_grade:.0%}")
    return


def main():
    if not os.path.exists(working_folder):
        os.mkdir(working_folder)
    
    parser = argparse.ArgumentParser(prog="Grader", description="Tabulates grades")
    parser.add_argument("action", choices=["add", "remove", "list"], help="Action to run. Item to add/remove inferred. List can optionally take course name")
    parser.add_argument("-v", "--verbose", action='store_true', help="Increase output verbosity")
    parser.add_argument("-c", "--course", help="Course name to interact with")
    parser.add_argument("-t", "--assignment_type", help="Assignment type to interact with")
    parser.add_argument("-w", "--weight", type=float, help="Weight of assignment type")
    parser.add_argument("-a", "--assignment", help="Assignment to interact with")
    parser.add_argument("-g", "--grade", help="Grade for an assignment")

    args = parser.parse_args()
    
    if (args.action == "add"):
        # Invalid if no course is provided
        if (args.course is None):
            parser.error("add requires --course")
        # If no assignment_type provided, must be course addition
        elif (args.assignment_type is None):
            add_course(args.course)
        # If no assignment provided, must be assignment_type addition
        elif (args.assignment is None):
            # assignment_type requires weight
            if (args.weight is None):
                parser.error("add assignment_type requires --weight")
            add_assignment_type(args.course, args.assignment_type, args.weight)
        # If all provided, must be assignment addition
        else:
            # assignment requires grade
            if (args.grade is None):
                parser.error("add assignment requires --grade")
            grade = None
            try:
                grade = Fraction(args.grade)
            except:
                sys.exit("Error: Given grade is not valid.")
            add_assignment(args.course, args.assignment_type, args.assignment, grade)
    elif (args.action == "remove"):
        # Invalid if no course is provided
        if (args.course is None):
            parser.error("remove requires --course")
        # If no assignment_type provided, must be course removal
        elif (args.assignment_type is None):
            remove_course(args.course)
        # If no assignment provided, must be assignment_type removal
        elif (args.assignment is None):
            remove_assignment_type(args.course, args.assignment_type)
        # If all provided, must be assignment removal
        else:
            remove_assignment(args.course, args.assignment_type, args.assignment)
    elif (args.action == "list"):
        list_grades(args.course, args.verbose)
    return
    
if __name__ == "__main__":
    main()