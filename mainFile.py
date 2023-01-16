
from enrollStudent import StudentNode
from enrollStudent import EnrollTable
from enrollStudent import PriorityQueue


def main():
    """Main program function"""
    continueProg = True
    enrollment = EnrollTable(51)
    waitList = PriorityQueue()
    userInputList = ["R", "D", "Q"]
    studentNo = 50

    # program loop
    while continueProg == True:
        inputVal = ""
        while not inputVal:
            inputVal = input("Would you like to register or drop students [R/D]: ")
            if inputVal in userInputList:
                pass
            else:
                # incorrect input
                print("Please type a valid input")

        # Quitting the program
        if inputVal == userInputList[2]:
            continueProg = False
        else:
            # checking the validity of the file
            fileValid = False
            while not fileValid:
                try:
                    # reading the file
                    text = input("Please enter a filename for student records: ")
                    fileName = open(text)
                    file = fileName.read().split("\n")
                    fileValid = True
                    studentInfo = []
                    for line in file:
                        eachInfo = line.strip().split(' ')
                        if len(eachInfo) == 4:
                            studentInfo.append(eachInfo)

                except OSError:
                    print("Cannot read file")
                    fileValid = False

            # registering for a course
            if inputVal == userInputList[0]:
                for eachInfo in studentInfo[0:studentNo]:
                    # each student node
                    enrollment.insert(StudentNode(*eachInfo))
                print(enrollment)

                # extra students to join the waitList
                studentInfoLen = len(studentInfo)
                if studentNo < studentInfoLen:
                    for eachInfo in studentInfo[studentNo:]:  # slicing
                        waitList.enqueue(StudentNode(*eachInfo))  # filling up the priority queue
                print(waitList)

            # dropping classes
            elif inputVal == userInputList[1]:
                for eachInfo in studentInfo:
                    try:
                        # removing students
                        studentId, faculty, firstName, lastName = eachInfo
                        dropped = enrollment.remove(studentId)
                        if dropped:
                            enrollment.insert(waitList.dequeue())
                        else:
                            studentId, faculty, firstName, lastName = eachInfo
                            error = "{} {}(ID: {}) is not currently enrolled and cannot be dropped".format(firstName,
                                                                                                           lastName,
                                                                                                           studentId)
                            raise AssertionError(error)
                    except AssertionError as err:
                        print("WARNING: " + str(err))


main()
