# Sean Perez
# 28/09/2022
# For use by Phillipstown Community Centre and their Human Resources branch.

import csv
import sys
from datetime import datetime, timedelta


def get_date():
    """Checks the current date and subtracts 3, in case of holidays.
        :return string with last week's Monday and Friday"""
    now = datetime.now().date() - timedelta(days=3)

    # Creates and offset for when the sunday will be
    sun_offset = abs(now.weekday() - 6)

    # Calculates start of week and formats it correctly
    monday = str(now - timedelta(days=now.weekday()))
    monday = f"{monday[-2:]}/{monday[5:7]}/{monday[:4]}"

    # Calculates end of week and formats it correctly
    sunday = str(now + timedelta(days=sun_offset))
    sunday = f"{sunday[-2:]}/{sunday[5:7]}/{sunday[:4]}"
    return f"{monday} to {sunday}"


def convert_dates(str_date):
    """Takes string of date in 202212251037 and converts to 25/12/2022 10:37"""
    date = f"{str_date[6:8]}/{str_date[4:6]}/{str_date[0:4]} {str_date[-4:-2]}:{str_date[-2:]}"
    return date


def simple_date(str_date):
    """Similar to convert_date, but will just do the day and not the time"""
    date = f"{str_date[6:8]}/{str_date[4:6]}/{str_date[0:4]}"
    return date


def create_file(worker):
    """Creates new csv file and adds the required formats"""
    title = ['Timesheet', '', get_date()]
    header = ['Name', 'Start Time', 'Finish Time', 'Break', 'Total Time', 'Project', 'Sick', 'Annual', 'Public Holiday']

    # Total pay will be appended to this list and passed to the document.
    total_header = ['Total Sick (Paid)', 'Total Sick (Unpaid)', 'Total Annual (Paid)',
                    'Total Annual (Unpaid)', 'Total Public Holiday', 'Total pay per hour (STD)']
    now = datetime.now().date() - timedelta(days=3)
    monday = str(now - timedelta(days=now.weekday()))

    calculated_data = calculate_totals(worker)

    with open(f'Timesheet_week_of_{monday}.csv', 'w+', newline='') as fl:
        writer = csv.writer(fl)

        # write the header
        writer.writerow(title)
        writer.writerow('')

        # Loops through names
        for i in calculated_data:
            writer.writerow([i])

            # Loops through dates & totals
            for j in calculated_data[i]:

                if j != 'total':
                    writer.writerow([f"Date: {simple_date(j)}"])
                    writer.writerow(header)

                    if isinstance(calculated_data[i][j], list):
                        # Loops through shifts
                        for k in range(len(calculated_data[i][j])):
                            test = calculated_data[i][j][k]
                            writer.writerow(calculated_data[i][j][k])
                    else:
                        writer.writerow(calculated_data[i][j])
                else:
                    writer.writerow(total_header)
                    writer.writerow(calculated_data[i]['total'])
                    writer.writerow('')
                    break
        return


# Validates file name input
def file_read_val():
    if len(sys.argv) <= 1:
        return False

    if ".csv" not in " ".join(sys.argv[1:]):
        return False
    return True


def list_to_dict(list_to_dic, reader) -> dict:
    # For every row, as long as there is a valid email with the at sign,
    # it will use that as key to create a list or append to existing list
    for row in reader:
        if "@" in row[-3]:
            try:
                list_to_dic[row[-3].strip('"')].append([s.strip('"') if s != '' else 0 for s in row])
            except KeyError:
                list_to_dic[row[-3].strip('"')] = []
                list_to_dic[row[-3].strip('"')].append([s.strip('"') if s != '' else 0 for s in row])

    return list_to_dic


