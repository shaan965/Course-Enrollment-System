"""
In this first part of the assignment, you will implement an enrollment table to store the data for students
registering in a course. The maximum capacity for the course is 50 students. The maximum number of
slots in the table is 51 but no more students than 50 will be added to the table at any time.
Author: Muhammad Safwan Hossain
"""


class StudentNode:
    def __init__(self, indx, faculty, first, last):
        """creates a new student node instance"""
        self.__indx = indx
        self.__faculty = faculty
        self.__first = first
        self.__last = last
        self.__next = None
        self.__previous = None

    '''setters'''

    def setId(self, indx):
        """Sets the id of student"""
        self.__indx = indx

    def setFac(self, faculty):
        """Sets the faculty of student"""
        self.__faculty = faculty

    def setFirstName(self, first):
        """Sets the first name of student"""
        self.__first = first

    def setLastName(self, last):
        """Sets the last name of student"""
        self.__last = last

    def setNext(self, nextNode):
        """Sets the next node of student"""
        self.__next = nextNode

    def setPrev(self, prevNode):
        """Sets the previous node of student"""
        self.__previous = prevNode

    '''getters'''

    def getId(self):
        """Gets the id of student"""
        return self.__indx

    def getFac(self):
        """Gets the faculty of student"""
        return self.__faculty

    def getFirstName(self):
        """Gets the first name of student"""
        return self.__first

    def getLastName(self):
        """Gets the last name of student"""
        return self.__last

    def getNext(self):
        """Gets the next node of student"""
        return self.__next

    def getPrev(self):
        """Gets the previous node of student"""
        return self.__previous

    def __str__(self):
        """String representation of the class"""
        idStr = str(self.__indx)
        facStr = str(self.__faculty)
        firstStr = str(self.__first)
        lastStr = str(self.__last)

        stringRep = "{} {} {} {}".format(idStr, facStr, firstStr, lastStr)

        return stringRep


class EnrollTable:
    def __init__(self, capacity):
        self.__capacity = capacity
        self.__size = 0
        self.__table = []
        for i in range(self.__capacity):
            self.__table.append(None)
        self.__head = None

    def cmputIndex(self, studentID):
        numList = []
        x = 0
        y = 1
        sum1 = 0

        # splitting the digits into 2 digit numbers
        for i in range(0, int(len(studentID) / 2)):
            numList.append(studentID[x:y + 1])
            x += 2
            y += 2

        # squaring the last digit
        numList[-1] = int(numList[-1]) * int(numList[-1])

        # getting sum
        for i in numList:
            sum1 += int(i)

        # getting the index position
        indexPos = sum1 % self.__capacity

        return indexPos

    def insert(self, item):
        """Inserting an item to the desired position"""
        itemIndex = item.getId()
        pos = self.cmputIndex(itemIndex)

        # condition for empty or full list
        if self.__table[pos] is None:
            self.__table[pos] = item
        else:
            # checking for other positions
            lastPos = self.__table[pos]
            currentPos = lastPos.getNext()

            # inserting the node at the head
            if lastPos.getId() > item.getId():
                # referencing the second item of the list
                item.setNext(lastPos)
                self.__table[pos] = item

            while currentPos.getId < item.getId() and currentPos is not None:
                if lastPos.getId() == item.getId():
                    print("Error: the student ID already exists.")
                lastPos = currentPos
                currentPos = currentPos.getNext()

            # inserting an object at the middle of the table

            item.setNext(currentPos)
            lastPos.setNext(item)

        self.__size += 1

    def remove(self, studentID):
        """Removes the item from a specific location given in the parameter"""
        pos = self.cmputIndex(studentID)
        found = False
        current = self.__table[pos]

        # If removing head
        if current is None:
            found = False

        elif current.getNext() is None:
            if current.getId() == studentID:
                self.__table[pos] = None
                found = True
        else:
            previous = current
            current = current.getNext()

            while current is not None and not found:
                if current.getId() == studentID:
                    previous.setNext(current.getNext())
                    found = True
        if found:
            self.__size -= 1

        return found

    def isEnrolled(self, studentID):
        """Checking if a student is enrolled in a course or not"""
        found = False
        pos = self.cmputIndex(studentID)
        current = self.__table[pos]
        while current is not None and not found:
            if current.getId() == studentID:
                found = True
            current = current.getNext()

        return found

    def size(self):
        """returns size of table"""
        return self.__size

    def isEmpty(self):
        """returns true or false depending on the list is empty or not"""
        return self.__size == 0

    def __listRep(self, head):
        """gets the objects of the table"""
        current = head
        output = []
        while current is not None:
            # adding all items of table in the list
            output.append(str(current))
            current = current.getNext()

        displayObj = ", ".join(output)

        return displayObj

    def __str__(self):
        """String representation of the table"""
        stringRep = []
        output = []
        alignment = 10
        # getting the items of the table
        for pos, val in enumerate(self.__table):
            if val:  # checking available values
                displayObj = self.__listRep(val)
                stringRep.append(f"{pos}:{' ' if pos < alignment else ''} {displayObj}")

        display = "[" + ',\n'.join(stringRep) + "]"

        return display


