import gspread	
from google.oauth2.service_account import Credentials	
from pprint import pprint

SCOPE = [	
    "https://www.googleapis.com/auth/spreadsheets",	
    "https://www.googleapis.com/auth/drive.file",	
    "https://www.googleapis.com/auth/drive"	
    ]	

CREDS = Credentials.from_service_account_file('creds.json')	
SCOPED_CREDS = CREDS.with_scopes(SCOPE)	
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)	
SHEET = GSPREAD_CLIENT.open('love_sandwiches')	

def get_sales_data():
    """
    Get sales figure input from user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 15, 30, 45, 60, 75\n")
        
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

def validate_data(values):
    """
    Converts all strings to integers.
    Raises ValueError if strings cannot be converted.
    """
    try: 
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def calculate_surplus_data(sales_row):

    print("Calculating surplus data.\n")
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(stock)
    stock_row = stock[-1]
    print(stock_row) 

    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def update_worksheet(data, worksheet):
    """
    Refactoring of functions 'update_surplus_worksheet(surplus_data)' and 'update_sales_worksheet(data)'.
    """
    print(f"Updating {worksheet} worksheet")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print("Surplus worksheet updated successfully.\n")

def get_last_5_entries_sales():
    """

    """
    sales = SHEET.worksheet("sales")
    column = sales.col_values(3)
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate average stock data based on last 5 days sale adding 10%.
    """
    print("Calculate stock data\n")

    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

def main():
    '''
    Run all program function
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(sales_data, "sales")
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    print(stock_data)
    

main()