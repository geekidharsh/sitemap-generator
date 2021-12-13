#!/usr/bin/env python
# coding: utf-8
# @author: Harsh Pandey
# @project: sitemap-generator

import pandas as pd
import os
import datetime
from jinja2 import Template
import gzip
import time

# compute time to run code
start_time = datetime.datetime.now()


# Import List of URLs
input_file = 'top-1m.csv'
list_of_urls = pd.read_csv(input_file)
print('Found file: ', input_file)

# remove extra columns
list_of_urls = pd.read_csv(input_file)
inp_columns = list_of_urls.columns.to_list()

if list_of_urls.empty:
    print('input file is empty')

elif list_of_urls.shape[1] > 1:
    print('Input file has more than 1 column')
    for i in inp_columns:
        if i.lower() == 'url':
            print('required column found: ', i)
            list_of_urls = list_of_urls[[i.lower()]]
            print(list_of_urls.shape)


# Escape Special Characters
special_char = {'&':'&',"'":"'",'"':'"','>':'&gt','<':'<'}
list_of_urls['url'] = list_of_urls['url'].replace(special_char, regex=True)


print('{} has a total of {} urls'.format(input_file, len(list_of_urls)))


# Set-Up Maximum Number of URLs (recommended max 50,000)
n = 50000

# Create New Empty Row to Store the Splitted File Number
list_of_urls['name'] = ''


print(list_of_urls.shape[0])

# # Split the file with the maximum number of rows specified
new_df = [list_of_urls[i:i+n] for i in range(0,list_of_urls.shape[0],n)]

for i in range(0, list_of_urls.shape[0], n):
    print(i, i+n)

# For Each File Created, add a file number to a new column of the dataframe
for i,v in enumerate(new_df):
    v.loc[:,'name'] = str(v.iloc[0,1])+'_'+str(i)
    print(v)
             
# Create a Sitemap Template to Populate 
sitemap_template='''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for page in pages %}
    <url>
        <loc>{{page[1]|safe}}</loc>
        <lastmod>{{page[3]}}</lastmod>
        <changefreq>{{page[4]}}</changefreq>
        <priority>{{page[5]}}</priority>        
    </url>
    {% endfor %}
</urlset>'''
 
template = Template(sitemap_template)
 
# Get Today's Date to add as Lastmod
lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')
 

print('Generating sitemap')

# Fill the Sitemap Template and Write File
for i in new_df:                           # For each URL in the list of URLs ...                                                          
    i.loc[:,'lastmod'] = lastmod_date      # ... add Lastmod date
    i.loc[:,'changefreq'] = 'daily'        # ... add changefreq
    i.loc[:,'priority'] = '1.0'            # ... add priority 
 
    # Render each row / column in the sitemap
    sitemap_output = template.render(pages = i.itertuples()) 
     
    # Create a filename for each sitemap like: sitemap_0.xml.gz, sitemap_1.xml.gz, etc.
    curr_path = os.getcwd()
    out_path = os.path.join(curr_path, 'output')
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    filename = os.path.join(out_path,'sitemap' + str(i.iloc[0,1]) + '.xml.gz')
 
    # Write the File to Your Working Folder
    print('Saving File: {}'.format(filename))
    with gzip.open(filename, 'wt') as f:   
        f.write(sitemap_output)
        

print('Duration: {}'.format(datetime.datetime.now() - start_time))