class PriorityQueue:
    """The highest priority nodes will be dequeued from the front of the
queue and the lowest priority nodes will be enqueued to the rear of the queue."""

    def __init__(self):
        self.__queue = {'SCI': 4, 'ENG': 3, 'BUS': 2, 'ART': 1, 'EDU': 0}
        self.__head = None
        self.__tail = None
        self.__size = 0

    def enqueue(self, item):
        """enqueues a new student node to the rear of the queue or traverses the queue to
        determine the position in which the new node will be inserted based on the faculty priority of the given
        item,"""

        # empty list
        if self.__size == 0:
            self.__head, self.__tail = item, item
        else:
            # traversing like a linked list
            current = self.__head
            currentFac = current.getFac()
            itemFac = item.getFac()
            currentQueue = self.__queue[currentFac]
            itemQueue = self.__queue[itemFac]

            # getting the orders correct
            currentNext = current.getNext()
            while itemQueue <= currentQueue and currentNext is not None:  # going to the last part of the list
                current = currentNext
                currentQueue = self.__queue[currentFac]

            if currentQueue >= itemQueue:
                lNode = current
                rNode = currentNext

                # last object of the node
                if rNode is None:
                    self.__tail.setNext(item)
                    item.setPrev(self.__tail)
                    self.__tail = item
                else:
                    # connecting the references
                    item.setNext(rNode)
                    item.setPrev(lNode)

                    lNode.setNext(item)
                    rNode.setPrev(item)
            else:
                lNode = current.getPrev()
                rNode = current

                if lNode is None:
                    self.__head.setPrev(item)
                    item.setNext(self.__head)
                    self.__head = item
                else:
                    item.setNext(rNode)
                    item.setPrev(lNode)

                    lNode.setNext(item)
                    rNode.setPrev(item)

        self.__size += 1

    def dequeue(self):
        """dequeues and returns the highest priority student
            node from the front of the queue"""

        # checking if the queue is empty or not
        if self.isEmpty():
            print("Error: empty queue")

        current = self.__head
        currentNextNode = current.getNext()
        if currentNextNode is None:
            self.__head, self.__tail = None, None
        else:
            # detaching the reference with the node
            self.__head = currentNextNode
            self.__head.setPrev(None)

        self.__size -= 1

        return current

    def size(self):
        """Returns size of queue"""
        return self.__size

    def isEmpty(self):
        """returns true or false depending on the list is empty or not"""
        return self.__size == 0

    def __str__(self):
        """String representation of the table"""
        output = []
        current = self.__head
        # Traversing the queue
        while current is not None:
            output.append(str(current))
            current = current.getNext()

        display = "[{},\n]".join(output)
        return display


if __name__ == '__main__':
    text = "input.txt"
    filename = open(text)
    file = filename.read().split("\n")
    student = []
    waitlist = PriorityQueue()
    sciStudents = []

    for eachLine in file:
        studentInfo = eachLine.strip().split(' ')
        if len(studentInfo) == 4:  # 4 information in 1 node
            student.append(studentInfo)

    for eachStudent in student:
        if eachStudent[1] == "SCI":
            sciStudents.append(eachStudent)

    for student in sciStudents:
        studentNode = StudentNode(*student)
        waitlist.enqueue(studentNode)

    print(waitlist)
    print(waitlist.dequeue())
    "-----------------------"
    print(waitlist)
