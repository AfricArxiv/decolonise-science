# -*- coding: utf-8 -*-
"""Zenodo-AfricArxiv

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13kHsC9_ar1y1QSID3iZKjP9IUrt724xr

## [Decolonise Science's Metadata extraction](https://github.com/AfricArxiv/decolonise-science/wiki/Metadata-extraction)

I adapted the `zenodo-community-stats.sh`  .. to work on Colab.

Just run all the cells below to the end to get your extracted CSV file
"""

! sudo apt-get install curl jq

"""We are using Python to set the variables because they do not get recognized just using `!`.

If you want to change the name of your extracted file, change the vairable `FILENAME`.
"""

import os
from datetime import datetime

# current date and time
curDT = datetime.now()
# current date
date = curDT.strftime("%Y-%m-%d")
# creating the date object of today's date
os.environ["date"] =  date
# Change below for your filename
FILENAME = f"lanafric_zenodo-extract_{date}"
os.environ["filename"] = FILENAME

# To use this script you need to have "curl" and "jq" installed.

# Download all records (including multiple versions) from the community (max 10k records)
!curl "https://zenodo.org/api/records/?page=1&size=10000&q=&all_versions=true&communities=africarxiv" > zenodo-resp.json

# Create CSV file header
!echo "URL,DOI,Title,Abstract,Views,Downloads,Author,Affiliation,ORCID,Created,Updated,License,Keywords" > "${filename}.csv"
# Process response and append to CSV file
# Take first author information, parse timestamps, join keywords into a single string if array
!jq -r '.hits.hits[] | [.links.self, .metadata.doi, .metadata.title, .metadata.description, .stats.views, .stats.downloads, .metadata.creators[0].name, .metadata.creators[0].affiliation, .metadata.creators[0].orcid, (.created | split(".")[0] + "Z" | fromdate | strftime("%Y-%m-%d")), (.updated | split(".")[0] + "Z" | fromdate | strftime("%Y-%m-%d")), .metadata.license.id, (.metadata.keywords | if type == "array" then join(", ") else . end)] | @csv' zenodo-resp.json >> "${filename}.csv"

# Add Excel UTF-8 BOM to CSV file
!echo -ne "\xEF\xBB\xBF" | cat - "${filename}.csv" > temp.csv && mv temp.csv "${filename}.csv"