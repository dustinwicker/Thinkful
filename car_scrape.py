import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Increase maximum width in characters of columns - will put all columns in same line in console readout
pd.set_option('expand_frame_repr', False)
# Be able to read entire value in each column (no longer truncating values)
pd.set_option('display.max_colwidth', -1)
# Increase number of rows printed out in console
pd.set_option('display.max_rows', 200)

# Webdriver options
options = Options()
# # Make call to Chrome
# options.add_argument('--headless')
# Define Chrome webdriver for site
driver = webdriver.Chrome(options=options)
# Define url
url = "https://www.ford.com/cars/mustang/models/"
# Supply url
driver.get(url=url)

### In Chrome, to find the necessary information click:
### In the upper right hand corner, click the 3 vertical dots -> More Tools -> Developer Tools
### Then in the upper left hand corner, click the square with a pointer in it icon to be able to hover over objects
### on the website and see their information

# Obtain vehicle information for each of the displayed Mustangs
cars = driver.find_elements(by='xpath', value="//div[@class='vehicleTile section']")
# Observe the web elements obtained
cars

# Lets observe the first car
first_car = cars[0].text
# Print first_car
first_car
# Print type of first_car
type(first_car)
# Lets split on the new line (\n) since it separates the various pieces of information of interest
first_car = first_car.split("\n")
# Print type
type(first_car)

# Lets get all of our desired information from the first car - year, car model, price, city mpg, hwy mpg, lease/mo

# year
first_car[0][0:4]

# car model
first_car[0][4:].strip()

# Locate the position of the '$'
first_car[1].index('$')
# Use the position of the $ to find the full price
first_car[1][first_car[1].index('$'): first_car[1].index('$')+7]
# Remove the $ and , so we can get the integer value
# price
first_car[1][first_car[1].index('$'): first_car[1].index('$')+7].replace("$", "").replace(",", "")

# city mpg
first_car[2].split("/")[0].split('MPG')[1].strip()[0:2]

# hwy mpg
first_car[2].split("/")[1].strip().split('HWY')[0].strip()

# Locate the position of the '$' and use the position of the $ to find the lease/mo amount
first_car[3][first_car[3].index('$'):first_car[3].index('$')+4]
# Remove the $ so we can get the integer value
# lease/mo
first_car[3][first_car[3].index('$'):first_car[3].index('$')+4].replace("$", "")

# Lets apply the above methodologies to all cars extracted from the website to get their specific information
# Use an empty list to capture the results
car_results_list = []
for i in range(len(cars)):
    # Use this list to capture the results of each car. After each for loop run, we append these results to our other
    # 'main' list (car_results_list)
    specific_car_info_list = []
    car = cars[i].text.split("\n")
    # year
    specific_car_info_list.extend([car[0][0:4]])
    # car model
    specific_car_info_list.extend([car[0][4:].strip()])
    # price
    specific_car_info_list.extend([car[1][car[1].index('$'): car[1].index('$') + 7].replace("$", "").replace(",", "")])
    # The following try/except blocks allow us to check if that car listing has the information we want to capture.
    # If it does not (i.e., we hit the except part, we extend an nan onto that car's specific information list)
    try:
        specific_car_info_list.extend([car[2].split("/")[0].split('MPG')[1].strip()[0:2]])  # city mpg
    except IndexError:
        print('No city mpg for this vehicle.')
        specific_car_info_list.extend([np.nan])
    try:
        specific_car_info_list.extend([car[2].split("/")[1].strip().split('HWY')[0].strip()])  # hwy mpg
    except:
        print('No hwy mpg for this vehicle.')
        specific_car_info_list.extend([np.nan])
    try:
        specific_car_info_list.extend([car[3][car[3].index('$'):car[3].index('$') + 4].replace("$", "")])  # lease/mo
    except:
        print('No lease/mo for this vehicle.')
        specific_car_info_list.extend([np.nan])
    car_results_list.append(specific_car_info_list)

# Now we have a list of lists - each specific list contains information for one car
car_results_list
# Notice the first element in the list corresponds to the first car
car_results_list[0]

# Convert list of lists to DataFrame
cars_df = pd.DataFrame(data=car_results_list, columns=['year', 'car_name', 'price', 'city_mpg', 'hwy_mpg', 'lease_mo'])
cars_df

# Remove all non-ASCII characters to make string easier to work with
# Dictionary to detect non-ASCII characters
find = dict.fromkeys(range(128), '')
# Get a list of all non-ascii characters in car_name column
non_ascii_characters_list = []
for car in cars_df['car_name']:
    for letter in list(car):
        if letter.translate(find):
            if letter.translate(find) not in non_ascii_characters_list:
                non_ascii_characters_list.append(letter.translate(find))
for symbol in non_ascii_characters_list:
    for index, value in enumerate(cars_df['car_name']):
        cars_df.loc[index]['car_name'] = cars_df.loc[index]['car_name'].replace(symbol, '')

print(cars_df)