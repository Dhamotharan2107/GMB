import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def scrape_gmb_details(url, worksheet):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Details
        business_name = soup.find(['div', 'h1'], {'class': ['PZPZlf ssJ7i B5dxMb','PZPZlf ssJ7i xgAzOe','lMbq3e']}).text.strip() if soup.find(['div','h1'],
                                                                                         {'class': ['PZPZlf ssJ7i B5dxMb' , 'PZPZlf ssJ7i xgAzOe', 'lMbq3e'] })  else ''
        address = soup.find(['span','div'], {'class': ['LrzXr', 'Io6YTe fontBodyMedium kR99db ']}).text.strip() if soup.find(['span','div'], {'class': ['LrzXr', 'Io6YTe fontBodyMedium kR99db ']}) else ''
        phone_number = soup.find(['span','div'], {'class' : ['LrzXr zdqRlf kno-fv', 'Io6YTe fontBodyMedium kR99db ']}).text.strip() if soup.find(['span','div'], {'class' : ['LrzXr zdqRlf kno-fv', 'Io6YTe fontBodyMedium kR99db ']}) else ''
        website = soup.find(['a','div'], {'class': ['mI8Pwc', 'Io6YTe fontBodyMedium kR99db ']})['href'] if soup.find(['a','div'], {'class': ['mI8Pwc', 'Io6YTe fontBodyMedium kR99db ']}) else ''

        # Find the next available row dynamically
        next_row = len(worksheet.get_all_values()) + 1

        # Define cell values
        worksheet.update(range_name='A1', values=[["BUSINESS NAME"]])
        worksheet.update(range_name='B1', values=[["ADDRESS"]])
        worksheet.update(range_name='C1', values=[["PHONE NUMBER"]])
        worksheet.update(range_name='D1', values=[["WEBSITE"]])

        worksheet.update(range_name=f'A{next_row}', values=[[business_name]])
        worksheet.update(range_name=f'B{next_row}', values=[[address]])
        worksheet.update(range_name=f'C{next_row}', values=[[phone_number]])
        worksheet.update(range_name=f'D{next_row}', values=[[website]])

        print(f"Data for {business_name} has been successfully updated in the Google Sheet.")

    else:
        print(f"Failed to fetch the page for {url}. Status code: {response.status_code}")

# Example usage
url = 'https://www.google.com/search?gs_ssp=eJzj4tVP1zc0TCuOj09PLsw2YLRSNagwTjQ1Mk1LTDEzT7RMNTIytjKoSLNMSTSxtDAzMUyyNE40t_ASKMgvyagsVkjOKMrPTS1ILQEAAPkWHg&q=pothys+chromepet&rlz=1C5CHFA_enIN1043IN1043&oq=pothys+chr&gs_lcrp=EgZjaHJvbWUqEwgCEC4YrwEYxwEYsQMYgAQYjgUyBggAEEUYOTIHCAEQABiABDITCAIQLhivARjHARixAxiABBiOBTIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIGCAYQRRg8MgYIBxBFGDzSAQg5MjMxajFqOagCALACAA&sourceid=chrome&ie=UTF-8'

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by title
sheet_title = 'Gmb-diggiplus'
worksheet = client.open(sheet_title).sheet1

# Call the function to update the Google Sheet
scrape_gmb_details(url, worksheet)
