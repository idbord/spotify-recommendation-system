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
The User Interface allows anyone running the program to interact with it and
allow them to add new songs to their pre-existing playlist. The UI has a simple
interface where you choose a song playlist (one that is already created or one
you created), a comparator playlist (three pre-existing playlists or you 
may choose the top 50 from any year), and then choose what algorithm you would
like to use to determine the songs best fit for your playlist. You may also
display some graphs that use the predictions from KNN. 


## Getting Started
#### 1) Install libraries needed to run program.
pip install -r requirements.txt

#### 2) Getting Your Playlists Ready
Before you start, you might want to create your own playlist or comparator playlist to use with the program. If you DO NOT want to create your own, move on to step 3.

You will see two Python lists in the main.py file. sFiles contains the files of playlists that are used to determine whether you like or dislike a song and cFiles are the comparator playlists. 

##### 2a) Song Playlists
If you are creating your own songs playlist, please create a new file (name it whatever you like) and add it to the sFiles list. Please use the songs playlist format listed below.

Format: song,artist,like or not like (1 = like, 0 = do not like)

Example: The Box,Roddy Ricch,1

We recommend adding at least 50 songs (25 liked songs and 25 disliked songs), but you may add however many you would like to.

##### 2b) Comparator Playlists
If you are creating your own comparator playlist, please create a new file (name it whatever you like) and add it to the cFiles list. Please use the comparator playlist format listed below.

Format: song,artist
Example: The Box,Roddy Ricch

For the comparator playlist, you may add as many songs you would like to. The comparator playlist are the songs that the algorithms may recommend you add to your songs playlist.

#### 2c) Comparator Playlist -- Top 50 for a year
If you choose to use the Top 50 songs from some year, you do not need to edit any code and you will be prompted to select a year using the user interface. Please note that you may choose any year from 2021 to 1951 (years around 1951 may cause errors, so we recommend staying above the year 2000).
#### 3) Running the program
Once you have organized your playlists, run the main.py file and use the console to interact with the program. If you have any issues with loading in songs, it may be due to an error while typing it in the CSV file. Please set the 'needHelp' variable to True (bool) and every song loading in will be printed in the console. The last song printed in the console (assuming it is breaking) is the reason your program may not be working properly. Here are some common issues that you may be experiencing...
1) You have quotes ("") around song names or artist names 
2) You have an extra comma in one of the lines (If a song or artist name has a comma, please do not include it)
3) You misspelt a song name or an artist's name
4) Song is not available on Spotify

