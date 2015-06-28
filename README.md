# Scopos

http://scopos.link

A personalized job search tool.

This is my Insight Data Science project.

## Prepare the job posting database

Currently the job database used by http://scopos.link only includes data scientist/engineer jobs in New York. To prepare your own job database:

0. create an empty mysql database "indeed"

1. Run createDB.sql

2. Create a text file indeed_api_key that contains your indeed.com API key and Mashape key
http://www.indeed.com/publisher
https://www.mashape.com/indeed/indeed

3. Follow JobsTest.py to add jobs to the database

