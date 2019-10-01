import pandas as pd
import re 
import pycountry


def extractSecurities(securities):
    df = pd.read_csv("data/security.csv")
    security= {}
    for index, row in df.iterrows():
        security[row['Security']] = [row[1],row[2],row[3],row[4]]
    ratings =[]
    for i in securities:
        try:
            ratings.append(security[i])
        except:
            ratings.append("Not rated")

    return ratings


def extractCompaniesId(company):
    companies_set = set(company)
    companies_set = {x for x in companies_set if x==x}
    companies_set = sorted(companies_set)
    
    companies_dict = {}
    for idx, elems in enumerate(companies_set):
        companies_dict[elems] = idx    
    
    companies_id = []
    for com in company:
        try:
            companies_id.append(companies_dict[com])
        except:
            companies_id.append(-1)

    return companies_id


def extractCountry(ids):
    special_codes = {
        'AN':'Netherlands Antilles',
        'CS':'Serbia and Montenegro',
        'EU':'European Union',
        'ZR':'Zaire'
    }
    country_name_new = {
        'Czechia':'Czech Republic',
        'Russian Federation':'Russia',
        'Zaire':'Congo',
        'Macao':'Macau',
        'Venezuela, Bolivarian Republic of':'Venezuela'
    }
    ids = list(ids)
    country_lst = []
    count=0
    for id in ids:
        count+=1
        try:
            code = id[:2]
            try:
                country = pycountry.countries.get(alpha_2=code.upper())
                if country.name in country_name_new.keys():
                    country_lst.append(country_name_new[country.name])
                else:
                    country_lst.append(country.name)
            except:
                try:
                    country_lst.append(special_codes[code])
                except:
                    country_lst.append('UNKNOWN')

        except:
            country_lst.append('UNKNOWN')
    return country_lst


def extractRatings(countries):
    df = pd.read_csv("data/countryRating.csv")
    country_rating = {}
    for index, row in df.iterrows():
        country_rating[row['Country']] = row['TE']
    ratings =[]
    for i in countries:
        try:
            ratings.append(country_rating[i])
        except:
            ratings.append(-1)

    return ratings

def main():
    data = pd.read_csv("data/userportfolio30d.csv", header=None, names=["Username", "Security_Type", "WSO_ID", "ISIN", "Security_Name"])
    countries = extractCountry(data['ISIN'])
    data =data.drop(columns=['WSO_ID','ISIN'])
    data['Country'] = countries
    credit_rating = extractRatings(countries)
    data['Credit_Rating'] = credit_rating
    security = extractSecurities(data['Security_Type'])
    print(type(security))

    length = []
    experience = []
    risk = []
    capital = []

    for i in security:
        length.append(i[0])
        experience.append(i[1])
        risk.append(i[2])
        capital.append(i[3])
    data['Investment_Time'] = length
    data['Experience'] = experience
    data['Risk'] = risk
    data['Capital'] = capital

    company_id = extractCompaniesId(data['Security_Name'])
    data['Company_ID'] = company_id

    print(data.head(100))


    data.to_csv("extracted_data.csv", index = False)

if __name__ == '__main__':
    main()