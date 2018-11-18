import datetime


class Meassurment:
    def __init__(self, utility, place, date, read):
        self.utility = utility
        self.place = place
        self.date = date
        self.read = read


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Sm:

    def __init__(self):
        self.__head = None
        self.__GPM = 72
        self.__WPM = 194.3
        self.__EPK = 21.32

    def utility_price(self, utility):
        if utility == 'Gas':
            return self.__GPM
        elif utility == 'Water':
            return self.__WPM
        elif utility == 'Electricity':
            return self.__EPK

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
            if temp.data.utility == utility and temp.data.place == place:
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
        new_measurement = Node(measurement)
        if self.__head is None:
            self.__head = new_measurement
        else:
            temp = self.__head
            while temp.next is not None and temp.next.data.read < new_measurement.data.read:
                temp = temp.next
                new_measurement.next = temp.next
            temp.next = new_measurement

    def add_measurement(self, utility, place):
        date = self.date_input("please insert the date as year-mm-dd or just type 'today' ")
        read = self.read_input(utility, date, place)
        measurement = Meassurment(utility, place, date, read)
        self.sorted_insert(measurement)
        print "Measurement added successfully"
        return

    def check_if_exist(self, utility, place, date):
        x = False
        temp = self.__head
        while temp is not None:
            if temp.data.utility == utility and temp.data.place == place and (temp.data.date == date or date is True):
                x = True
            temp = temp.next
        return x

    def utility_unit(self, utility):
        if utility == 'Gas' or utility == 'Water':
            return u'm\u00b3'
        elif utility == 'Electricity':
            return 'Kwh'

    def display(self, utility, place):
        tmp = self.__head
        check = self.check_if_exist(utility, place, True)
        if check is True:
            print "Saved data for " + utility + " utility for", place, "are the following:"
            n = 1
            while tmp is not None:
                if tmp.data.utility == utility and tmp.data.place == place:
                    print str(n) + '- On date: ' + tmp.data.date + '  - reading: ' + str(tmp.data.read),\
                        self.utility_unit(utility)
                    n = n + 1
                tmp = tmp.next

        else:
            print "There are no readings for", utility, "utility for", place, "to edit"
            self.start_sm()
        return place, utility

    def change_data(self, utility, date, place):
        new_read = self.read_input(utility, date, place)
        temp = self.__head
        while temp is not None and temp.data.date != date:
            temp = temp.next
        temp.data.read = new_read

    def delete_data(self, date):
        temp = self.__head
        if temp.data.date == date:
            self.__head = temp.next
        else:
            while temp is not None and temp.next.data.date != date:
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
            if temp.data.date == date and temp.data.place == place and temp.data.utility == utility:
                return temp.data.date, temp.data.read
            temp = temp.next

    def usage_check(self, utility, place):
        len = self.data_lenght(utility, place)
        if len >= 2:
            self.display(utility, place)
            print "Enter any two dates to calculate the usage"
            date1 = self.date_input("please enter the first date as 'year-mm-dd'")
            first_date, first_read = self.find_data(utility, place, date1)
            date2 = self.date_input("please enter the second date as 'year-mm-dd'")
            second_date, second_read = self.find_data(utility, place, date2)
            if first_date > second_date and first_read > second_read or first_date < second_date and first_read \
                    < second_read:
                used_amount = abs(int(first_read - second_read))
                from datetime import datetime
                date_format = "%Y-%m-%d"
                a = datetime.strptime(first_date, date_format)
                b = datetime.strptime(second_date, date_format)
                delta = abs(b - a)
                used_days = delta.days
                cost = used_amount * self.utility_price(utility)
                print "The amount of", utility, "used in", used_days, "days is", \
                    used_amount, self.utility_unit(utility)
                print "which's cost for", used_days, "days is", cost, "Drams"
                if used_days > 30:
                    print "Approximately", int((30 * cost) / used_days), "Drams per month"
                else:
                    print "Approximately", int(cost / used_days), "Drams per Day"
            else:
                print first_date + '  -  ', first_read
                print second_date + '  -  ', second_read
                if first_date > second_date:
                    print "the usage for " + second_date + " is bigger than the usage of " + first_date
                    print "which makes no sense, please check the readings for the dates"
                if first_date < second_date:
                    print "the usage for " + first_date + " is bigger than the usage of " + second_date
                    print "which makes no sense, please check the readings for the dates"
                print "if you want to do other operations select one or exit"
                return
        else:
            print "There are ", len, " reading" + " for " + utility + " utility"
            print "There should be at least two readings"
            return
        return

    def change_cost(self,utility):
        if utility == "Gas":
            print "Current price for each meter cube is ", self.__GPM
        elif utility == "Electricity":
            print "Current price for each kilo Watt per hour is", self.__EPK
        else:
            print "Current price for each meter cube is ", self.__WPM
        while True:
            try:
                x = input("Please enter new cost for " + utility)
                if utility == "Gas":
                    self.__GPM = x
                    return
                elif utility == "Electricity":
                    self.__EPK = x
                    return
                else:
                    self.__WPM = x
                    return
            except:
                print "Invalid Input, please enter integers"

    def start_sm(self):
        while True:
            print "1- Add a new measurement"
            print "2- Check your usage"
            print "3- Edit the data"
            print "4- Display data"
            print "5- Change utility costs"
            print "6- Exit"
            x = raw_input()
            if x == "1" or x == "2" or x == "3" or x == "4":
                print "please select one of the following utilities"
                utility = self.input("Electricity", "Water", "Gas")
                print "please select one of the following places"
                place = self.input("Home", "Work", "Other")
            if x == '1':
                self.add_measurement(utility ,place)
            elif x == '2':
                self.usage_check(utility, place)
            elif x == '3':
                self.edit_data(utility, place)
            elif x == '4':
                self.display(utility, place)
            elif x == '5':
                print "please select one of the following utilities"
                utility = self.input("Electricity", "Water", "Gas")
                self.change_cost(utility)
            elif x == '6':
                print "Thank you sir"
                print "Have a nice day"
                exit()
            else:
                print "invalid input, please enter 1, 2, 3, 4 or 5"
            print "Please choose other operation or enter 5 to exit"


def main():
    my_sm = Sm()
    measurement1 = Meassurment("Water", "Home", "1999-12-12", 11111)
    measurement2 = Meassurment("d", "Home", "2012-12-12", 26444)
    measurement3 = Meassurment("Water", "Work", "2013-12-12", 33333)
    measurement4 = Meassurment("Electricity", "Other", "2013-12-12", 44444)
    measurement5 = Meassurment("Gas", "Home", "2013-12-12", 55555)

    my_sm.sorted_insert(measurement1)
    my_sm.sorted_insert(measurement2)
    my_sm.sorted_insert(measurement3)
    my_sm.sorted_insert(measurement4)
    my_sm.sorted_insert(measurement5)
    my_sm.start_sm()


main()
