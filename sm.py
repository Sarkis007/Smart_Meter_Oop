import datetime

class Meassurment:
    def __init__(self, utility, place, date, read):
        self.utility = utility
        self.place = place
        self.date = date
        self.read = read
        if utility == 'Gas' or utility == 'Water':
            self.unit = u'm\u00b3'
        elif utility == 'Electricity':
            self.unit = 'Kwh'


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Sm:

    def __init__(self):
        self.__head = None

    def date_input(self, sentence):
        now = datetime.datetime.now()
        date = raw_input(sentence)
        if date == 'today':
            date = str(now.strftime("%Y-%m-%d"))
            return date
        else:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                return date
            except ValueError:
                print "Invalid input"
                x = self.date_input("The date should be as 'year-mm-dd'")
                return x

    def input(self,x,y,z):
        tmp = raw_input("1 - " + x + "2 - " + y + "3 - "+z)
        while True:
            if tmp == "1":
                return x
            elif tmp == "2":
                return y
            elif tmp == "3":
                return z
            else:
                tmp = raw_input ("please enter 1, 2 or 3")

    def read_input(self,utility,date,place):
        while True:
            try:
                read = input('please enter meter read for ' + utility + " on " + date + " for " + place)
                if len(str(read)) <= 5:
                    return read
                else:
                    print "the length should not be more than 5 numbers, please try again"
            except NameError:
                print "Invalid input, your input should be only numbers"


    def sorted_insert(self, measurement):
        new_measurement = Node(measurement)
        if self.__head is None:
            self.__head = new_measurement
        else:
            temp = self.__head
            while temp.next is not None and temp.next.data.read < new_measurement.data.read:
                temp = temp.next
                new_measurement.next = temp.next
            temp.next = new_measurement

    def add_measurement(self):
        date = self.date_input("please insert the date as year-mm-dd or just type 'today' ")
        print "Please select the utility type you want to add"
        utility = self.input("Electricity", "Water", "Gas")
        print "Please select for which place you want to add a new measurement "
        place = self.input("Home", "Work", "Other")
        read = self.read_input(utility,date,place)
        measurement = Meassurment(utility,place,date,read)
        self.sorted_insert(measurement)
        print "Measurement added successfully"
        return

    def checkifexist(self,utility, place):
        x = False
        y = False
        temp = self.__head
        while temp is not None:
            if temp.data.utility == utility:
                x = True
            if temp.data.place == place:
                y = True
            temp = temp.next
        if y == True and x == True:
            return True
        else:
            return False


    def display(self):
        print "please select one of the following places"
        place = self.input("Home", "Work", "Other")
        print "Please select one of the following utilities"
        utility = self.input("Electricity", "Water", "Gas")
        tmp = self.__head
        check = self.checkifexist(utility,place)
        if check == True:
            print "Saved data for " + utility + " utility for",place ,"are the following:"
            n = 1
            while tmp is not None and tmp.data.utility == utility and tmp.data.place == place:
                print str(n) + '- On date: ' + tmp.data.date + '  - reading: ' + str(tmp.data.read) + ' ' + str(tmp.data.unit)
                tmp = tmp.next
                n = n + 1
        else:
            print "There are no readings for", utility, "utility for", place, "to edit"
            return
        return

    def usage_check(self):
        print "Please select for which place you want to check your usage"
        return

    def start_sm(self):
        while True:
            print "1- Add a new measurement"
            print "2- Check your usage"
            print "3- Edit the data"
            print "4- Exit"
            x = raw_input()
            if x == '1':
                self.add_measurement()
            elif x == '2':
                self.usage_check()
            elif x == '3':
                self.edit_data()
            elif x == '4':
                print "Thank you sir"
                print "Have a nice day"
                exit()
            else:
                print "invalid input, please enter 1 or 2 or 3"
            print "Please choose other operation or enter 4 to exit"


def main():
    my_sm = Sm()
    measurement1 = Meassurment("Electricity", "Home", "12-12-12", "22222")
    measurement2 = Meassurment("Electricity", "Home", "12-12-12", "11111")
    measurement3 = Meassurment("Electricity", "Home", "12-12-12", "33333")
    my_sm.sorted_insert(measurement1)
    my_sm.sorted_insert(measurement2)
    my_sm.sorted_insert(measurement3)
    my_sm.start_sm()



main()