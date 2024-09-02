# %%
print("Helloo")

# %%
from bs4 import BeautifulSoup
import requests

# %%
url ='https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html')

# %%
print(soup)

# %%
soup.find('table')

# %%
table =soup.find_all('table')[1]
print(table)

# %%
world_title=table.find_all('th')
world_title

# %%
world_table_titles = [title.text for title in world_title]
world_table_titles

# %%
world_table_title = [ title.text.strip() for title in world_title]
print(world_table_title)

# %%
import pandas as pd
df = pd.DataFrame(columns= world_table_title)
df

# %%
column_data=table.find_all('tr')
for row in column_data[1:]:
    row_data= row.find_all('td')
    individual_row_data=[data.text.strip() for data in row_data]
    # print(individual_row_data)

    lenght = len(df)
    df.loc[lenght] = individual_row_data


# %%
df

# %%
df.to_excel(r'D:\Programming\IRS design\webScrapping\Companies.xlsx')


