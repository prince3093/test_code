from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
import pandas as pd


def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

def which_digit(html):
    mappingDict={'icon-ji':9,
                'icon-dc':'+',
                'icon-fe':'(',
                'icon-hg':')',
                'icon-ba':'-',
                'icon-lk':8,
                'icon-nm':7,
                'icon-po':6,
                'icon-rq':5,
                'icon-ts':4,
                'icon-vu':3,
                'icon-wx':2,
                'icon-yz':1,
                'icon-acb':0,
                }
    return mappingDict.get(html,'')

def get_phone_number(body):
    i=0
    phoneNo = "0000000000"
    try:
            
        for item in body.find('p',{'class':'contact-info'}):
            i+=1
            if(i==2):
                phoneNo=''
                try:
                    for element in item.find_all(class_=True):
                        classes = []
                        classes.extend(element["class"])
                        phoneNo+=str((which_digit(classes[1])))
                except:
                    pass
    except:
        pass
    body = body['data-href']
    soup = BeautifulSoup(body, 'html.parser')
    for a in soup.find_all('a', {"id":"whatsapptriggeer"} ):
        phoneNo = str(a['href'][-10:])


    return phoneNo


def get_rating(body):
	rating = 0.0
	text = body.find('span', {'class':'star_m'})
	if text is not None:
		for item in text:
			rating += float(item['class'][0][1:])/10
            
	return rating

def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

page_number = 1
service_count = 1

fields = ['Name', 'Phone', 'Rating', 'Address']
out_file = open('pharma.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

while True:
	# Check if reached end of result
	if page_number > 50:
		break

	url="https://www.justdial.com/Visakhapatnam/Pharmacies/page-%s" % (page_number)
	print(url)
	req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
	page = urllib.request.urlopen( req )

	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})

	# Iterate through the 10 results in the page
	for service_html in services:

		# Parse HTML to fetch data     
		dict_service = {}
		name = get_name(service_html)
		phone = get_phone_number(service_html)
		rating = get_rating(service_html)
		address = get_address(service_html)
		if name != None:
			dict_service['Name'] = name
		if phone != None:
			dict_service['Phone'] = phone
		if rating != None:
			dict_service['Rating'] = rating
		if address != None:
			dict_service['Address'] = address

		# Write row to CSV
		csvwriter.writerow(dict_service)

		print("#" + str(service_count) + " " , dict_service)
		service_count += 1

	page_number += 1

out_file.close()

# extracting zip code and phone number 
a = pd.read_csv("Pharma.csv")
a = a.fillna(0)
a.columns =['Name', 'Phone', 'Rating', 'Address']
a.loc[:, ~a.columns.str.contains('^Unnamed')]
a.Rating = a.Rating.apply(int)
a['zip'] = a['Address'].str.extract(r'(\d{5}\-?\d{0,4})')
a.to_csv("Pharma.csv")
