import re
import csv
from openpyxl import workbook, load_workbook 

linebreak = 0

#Extracts the country name from the ids 
def extractCountry(ids):
    string = re.findall("[A-Z]",ids)
    try:
        countries = string[0]+ string[1]
    except:
        #print("No countries in this one: {0}".format(ids))
        countries =""
    return countries 


#main function used to open the csv and do things on it
with open("userportfolio30d.csv", newline = "") as csvFile:
    securites = []
    companies = []
    users = []
    countries = []
    all_file = csv.reader(csvFile)
    for row in all_file:
        #print(row)
        # if row[3] == "":
        #     print(row)
        cn = extractCountry(row[3])
        row.append(cn)
        #print(row)
        users.append(row[0])
        countries.append(row[5])
        securites.append(row[1])
        companies.append(row[4])
        # if linebreak == 10:
        #     break
        # linebreak += 1
    print(set(securites))
    print("No. of. Companies:  {0}".format(len(set(companies))))
    print("No.of Users: {0}".format(len(set(users))))
    
    print("No.of countries: {0}".format(len(set(countries))))
    
    