def one_day_dic(email_dic, day_flag=True):
    """Creates a dictionary for a one shift/row"""
    # email_dic contents
    # [Name-0, Start-1, Finish-2, Break-3, Total(min)-4, Project-5, Sick-6, Annual-7,
    # Public-8, email-9, start_num-10, finish_num-11]
    proj = 'No Project' if email_dic[5] == 0 else email_dic[5]
    day_list = [
        [
            email_dic[0],
            convert_dates(email_dic[10]),
            convert_dates(email_dic[11]),
            int(email_dic[3]) / 60,
            int(email_dic[4]) / 60,
            proj,
            email_dic[6],
            email_dic[7],
            email_dic[8]
        ]
    ]

    if day_flag:
        # sick
        totals_list = []
        match email_dic[6]:

            case 'Paid':
                totals_list.append(int(email_dic[4]) / 60)
                totals_list.append(0)

            case 'Unpaid':
                totals_list.append(0)
                totals_list.append(int(email_dic[4]) / 60)

            case _:
                totals_list.append(0)
                totals_list.append(0)

        # annual
        match email_dic[7]:

            case 'Paid':
                totals_list.append(int(email_dic[4]) / 60)
                totals_list.append(0)

            case 'Unpaid':
                totals_list.append(0)
                totals_list.append(int(email_dic[4]) / 60)

            case _:
                totals_list.append(0)
                totals_list.append(0)

        # public holiday
        if email_dic[8] == "Yes":
            totals_list.append(int(email_dic[4]) / 60)
        else:
            totals_list.append(0)

        # Total hours
        count = int(email_dic[4]) / 60
        for num in totals_list:
            count = count - num

        totals_list.append(count)

        day_list.append(totals_list)
        return day_list

    return day_list[0]


def calculate_totals(email_dic):
    """loops through every user, figures out what each row will be"""

    formatted_data = {}

    for key in email_dic:

        # to create the list of totals at the end
        total_sick_paid = 0
        total_sick_unpaid = 0
        total_annual_paid = 0
        total_annual_unpaid = 0
        total_public_holiday = 0
        total_total = 0

        for i in range(len(email_dic[key])):

            # If there is a date with a list, it appends the next row
            try:
                formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]].append(
                    one_day_dic(email_dic[key][i], False))
            except KeyError:

                # If not, it first checks to see if there is a dictionary for the date
                try:
                    isinstance(formatted_data[email_dic[key][i][9]], dict)

                    # If there is a dictionary for the person
                    try:
                        formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]]
                        formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]].append(
                            one_day_dic(email_dic[key][i], False))

                    # Creates a list for the date
                    except KeyError:
                        formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]] = []
                        formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]].append(
                            one_day_dic(email_dic[key][i], False))

                # creates a dictionary with the first entry and a list for its value
                except KeyError:
                    formatted_data[email_dic[key][i][9]] = {email_dic[key][i][10][:8]: []}
                    formatted_data[email_dic[key][i][9]][email_dic[key][i][10][:8]].append(
                        one_day_dic(email_dic[key][i], False))

            # Calculates the totals and keeps track in their variables
            row_list = email_dic[key][i]
            total_hour = int(row_list[4]) / 60
            match row_list[6]:

                case 'Paid':
                    total_sick_paid += total_hour
                case 'Unpaid':
                    total_sick_unpaid += total_hour

            # annual
            match row_list[7]:
                case 'Paid':
                    total_annual_paid += total_hour
                case 'Unpaid':
                    total_annual_unpaid += total_hour

            # public holiday
            if row_list[8] == "Yes":
                total_public_holiday += total_hour

            total_total += total_hour

        # creates a new entry in dic along with the dates called totals with a list of totals
        totals_list = [
            total_sick_paid,
            total_sick_unpaid,
            total_annual_paid,
            total_annual_unpaid,
            total_public_holiday,
            total_total - total_sick_paid - total_sick_unpaid -
            total_annual_paid - total_annual_unpaid - total_public_holiday
        ]

        formatted_data[email_dic[key][i][9]]['total'] = totals_list

    return formatted_data


# Total times is in minutes; convert to hours in float so that you get percentages of the hours in decimal form
def import_csv():
    """Import the file from the path"""
    # Checks to see if file was added and if it has the file type in the name
    if not file_read_val():
        error_msg = "No file name or file type '.csv' was provided, " \
                    "please try again by writing: python main.py NAME-OF-FILE.csv"
        print(error_msg)
        return

    # Creates the path that the new csv file will be created in the root directory (where the py file is located)
    read_path = " ".join(sys.argv[1:])

    with open(f'{read_path}', newline='') as csv_file:
        reader = list(csv.reader(csv_file, quotechar='|'))

        email_dic = list_to_dict({}, reader)

        return email_dic


if __name__ == "__main__":
    create_file(import_csv())
