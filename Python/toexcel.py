from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML content from a local file
with open('C:\\Users\\QQ\\Desktop\\Python\\ad_account.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a list to store the extracted data
data = []

# Find all rows in the table body
rows = soup.find_all('div', class_='f742b')
for row in rows:
    # Extract status
    status_div = row.find('div', id='td-adaccount-account_status')
    if not status_div:
        continue  # Skip rows that do not have the expected structure
    status = status_div.find('div', class_='text-nowrap').text.strip()
    
    # Extract account name and ID
    account_div = row.find('div', id='td-adaccount-account')
    if not account_div:
        continue  # Skip rows that do not have the expected structure
    account_name = account_div.find('span', class_='text-semibold hover-underline').text.strip()
    account_id = account_div.find('span', class_='text-12').text.strip().split(': ')[1]
    
    # Extract spending cap details
    spend_cap_div = row.find('div', id='td-adaccount-spend_cap')
    if not spend_cap_div or 'data-tooltip' not in spend_cap_div.attrs:
        continue  # Skip rows that do not have the expected structure
    tooltip_text = spend_cap_div['data-tooltip']
    spent_str, limit_str = tooltip_text.split(' / ')
    spent = float(spent_str.replace(',', ''))  # Handle comma in numbers like "0,01"
    limit = float(limit_str)
    progress_bar = spend_cap_div.find('progress')['value']
    percentage = float(progress_bar)
    
    # Append the extracted data to the list
    data.append({
        'Status': status,
        'Account Name': account_name,
        'Account ID': account_id,
        'Spent': spent,
        'Limit': limit,
        'Percentage': percentage
    })

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = 'C:\\Users\\QQ\\Desktop\\Python\\ad_accounts.xlsx'
df.to_excel(output_file, index=False)

print(f'Data has been saved to {output_file}')



