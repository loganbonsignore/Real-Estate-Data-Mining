# Scraping WA Real Estate Information

## Overview
This web scraping program performs the Extract, Transform, Load (ETL) process of real estate metadata in Washington, USA. It collects data from multiple endpoints at kingscounty.gov, all related to a unique parcel number.

Data Collected:
- Occupants Full Name
- Mailing Address
- Lot Size
- Appraisal Value
- Acres
- Zoning
- Water
- Sewer/Septic
- Power Lines
- Water Problems
- Environmental
- Latitude/Longitude
- & more

All collected information is saved to an excel file named “results.py”. It downloads to the same directory that “executable.py” is executed from.

![Output Example](images/output_example.png)