import pandas as pd
import json


def load_data(filename):
    """Load data from csv file"""
    return pd.read_csv(filename)


def load_test_mark_data(data, col1, col2, col3):
    """Load data from Marks and Tests Dataframe"""
    data_dict = {}
    for j in range(len(data)):
        key = int(data[col2][j])
        if key not in data_dict.keys():
            data_dict[key] = []
        details = {col1: int(data[col1][j]), col3: int(data[col3][j])}
        data_dict[key].append(details)

    return data_dict


def calculate_avg(marks_list, tests_list, results):
    for student_id in marks_list.keys():
        total_avg = 0
        course_avg_list = []

        for course_id in tests_list.keys():
            course_avg = 0
            for test in marks_list[student_id]:
                for test_weight in tests_list[course_id]:
                    if test['test_id'] == test_weight['id']:
                        course_avg += test['mark'] * (test_weight['weight'] / 100)

            rounded_course_avg = round(course_avg, 2)

            for student_record in results["students"]:
                if student_id == student_record['id']:
                    for course in student_record['courses']:
                        if course_id == course['id']:
                            if rounded_course_avg != 0:
                                course_avg_list.append(rounded_course_avg)
                                course['courseAverage'] = rounded_course_avg
                            else:
                                student_record['courses'].remove(course)

        total_avg += sum(course_avg_list) / len(course_avg_list)

        for student_record in results["students"]:
            if student_id == student_record['id']:
                student_record['totalAverage'] = round(total_avg, 2)
                
                
if __name__ == '__main__':
    result = {"students": []}

    """Loading the data from students.csv"""
    stu_data = load_data('students.csv')

    for i in range(len(stu_data)):
        student_details = {'id': int(stu_data['id'][i]), 'name': stu_data['name'][i]}
        result["students"].append(student_details)

    """Loading the data from courses.csv"""
    course_data = load_data('courses.csv')

    for student in result["students"]:
        if 'courses' not in student.keys():
            student["courses"] = []
        for i in range(len(course_data)):
            course_details = {'id': int(course_data['id'][i]), 'name': course_data['name'][i],
                              'teacher': course_data['teacher'][i]}
            student["courses"].append(course_details)

    """Loading the data from marks.csv"""
    marks_data = load_data('marks.csv')
    marks = load_test_mark_data(marks_data, 'test_id', 'student_id', 'mark')

    """Loading the data from tests.csv"""
    tests_data = load_data('tests.csv')
    tests = load_test_mark_data(tests_data, 'id', 'course_id', 'weight')

    """Calculate Course and Total Average"""
    calculate_avg(marks, tests, result)

    """Dump the output into a json file"""
    with open('output.json', 'w') as fp:
        fp.write(json.dumps(result, indent=4))






