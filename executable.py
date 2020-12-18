import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

# Defining function to create chromebrowser
def initialize_chromebrowser(headless: bool):
    """
    Arguements:
        1) Headless (boolean)
            False -> Web scraping browser IS VISIBLE to user as it executes
            True -> Web scraping browser is NOT VISIBLE to user as it executes
    """
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}  ###### THIS PATH MUST POINT TO YOUR LOCAL CHROMEBROWSER FILE ######
    browser = Browser("chrome", **executable_path, headless=headless)
    return browser

# Creating master dataframe (output file) layout 
output_file = pd.DataFrame({
    "Name": ["Name"],
    "Full Name": ["full_name"],
    "First Name": ["First Name"],
    "Last Name": ['Last Name'],
    "Legal": ['Legal'],
    "Lot Size": ["Lot Size"],
    "Views": ["Views"],
    "Appraised Land Value ($)": ["Land Value"],
    "Appraised Imps Value ($)": ["Appraised Imps"],
    "Appraised Total ($)": ["Appraised Total"],
    "Property Name": ["property_name"],
    "Present Use": ["present_use"],
    "Acres": ["acres"],
    "Unbuildable": ["unbuildable"],
    "Restrictive Size Shape": ["restrictive_size_shape"],
    "Zoning": ["zoning"],
    "Water": ["water"],
    "Sewer/Septic": ["sewer_septic"],
    "Road Access": ["road access"],
    "Power Lines": ["power_lines"],
    "Water Problems": ["water problems"],
    "Environmental": ["environmental"],
    "PAddress": ["address"],
    "PCity": ["jurisdiction"],
    "PZip": ["zipcode"],
    "Latitude": ["lat"],
    "Longitude": ["long"],
    "Urban Growth Area": ["urban_growth_area"],
    "Address_1": ["address"],
    "Address_2": ["address_2"],
    "City": ["city"],
    "State": ["state"],
    "Zip": ["zipcode"],
    "Total Billed": ["total_billed"],
    "Balance": ["balance"],
    "Document Date": ["document_date"],
    "Sales Price": ["sales_price"],
    "Parcel ID": ["parcel_id"]})

# Reading in Parcel Ids
df = pd.read_excel("parcels.xlsx") ######## Input path of excel file that contains parcel id's
parcel_ids = list(df["PARCEL_ID"]) ######## Column header of parcel ids 
parcel_length = len(parcel_ids)

# Initializing chromebrowser
browser = initialize_chromebrowser(headless=False)

