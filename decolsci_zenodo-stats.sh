#!/bin/bash

# To use this script you need to have "curl" and "jq" installed.

# Download all records (including multiple versions) from the community (max 10k records)
curl "https://zenodo.org/api/records/?page=1&size=10000&q=&all_versions=true&communities=africarxiv" > /tmp/zenodo-resp.json

# Create CSV file header
echo "URL,DOI,Title,Abstract,Views,Downloads,Author,Affiliation,ORCID,Created,Updated,License,Keywords" > "africarxiv_stats.csv"

# Process response and append to CSV file
# Take first author information, parse timestamps, join keywords into a single string if array
jq -r '.hits.hits[] | [.links.self, .metadata.doi, .metadata.title, .metadata.description, .stats.views, .stats.downloads, .metadata.creators[0].name, .metadata.creators[0].affiliation, .metadata.creators[0].orcid, (.created | split(".")[0] + "Z" | fromdate | strftime("%Y-%m-%d")), (.updated | split(".")[0] + "Z" | fromdate | strftime("%Y-%m-%d")), .metadata.license.id, (.metadata.keywords | if type == "array" then join(", ") else . end)] | @csv' /tmp/zenodo-resp.json >> "africarxiv_stats.csv"

# Add Excel UTF-8 BOM to CSV file
echo -ne "\xEF\xBB\xBF" | cat - "africarxiv_stats.csv" > temp.csv && mv temp.csv "africarxiv_stats.csv"