import datetime


class Meassurment(object):
    def __init__(self, place, date, read):
        self.place = place
        self.date = date
        self.read = read
        self.price = None
        self.unit = None
        self.utility = None
        self.next = None

    def getprice(self, data1, data2):
            if data1.date > data2.date and data1.read > data2.read or data1.date < data2.date and data1.read \
                    < data2.read:
                used_amount = abs(int(data1.read - data2.read))
                from datetime import datetime
                date_format = "%Y-%m-%d"
                a = datetime.strptime(data1.date, date_format)
                b = datetime.strptime(data2.date, date_format)
                delta = abs(b - a)
                used_days = delta.days
                cost = used_amount * self.price
                print "The amount of", self.utility, "used in", used_days, "days is", \
                    used_amount, self.unit
                print "which's cost for", used_days, "days is", cost, "Drams"
                if used_days > 30:
                    print "Approximately", int((30 * cost) / used_days), "Drams per month"
                else:
                    print "Approximately", int(cost / used_days), "Drams per Day"
            else:
                print data1.date + '  -  ', data1.read
                print data2.date + '  -  ', data2.read
                if data1.date > data2.date:
                    print "the usage for " + data2.date + " is bigger than the usage of " + data1.date
                    print "which makes no sense, please check the readings for the dates"
                if data1.date < data2.date:
                    print "the usage for " + data1.date + " is bigger than the usage of " + data2.date
                    print "which makes no sense, please check the readings for the dates"
                print "if you want to do other operations select one or exit"
                return


class Gas(Meassurment):
    def __init__(self, place, date, read):
        Meassurment.__init__(self, place, date, read)

        self.price = 72
        self.unit = u'm\u00b3'
        self.utility = "Gas"
        self.lenght = None

    def changep(self):
        self.price = 2222222
        return


class Water(Meassurment):
    def __init__(self, place, date, read):
        Meassurment.__init__(self, place, date, read)
        self.price = 194.3
        self.unit = u'm\u00b3'
        self.utility = "Water"


