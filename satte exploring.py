
import PyPDF2
import re
import pandas as pd
from urlextract import URLExtract

f = open('satte 2023.pdf','rb')
pdf_reader = PyPDF2.PdfReader(f)

number_of_pages = len(pdf_reader.pages)
page = pdf_reader.pages[34]
text = page.extract_text()
text = text.replace('37','37\n')


dashes = [match.span() for match in re.finditer('---',text)]


re.findall('\n[A-Z]+(?:\s+[A-Z]+)*\n', text)
re.findall('\n[A-Z]+', text)
re.findall('\W*?[A-Z]{2,}', text)

for match in re.finditer('\n[A-Z]+', text):
    if match.group() != '\nEVENT' and match.group() != '\nHALL' and match.group() != '\nBOOTH':
        print(match.group())




spans = [match.span() for match in re.finditer('\n[A-Z]+', text) if match.group() != '\nEVENT' and match.group() != '\nHALL' and match.group() != '\nBOOTH']

exact_spans = [ ]
for i in range(len(spans)):
    start = spans[i][0]
    if i != len(spans)-1 :
        end = spans[i+1][0]-1
    else :
        end = len(text)-1
    exact_spans.append([start,end])


a = text[54:576].find('Address')
b = text[54:576].find('Person Name')
c = text[54:576].find('Phone')
d = text[54:576].find('Email')

re.match('CO EXHIBITORS',text)

text[54:576][a:b]
text[54:576][b:c]
text[54:576][c:d]


for item in exact_spans:
    s = text[item[0]:item[1]]
    a = s.find('Address')
    b = s.find('Person Name')
    c = s.find('Phone')
    d = s.find('Email')
    address = s[a:b]
    person = s[b:c]
    phone = s[c:d]
    email = s[d:]
    print(address)
    print('------')
    print(person)
    print('------')
    print(phone)
    print('------')
    print(email)

pages = range(34,171)

exhibitor_name = [ ]
exhibitor_address = []
exhibitor_person_name = []
exhibitor_phone = []
exhibitor_email_id = []
undone_pages= []

for k in pages:
    print(k,'page doing')
    try :
        page = pdf_reader.pages[k]
        text = page.extract_text()
        text = text.replace(str(k+1), str(k+1)+'\n', 1)
        if re.search('CO EXHIBITORS',text) :
            #undone_pages.append(k)
            pass
        else:
            if re.search('---', text):
                dashes = [match.span() for match in re.finditer('---', text)]
                last_dash = dashes[-1][1]
                text = text[last_dash:]
                 # undone_pages.append(k)
                email_index = [match.span() for match in re.finditer('Email', text)]
                text = text[email_index[0][1]:]
            else :
                pass

            spans = [match.span() for match in re.finditer('\n[A-Z]+', text) if
                 match.group() != '\nEVENT' and match.group() != '\nHALL' and match.group() != '\nBOOTH']

            exact_spans = []
            for i in range(len(spans)):
                start = spans[i][0]
                if i != len(spans) - 1:
                    end = spans[i + 1][0]
                else:
                    end = len(text) - 1
                exact_spans.append([start, end])

            for item in exact_spans:
                s = text[item[0]:item[1]]
                names_initial = [j.span() for j in re.finditer('\n', s)]
                names_start = names_initial[0][1]
                names_end = names_initial[1][0]
                name = s[names_start:names_end]

                a = s.find('Address')
                b = s.find('Person Name')
                c = s.find('Phone')
                d = s.find('Email')

                address = s[a:b]
                person = s[b:c]
                phone = s[c:d]
                email_website = s[d:]

                exhibitor_name.append(name)
                exhibitor_address.append(address)
                exhibitor_phone.append(phone)
                exhibitor_person_name.append(person)
                exhibitor_email_id.append(email_website)
    except :
        undone_pages.append(k)






sample =  pd.DataFrame({"exhibitor_name":exhibitor_name,"exhibitor_address":exhibitor_address,"exhibitor_person_name": exhibitor_person_name,"email" :exhibitor_email_id,"Phone":exhibitor_phone})

sample.to_csv('exhibitors.csv')



exhibitor_name = [ ]
exhibitor_address = []
exhibitor_person_name = []
exhibitor_phone = []
exhibitor_email_id = []

for pg in undone_pages :
    page = pdf_reader.pages[pg]
    text = page.extract_text()
    text = text.replace(str(pg + 1), str(pg + 1) + '\n', 1)
    split_char = '-'*65
    results = text.split(split_char)
    if len(results)>1:
        for result in results:
            try :
                b = result.find('Person Name')
                c = result.find('Phone')
                d = result.find('Email')

                name = result[:b]
                person = result[b:c]
                phone = result[c:d]
                email_website = result[d:]

                exhibitor_name.append(name)
                exhibitor_phone.append(phone)
                exhibitor_person_name.append(person)
                exhibitor_email_id.append(email_website)
            except :
                pass



co_exhibitors = pd.DataFrame({"exhibitor_name":exhibitor_name,"exhibitor_person_name": exhibitor_person_name,"email" :exhibitor_email_id,"Phone":exhibitor_phone})

co_exhibitors.exhibitor_name =  co_exhibitors.exhibitor_name.str.strip()


co_exhibitors.to_csv('coexhibitors.csv')

# cleaning

df = pd.read_csv('exhibitors.csv')

pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})+'

text = df['email'][0]
email = re.search(pattern, text).group()

df['email_actual'] = df['email'].apply(lambda x : re.search(pattern, x).group() if  re.search(pattern, x) else '')



web_pattern = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'

web_pattern = r'^www.[a-zA-Z0-9\.\/\?\:\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
website =  re.search(web_pattern, text).group()


def extract_email(text):
    web_address= ''
    if text.find('Description') != -1 :
        description = text.split('Description')[1]
        text_splitted = text.split('Description')[0].split('www')
        if len(text_splitted)>1 :
            web_address = 'www' + text_splitted[1]
    else :
        text_splitted = text.split('www')
        description = ' '
        if len(text_splitted)>1 :
            web_address = 'www' + text_splitted[1]

    return web_address,description



extract_email(text)

df[['website','description']] = df.apply(lambda x :extract_email(x['email']), axis= 1,  result_type="expand")


df.to_csv('exhibitors_ver2.csv')


