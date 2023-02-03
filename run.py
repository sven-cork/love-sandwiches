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
    
def update_sales_worksheet(data):
    """
    Add new row with the sales data to sales worksheet.
    """

    print("Updating sales worksheet\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updates successfully.\n")

def calculate_surplus_data(sales_row):

    print("Calculating surplus data.\n")
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(stock)
    stock_row = stock[-1]
    print(stock_row) 

def main():
    '''
    Run all program function
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

main()