'''This script scrapes a web page and goes to the next page till all pages are scraped
   and writes the data to a csv file'''

from bs4 import BeautifulSoup
import requests
import csv

current_page_url = "https://eci.gov.in/files/category/1359-general-election-2019/"
source = requests.get(current_page_url).text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'link'])

container = soup.find_all(class_="ipsType_break ipsContained")

# Get the next page url
def NextPageUrl(soup, current_page_url):
	next_page = soup.find_all(class_="ipsPagination_next") # Get the next page info
	next_page_url = next_page[0].a["href"] # Get url of the next page
	print(f'Current page url: {current_page_url}')
	print(f'Next page url:    {next_page_url}\n')
	
	if(next_page_url) and (next_page_url != current_page_url): # Check if next page exists
		source = requests.get(next_page_url).text
		soup = BeautifulSoup(source, 'lxml')
		container = soup.find_all(class_="ipsType_break ipsContained")
		current_page_url = next_page_url # Update current page url
		
		return current_page_url, container
	else:
		exit(0)


while(True):
	# Read each line in container and get the display text and the corresponding hyperlink
	for data in container:
		headline = data.a.text # Display text
		link = data.a["href"] # Hyperlink
		print(f'{headline}')
		print(f'{link}\n')
		csv_writer.writerow([headline, link]) # Write display text and link to csv file
	
	print(f'{type(container)}')
	print(f'{len(container)}\n')
	
	current_page_url, container = NextPageUrl(soup, current_page_url)

csv_file.close()

