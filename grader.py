import os
import sys
import argparse

def add_course(course_name):
    print("todo")

def add_assignment_type(course_name, type_name, type_weight):
    print("todo")

def add_assignment(course_name, type_name, grades):
    print("todo")

def list(course_name, verbosity):
    print("todo")

def main():
    working_folder = "./courses"
    if not os.path.exists(working_folder):
        os.mkdir(working_folder)
    
    parser = argparse.ArgumentParser(prog="Grader", description="Tabulates grades")
    parser.add_argument("action", choices=["add_course", "add_type", "add_assignment", "list"], help="Action to run")
    parser.add_argument("-v", "--verbose", action='store_true', help="Increase output verbosity")
    parser.add_argument("-c", "--course", help="Course name to interact with")
    parser.add_argument("-t", "--assignment_type", help="Assignment type to interact with")
    parser.add_argument("-w", "--weight", help="Weight of assignment type")
    parser.add_argument("-g", "--grade", help="Grade for an assignment type")

    args = parser.parse_args()
    
    if (args.action == "add_course"):
        if (args.course is None):
            parser.error("add_course requires --course")
        add_course(args.course)
    elif (args.action == "add_type"):
        if (args.course is None or args.assignment_type is None or args.weight is None):
            parser.error("add_type requires --course and --assignment_type and --weight")
        add_assignment_type(args.course, args.assignment_type, args.weight)
    elif (args.action == "add_assignment"):
        if (args.course is None or args.assignment_type is None or args.grade is None):
            parser.error("add_assignment requires --course and --assignment_type and --grade")
        add_assignment(args.course, args.assignment_type, args.grade)
    elif (args.action == "list"):
        list(args.course, args.verbosity)
    
if __name__ == "__main__":
    main()