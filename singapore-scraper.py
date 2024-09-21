import requests
from bs4 import BeautifulSoup
import csv
result_csv = open('sgx_scrape.csv','w', newline='')
csv_writer = csv.writer(result_csv)

headers = ['Company Name', 'Full Company Name :', 'Last Updated On:','AUDITORS', 'Authorised Capital (Others) :', 'Authorised Capital (Pref) :', 'Authorised Capital :', 'Email :', 'Fax :', 'ISIN Code :', 'Incorporated in :', 'Incorporated on :', 'Issued & Paid-up Capital (Others) :', 'Issued & Paid-up Capital (Pref) :', 'Issued & Paid-up Capital :', 'LISTING', 'LISTING BOARD', 'Link to Internet Website :', 'OTHER STOCK EXCHANGE LISTINGS', 'Par Value (Others) :', 'Par Value (Pref) :', 'Par Value :', 'REGISTRARS / TRANSFER AGENTS & ADDRESS', 'Registered Office :', 'Secretary :', 'Telephone :', 'Trading Currency :']

csv_writer.writerow(headers)

for i in range(1000,3017):
    try:
        url = f"https://links.sgx.com/1.0.0/corporate-information/{i}"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        product = soup.find("div", id="divControls")
        name = [i.text.replace("\n", " ").strip() for i in soup.find_all("h2",class_="announcement-group-header")]
        date = [i.text.replace("\n"," ").strip() for i in soup.find("span", class_="displayLabel") ]
        
        # Create a dictionary to map dt to concatenated dd
        data = {}
        data["Company Name"] = name.pop()
        data["Last Updated On:"] = date.pop()
        dt_elements = product.find_all("dt")
        dd_elements = product.find_all("dd")
        
        for dt in dt_elements:
            key = dt.text.replace("\n", " ").strip()
            values = []
            # Find all following-sibling dd elements until the next dt
            sibling = dt.find_next_sibling()
            while sibling and sibling.name == "dd":
                values.append(sibling.text.replace("\n", " ").strip())
                sibling = sibling.find_next_sibling()
            data[key] = " ".join(values)
        # Create a row based on the headers
        row = [data.get(header, '') for header in headers]
        csv_writer.writerow(row)
    except Exception as e:
        print(f"Error processing company {i}: {e}")
        
    
result_csv.close()