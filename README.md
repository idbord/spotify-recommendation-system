# CSCIB351FinalProject - ML: Machine Learning or Music Learning
Final project repository for Group 15.

## Overview
This projects estimates how much you will like a given playlists based on a
liked input playlist. It lets you use three different algorithms, Naive Bayes,
Random Forest, and K-Nearest Neighbor and compare the results.


### analytics.py
This module is used to create data tables and find specific values within them.
It has a method to create a data table based on a given playlist and values from
a comparator playlist. It also has a method to find the average of a data table
returning both the averages and the table name it found them from.

### dataOrganization.py
This module is used to connect to and pull information from the Spotify API.
It has methods that can find the Spotify ID of a song, the top 50 songs of a
given year, and is able to turn CSV files of names and artists of songs into
useful information for the program to use.


### kNearestNeighbor.py
This module uses the K-Nearest neighbors algorithm to determine whether two
Spotify playlists are similar. It has methods for fitting data based on given
input data and predicting results based off the fitted data.

### main.py
This module runs the algorithms with given song csv files and comparator csv
files.

### naiveBayes.py
This module implements the Naïve Bayes algorithm to determine whether two
Spotify playlists are similar. It has methods for fitting data that it is given
and predicting a result off of the fitted data.

### randomForest.py
This module uses the Random Forest algorithm to determine whether or not two
Spotify playlists are similar. It's fit and predict methods are implemented
using the Sci-kit-Learn.

### userInterface.py
