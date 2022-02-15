'''
course_search is a Python script using a terminal based menu to help
students search for courses they might want to take at Brandeis
'''

from schedule import Schedule
import sys

schedule = Schedule()
schedule.load_courses()
schedule = schedule.enrolled(range(5,1000)) # eliminate courses with no students

TOP_LEVEL_MENU = '''
quit
reset
term  (filter by term)
course (filter by coursenum, e.g. COSI 103a)
instructor (filter by instructor)
subject (filter by subject, e.g. COSI, or LALS)
title  (filter by phrase in title)
description (filter by phrase in description)
timeofday (filter by day and time, e.g. meets at 11 on Wed)
days (filter by meeting days–classes shown will only meet on the given days)
stillfree (filter the classes that have seats still available)
'''

terms = {c['term'] for c in schedule.courses}

def topmenu():
    '''
    topmenu is the top level loop of the course search app
    '''
    global schedule
    while True:         
        command = input(">> (h for help) ")
        if command=='quit':
            return
        elif command in ['h','help']:
            print(TOP_LEVEL_MENU)
            print('-'*40+'\n\n')
            continue
        elif command in ['r','reset']:
            schedule.load_courses()
            schedule = schedule.enrolled(range(5,1000))
            continue
        elif command in ['t', 'term']:
            term = input("enter a term:"+str(terms)+":")
            schedule = schedule.term([term]).sort('subject')
        elif command in ['s','subject']:
            subject = input("enter a subject:")
            schedule = schedule.subject([subject])
        elif command in ['ds', 'desc', 'description']:
            phrase = input("enter a phrase: ")
            schedule = schedule.description(phrase)
        elif command in ['d', 'days']:
            days = input("enter some days {m, tu, w, th, f} - comma separated: ")
            schedule = schedule.days(days.lower().replace(" ", "").split(","))
        elif command in ['i','instructor']:
            pointer = input("find instructor by email/last_name: ")
            while (pointer!="email" and pointer!= "last_name"):
                pointer = input("please type either email or last_name: ")
            if pointer == "email":
                email = input("enter instructor email address: ")
                schedule = schedule.email([email])
            else:
                last_name = input("enter instructor email address: ")
                schedule = schedule.lastname([last_name])
        elif command in ['still_free', 'sf']:
            subject = input("enter a subject:")
            schedule = schedule.stillFree([subject])
        else:
            print('command',command,'is not supported')
            continue

        print("courses has",len(schedule.courses),'elements',end="\n\n")
        print('here are the first 10')
        for course in schedule.courses[:10]:
            print_course(course)
        print('\n'*3)

def print_course(course):
    '''
    print_course prints a brief description of the course 
    '''
    print(course['subject'],course['coursenum'],course['section'],
          course['name'],course['term'],course['instructor'])

if __name__ == '__main__':
    topmenu()