class Electricity(Meassurment):
    def __init__(self, place, date, read):
        Meassurment.__init__(self,  place, date, read)
        self.price = 21.3
        self.unit = 'Kwh'
        self.utility = "Electricity"


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

    def usage_check(self, utility, place):
        data_len = self.data_lenght(utility, place)
        if data_len >= 2:
            self.display(utility, place)
            print "Enter any two dates to calculate the usage"
            date1 = self.date_input("please enter the first date as 'year-mm-dd'")
            data1 = self.find_data(utility, place, date1)
            date2 = self.date_input("please enter the second date as 'year-mm-dd'")
            data2 = self.find_data(utility, place, date2)
            data2.getprice(data1, data2)
        else:
            print "There are ", data_len, " reading" + " for ", utility, " utility"
            print "There should be at least two readings"
            return
        return

    def input(self, x, y, z):
        tmp = raw_input("1 - " + x + '\n' + "2 - " + y + '\n' + "3 - "+z)
        while True:
            if tmp == "1":
                return x
            elif tmp == "2":
                return y
            elif tmp == "3":
                return z
            else:
                tmp = raw_input("please enter 1, 2 or 3")

    def data_lenght(self, utility, place):
        n = 0
        temp = self.__head
        while temp is not None:
            if temp.utility == utility and temp.place == place:
                n += 1
            temp = temp.next
        return n

    def read_input(self, utility, date, place):
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
        if self.__head is None:
            self.__head = measurement

        else:
            temp = self.__head
            while temp.next is not None:
                temp = temp.next
            temp.next = measurement

    def add_measurement(self, utility, place):
        date = self.date_input("please insert the date as year-mm-dd or just type 'today' ")
        read = self.read_input(utility, date, place)
        if utility == "Gas":
            measurement = Gas(place, date, read)
        elif utility == "Water":
            measurement = Water(place, date, read)
        else:
            measurement = Electricity(place, date, read)
        self.sorted_insert(measurement)
        print "Measurement added successfully"
        return

    def check_if_exist(self, utility, place, date):
        x = False
        temp = self.__head
        while temp is not None:
            if temp.utility == utility and temp.place == place and (temp.date == date or date is True):
                x = True
            temp = temp.next
        return x

    def display(self, utility, place):
        tmp = self.__head
        check = self.check_if_exist(utility, place, True)
        if check is True:
            print "Saved data for " + utility + " utility for", place, "are the following:"
            n = 1
            while tmp is not None:
                if tmp.utility == utility and tmp.place == place:
                    print str(n) + '- On date: ' + tmp.date + '  - reading: ' + str(tmp.read), tmp.unit
                    n = n + 1
                tmp = tmp.next

        else:
            print "There are no readings for", utility, "utility for", place, "to edit"
            self.start_sm()
        return place, utility

    def change_data(self, utility, date, place):
        new_read = self.read_input(utility, date, place)
        temp = self.__head
        while temp is not None and temp.date != date:
            temp = temp.next
        temp.read = new_read

    def delete_data(self, date):
        temp = self.__head
        if temp.date == date:
            self.__head = temp.next
        else:
            while temp is not None and temp.next.date != date:
                temp = temp.next
            temp.next = temp.next.next

    def edit_data(self, utility, place):
        self.display(utility, place)
        date = self.date_input("please select one of the dates above to edit")
        check = self.check_if_exist(utility, place, date)
        while check is False:
            date = self.date_input("The date you entered is not in the data, please enter other date ")
            check = self.check_if_exist(utility, place, date)
        x = raw_input("Do you want to delete it or change it ?")
        while True:
            if x == 'change':
                self.change_data(utility, date, place)
                print "Measurement changed successfully"
                break
            elif x == 'delete':
                self.delete_data(date)
                print "Measurement deleted successfully"
                break
            else:
                x = raw_input("Invalid input, please enter 'edit' or 'delete'")

    def find_data(self, utility, place, date):
        check = self.check_if_exist(utility, place, date)
        while check is False:
            date = self.date_input("The date you entered is not in the data, please enter other date ")
            check = self.check_if_exist(utility, place, date)
        temp = self.__head
        while temp is not None:
            if temp.date == date and temp.place == place and temp.utility == utility:
                return temp
            temp = temp.next

    def start_sm(self):
        while True:
            print "1- Add a new measurement"
            print "2- Check your usage"
            print "3- Edit the data"
            print "4- Display data"
            print "5- Exit"
            x = raw_input()
            utility = ""
            place = ""
            if x == "1" or x == "2" or x == "3" or x == "4":
                print "please select one of the following utilities"
                utility = self.input("Electricity", "Water", "Gas")
                print "please select one of the following places"
                place = self.input("Home", "Work", "Other")
            if x == '1':
                self.add_measurement(utility, place)
            elif x == '2':
                self.usage_check(utility, place)
            elif x == '3':
                self.edit_data(utility, place)
            elif x == '4':
                self.display(utility, place)
            elif x == '5':
                print "Thank you sir"
                print "Have a nice day"
                exit()
            else:
                print "invalid input, please enter 1, 2, 3, 4 or 5"
            print "Please choose other operation or enter 5 to exit"


def main():
    my_sm = Sm()
    measurement1 = Water("Home", "1999-12-12", 11111)
    measurement2 = Gas("Home", "2012-12-12", 26444)
    measurement3 = Water("Work", "2013-12-12", 33333)
    measurement4 = Electricity("Other", "2013-12-12", 44444)
    measurement5 = Gas("Home", "2013-12-12", 22222)

    my_sm.sorted_insert(measurement1)
    my_sm.sorted_insert(measurement2)
    my_sm.sorted_insert(measurement3)
    my_sm.sorted_insert(measurement4)
    my_sm.sorted_insert(measurement5)
    my_sm.start_sm()


main()
