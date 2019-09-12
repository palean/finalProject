## Recommendation System for Hiking in Mexico

Paola Alean
Datamex 0719

## Overview
I love hiking. Personally, it's one of the ways to get to know a new country. So, what if we map all available hikes in Mexico and find out if there are routes that have desirable characteristics? Well, this recommender system will provide that first approach. It includes difficulty level, facilities for kids or even if you can do mountain bike. Additionally, it will recommend hikes based on trails you know you like.

![overview](https://dl.dropboxusercontent.com/s/s0jlrva0j7q43ru/overview.jpg?dl=0)

## The Process
![process](https://dl.dropboxusercontent.com/s/pvngjhvco6kecgk/process.jpg?dl=0)

## Data Collection and Cleanning
I got all data from AllTrails.com. Using Selenium, I web scraped their list of the existing 322 hikes in Mexico. This included all of the hike meta data such as the users who reviewed the hike and the corresponding ratings. Once I cleaned the data by getting rid of the hikes that had no ratings or were missing data, I was left with 252 trails. 

I addition, I turned some of the hike attributes into features. The features for each hike were: hike ID, hike Name, region, distance in kms, elevation gain in mts, difficulty level, global stars, number of reviews, user ID, user name, rating given by user, Route Type (loop, out and back, point to point), dog Friendly, kid Friendly, camping, near water, mountain biking, views, bird watching, climbing, forest, trail running and historic place.
