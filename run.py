# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data form the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter data string here: ") 
        sales_data = data_str.split(",")
    
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into intergers.
    Raise ValueError if strings can not be converted to int,
    or if they aren't exactly 6 values.
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"exactly 6 values required; you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again\n")
        return False
    return True
#Commented out REPETITIVE! code USE the code BELOW! for the same purpose
#def update_sales_worksheet(data):
#    """
 #   Update sales worksheet row with the data provided.
#     """  
#
#    print("Update sales worksheet...\n")
#    sales_worksheet = SHEET.worksheet("sales")
#    sales_worksheet.append_row(data) 
 #   print("Sales worksheet updated successfully.\n")

#def update_surplus_worksheet(data):
#    """
#    Update surplus worksheet row with the data provided.
#    """  
#    print("Update surplus worksheet...\n")
#    surplus_worksheet = SHEET.worksheet("surplus")
#    surplus_worksheet.append_row(data) 
#    print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Receive list of intergers to insert into worksheet
    Update the revelant worksheet with the data provided
    """
    print(f"Update {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} have been updated successfully\n")



def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock runs out
    """

    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collect columns of data from worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """

    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns



def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to Love Sandwich Data Automation")
#main()
sales_columns = get_last_5_entries_sales()