count = 1
# Collecting information
for parcel_id in parcel_ids:
    # Navigate to website 1
    browser.visit(f"https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={parcel_id}")
    time.sleep(2)
    try:
        # Scrape HTML
        dataframes = pd.read_html(browser.html)
        data = dataframes[1]
        # Extract data from website 1
        for index, row in data.iterrows():
            # Retrieving NAME, LEGAL, LOT SIZE, VIEWS, APPRAISAL INFORMATION
            if row[0] == "Name":
                name = row[1]   
            if row[0] == "Legal":
                legal = row[1]
            if row[0] == "Lot Size":
                lot_size = row[1]
            if row[0] == "Views":
                views = row[1]
            if row[0] == "Valued Year":
                next_index = index + 1
                appraised_land_value = data.loc[next_index, 2]
                appraised_imps_value = data.loc[next_index, 3]
                appraised_total = data.loc[next_index, 4]
        # Separating FIRST NAME and LAST NAME
        split_full_name = name.split(" ")
        if len(split_full_name) == 2:
            last_name = split_full_name[0]
            first_name = split_full_name[1]
        elif len(split_full_name) >= 3:
            last_name = split_full_name[0]
            first_name_list = split_full_name[1:3]
            if len(first_name_list[1]) == 1:
                first_name = " ".join(first_name_list)
            else:
                first_name = first_name_list[0]
        else:
            last_name = split_first_name[0]
            first_name = "OCCUPANT"
        # FULL NAME
        if ("LLC" in name) or ("llc" in name):
            full_name = name
        else:
            full_name = f"{first_name} {last_name}"
    except:
        name = ""
        full_name = ""
        legal = ""
        lot_size = ""
        views = ""
        appraised_land_value = ""
        appraised_imps_value = ""
        appraised_total = ""
        last_name = ""
        first_name = ""
    
    # Navigate to website 2
    browser.visit(f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={parcel_id}")
    time.sleep(2)
    try:
        # Scrape HTML
        dataframes = pd.read_html(browser.html)
        # Extracting PROPERTY NAME, PRESENT USE, ACRES, UNBUILDABLE, RESTRICTIVE SIZE SHAPE, ZONING, WATER, SEWER/SEPTIC, ROAD ACCESS, POWER LINES, WATER PROBLEMS, ENVIRONMENTAL
        for index, row in dataframes[1].iterrows():
            if row[0] == "Property Name":
                property_name = row[1]  
            if row[0] == "Present Use":
                present_use = row[1]
            if row[0] == "Acres":
                acres = row[1]
            if row[0] == "Unbuildable":
                unbuildable = row[1]
            if row[0] == "Restrictive Size Shape":
                restrictive_size_shape = row[1]
            if row[0] == "Zoning":
                zoning = row[1]
            if row[0] == "Water":
                water = row[1]
            if row[0] == "Sewer/Septic":
                sewer_septic = row[1]
            if row[0] == "Road Access":
                road_access = row[1]
            if row[0] == "Power Lines":
                power_lines = row[1]
            if row[0] == "Water Problems":
                water_problems = row[1]
            if row[0] == "Environmental":
                environmental = row[1]
    except:
        property_name = ""
        present_use = ""
        acres = ""
        unbuildable = ""
        restrictive_size_shape = ""
        zoning = ""
        water = ""
        sewer_septic = ""
        road_access = ""
        power_lines = ""
        water_problems = ""
        environmental = ""
        
    # DOCUMENT DATE, SALES PRICE
    soup = bs(browser.html, "html.parser")
    try:
        items = soup.find("table", {"id":"cphContent_GridViewSales"}).find_all("td")
        document_date = items[2].text.strip()
        sales_price = items[3].text.strip()
    except:
        document_date = ""
        sales_price = ""
            
    # Navigate to website 3
    browser.visit(f"https://www5.kingcounty.gov/kcgisreports/dd_report.aspx?PIN={parcel_id}")
    time.sleep(2)
    try:
        # Scrape HTML
        dataframes = pd.read_html(browser.html)
        # Extracting ADDRESS, JURISDICTION, ZIPCODE, LATITUDE, LONGITUDE, URBAN GROWTH AREA
        for index, row in dataframes[1].iterrows():
            if row[0] == "Address":
                paddress = row[1] 
            if row[0] == "Jurisdiction":
                jurisdiction = row[1] 
            if row[0] == "Zipcode":
                pzip = row[1] 
            if row[0] == "Latitude":
                lat = row[1] 
            if row[0] == "Longitude":
                long = row[1] 
            if row[0] == "Urban Growth Area":
                urban_growth_area = row[1]
    except:
        paddress = ""
        jurisdiction = ""
        pzip = ""
        lat = ""
        long = ""
        urban_growth_area = ""
        
    # Navigate to website 4
    browser.visit(f"https://payment.kingcounty.gov/Home/Index?app=PropertyTaxes&Search={parcel_id}")
    time.sleep(2)
    try:
        try:
            # Scrape HTML
            dataframes = pd.read_html(browser.html)
        except:
            time.sleep(3)
            dataframes = pd.read_html(browser.html)
        # Get Tax Information
        for i in range(len(dataframes)):
            if "Balance" in list(dataframes[i].iloc[:,0]):
                for index, row in dataframes[i].iterrows():
                    if row["Tax Information"] == "Balance":
                        balance = row["2020"]
            if ("Total billed" in list(dataframes[i].iloc[:,0])) or ("Total Billed" in list(dataframes[i].iloc[:,0])):
                for index, row in dataframes[i].iterrows():
                    if (row["Tax Information"] == "Total billed") or (row["Tax Information"] == "Total Billed"):
                        total_billed = row["2020"]
    except:
        total_billed = ""
        balance = ""
        
    try:
        # Extracting ADDRESS, CITY, STATE, ZIPCODE
        soup = bs(browser.html, "html.parser")
        items = soup.find("div",{"id":"parcelPanels"})
        narrowed = items.find_all("p")
        if len(narrowed) == 7:
            address_information = narrowed[2]
        elif len(narrowed) == 9:
            address_information = narrowed[4]

        master_list = []
        address_list = []
        address_element_list = address_information.text.strip().split(" ")
        # ZIPCODE
        zipcode = address_element_list[-1]
        # Finding address pieces
        for i in address_element_list:
            master_list.append(i)
            num_blanks = len([j for j in master_list if j == ""])
            if num_blanks == 2:
                address_piece = " ".join(master_list).strip()
                address_list.append(address_piece)
                master_list = []
        # Eliminating all blank elements in list
        while "" in address_list:
            _index = 0
            for _ in address_list:
                if _ == "":
                    address_list.pop(_index)
                _index+=1
        # ADDRESS_1 ADDRESS_2
        if len(address_list) == 3:
            address_1 = address_list[1]
            address_2 = address_list[0]
        elif len(address_list) == 2:
            address_1 = address_list[0]
            address_2 = ""
        # CITY
        city_word_list = address_list[-1].split(" ")[:-1]
        city = " ".join(city_word_list)
    except:
        address_1 = ""
        address_2 = ""
        city = ""
        zipcode = ""

    # Creating new row of data
    new_row = pd.DataFrame({
        "Name": name,
        "Full Name": full_name,
        "First Name": first_name,
        "Last Name": last_name,
        "Legal": legal,
        "Lot Size": lot_size,
        "Views": views,
        "Appraised Land Value ($)": appraised_land_value,
        "Appraised Imps Value ($)": appraised_imps_value,
        "Appraised Total ($)": appraised_total,
        "Property Name": property_name,
        "Present Use": present_use,
        "Acres": acres,
        "Unbuildable": unbuildable,
        "Restrictive Size Shape": restrictive_size_shape,
        "Zoning": zoning,
        "Water": water,
        "Sewer/Septic": sewer_septic,
        "Road Access": road_access,
        "Power Lines": power_lines,
        "Water Problems": water_problems,
        "Environmental": environmental,
        "PAddress": paddress,
        "PCity": jurisdiction,
        "PZip": pzip,
        "Latitude": lat,
        "Longitude": long,
        "Urban Growth Area": urban_growth_area,
        "Address_1": address_1,
        "Address_2": address_2,
        "City": city,
        "State": "WA",
        "Zip": zipcode,
        "Total Billed": total_billed,
        "Balance": balance,
        "Document Date": document_date,
        "Sales Price": sales_price,
        "Parcel ID": parcel_id}, index=[max(output_file.index)+1])

    # Appending new row to Master DataFrame
    output_file = output_file.append(new_row)

    time.sleep(2)
    print(f"{count}/{parcel_length} Parcel ID's Processed")
    count += 1

# Closing the browser window
browser.quit()
# Dropping Layout Row of Master Dataframe
output_file.drop(index=0, axis=0, inplace=True)
# Saving Data to excel spreadsheet
output_file.to_excel(f"results.xlsx", index=False)