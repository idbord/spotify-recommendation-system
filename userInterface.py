import dataOrganization
import numpy
from naiveBayes import *
from kNearestNeighbor import *
from randomForest import *
import analytics
import seaborn as sns
import matplotlib.pyplot as plt

class Demo:
    def __init__(self, sFiles, cFiles, needHelp):
        self.algorithms = [("Naive Bayes", "NB"), ("K-Nearest Neighbor", "KNN"), ("Random Forest", "RF")]
        self.dataFrameTrainX = None
        self.dataFrameTrainY = None
        self.dataFrameTestX = None

        self.comparatorData = None
        self.comparatorURIList = None
        self.comparatorTrackNames = None
        self.comparatorDataFrame = None
        self.comparatorDataFrameRounded = None
        self.comparatorsDataFrameTestNumpy = None

        self.songsURIList = None
        self.songsTrackNames = None
        self.songsClassification = None
        self.songsDataFrame = None
        self.songsDataFrameRounded = None
        self.songsDataFrameTestNumpy = None

        self.sFiles = sFiles
        self.cFiles = cFiles

        self.needHelp = needHelp

    def readFile(self, path):
        path = "./Playlists/" + path
        try:
            fptr = open(path)
            result = []
            for line in fptr.readlines():
                result.append(line[:-1].split(","))
            return result
        except:
            return []

    """
    Collects the data and stores it into a dataframe.
    Checks to see if comparator playlist is a file or Top 50 from some year.
    """
    def collectData(self, songPath, comparatorPath):
        songData = self.readFile(songPath)
        self.songsURIList, self.songsTrackNames, self.songsClassification = dataOrganization.playlistReader(songData, self.needHelp)
        self.songsDataFrame = dataOrganization.buildDataFrame(self.songsURIList, self.songsTrackNames, self.songsClassification)
        self.songsDataFrameRounded = dataOrganization.roundAndMapValues(self.songsDataFrame)
        self.songsDataFrameTestNumpy = self.songsDataFrameRounded.to_numpy()

        if comparatorPath != None:
            self.comparatorData = self.readFile(comparatorPath)
            self.comparatorURIList, self.comparatorTrackNames = dataOrganization.playlistReaderCompare(self.comparatorData, self.needHelp)

        self.comparatorDataFrame = dataOrganization.buildDataFrameCompare(self.comparatorURIList, self.comparatorTrackNames)
        self.comparatorDataFrameRounded = dataOrganization.roundAndMapValues(self.comparatorDataFrame)
        self.comparatorsDataFrameTestNumpy = self.comparatorDataFrameRounded.to_numpy() # Could probably add this to a method in organization

        self.dataFrameTrainX = self.songsDataFrameTestNumpy[:,0:11]
        self.dataFrameTrainY = self.songsDataFrameTestNumpy[:,11:]
        self.dataFrameTrainY = numpy.concatenate(self.dataFrameTrainY, axis=0)
        self.dataFrameTestX = self.comparatorsDataFrameTestNumpy[:,0:11]


    def runNaiveBayes(self):
        nb = NaiveBayes(self.dataFrameTrainX, self.dataFrameTrainY)
        nb.fit(self.dataFrameTrainX, self.dataFrameTrainY)
        y_pred = nb.predict(self.dataFrameTestX)
        return y_pred

    def runKNN(self):
        KNNTest = KNN(3)
        KNNTest.fit(self.dataFrameTrainX, self.dataFrameTrainY)
        predictions = KNNTest.predict(self.dataFrameTestX)
        return predictions

    def runRandomForest(self):
        rf = RandomForest(100)
        rf.fitLocal(self.dataFrameTrainX, self.dataFrameTrainY)
        return rf.prediction(self.dataFrameTestX)

    """
    Display Analytics takes in the predictions from some algorithm 
    and filters out the playlists that did not match our given 
    song playlist. It then builds a dataframe and returns it to be displayed. 
    """
    def displayAnalytics(self, predictions):
        tempURIList, tempTrackNames = list(), list()
        for _ in range(len(predictions)):
            if predictions[_] == 1:
                tempURIList.append(self.comparatorURIList[_])
                tempTrackNames.append(self.comparatorTrackNames[_])

        comparatorPlayListUpdated = dataOrganization.buildDataFrame(tempURIList, tempTrackNames, [1] * len(tempURIList))
        comparatorPlayListUpdated = dataOrganization.roundAndMapValues(comparatorPlayListUpdated)
        comparatorPlayListUpdated = comparatorPlayListUpdated.drop_duplicates()
        
        songsTable = analytics.findAverage(self.songsDataFrameRounded, "Songs")
        analyticsTable = analytics.dataTable(songsTable, comparatorPlayListUpdated.transpose())
        return analyticsTable

    def run(self):
        sFile, cFile = self.getFiles()  # Gets song and comparator playlist locations
        print("---- Loading Data ---")
        self.collectData(sFile, cFile)  # Stores them in Panda tables.

        while 1:
            print("Choose an Algorithm")
            for index, algo in enumerate(self.algorithms):
                print(f"{index + 1}. {algo[0]}")
            
            print("D. Display KNN Graphs")
            print("Q. Quit")
            option = input("Choose a playlist: ")

            if option == "q" or option == "Q":
                break

            if option == "d" or option == "D":
                print("Gathering data and building your graphs...")
                self.displayKNN()

            elif int(option) > 0 and int(option) <= len(self.algorithms):
                print()
                self.chooseAlgorithm(self.algorithms[int(option) - 1][1])
            else:
                print("Not a valid command")
            print("\n----------------------------------\n")
        print("Enjoy your new music!")

    """
    Lets you choose an algorithm to run and display analytics
    """
    def chooseAlgorithm(self, Algorithm):
        predictions = list()
        if Algorithm == "NB": predictions = self.runNaiveBayes()
        elif Algorithm == "KNN": predictions = self.runKNN()
        elif Algorithm == "RF": predictions = self.runRandomForest()
        
        if predictions != []:
            print(self.displayAnalytics(predictions))

    """
    Program allows you to choose what song/comparator playlist you
    want. If you add a csv file to the main.py lists, then it will
    automatically adjust, so you can choose what playlist you want. 
    """
    def getFiles(self):
        songFile = "songs.csv"
        comparatorFile = "comparator.csv"

        # Displays songs
        print("Song Playlists: ")
        for index, playlist in enumerate(self.sFiles):
            print(f"{index + 1}. {playlist}")
        songOption = input("Choose playlist: ")  # Grabs song pick

        """
        sets songFile to what you option you picked as long as it
        is within range of songList. If it's not, sets it to default
        song playlist of "songs.csv"
        """
        if int(songOption) - 1 < len(self.sFiles):
            songFile = self.sFiles[int(songOption) - 1]

    
        # Display comparator playlists    
        print("Comparator Playlists: ")
        for index, playlist in enumerate(self.cFiles):
            print(f"{index + 1}. {playlist}")
        print(f"{len(self.cFiles) + 1}. Choose a year (2021 or earlier)")  # 2020 will not work for some reason, but 2019 will
        comparatorOption = input("Choose playlist: ")  # Grab comparator option
        
        """
        Checks if it's within bounds of comparator playlist or if
        you're choosing Top 50 from some year (2021 or earlier).
        """
        if int(comparatorOption) == len(self.cFiles) + 1:
            year = int(input("Input a year: "))
            artist_name, track_name, track_id, values = dataOrganization.yearURIs(year)
            self.comparatorURIList, self.comparatorTrackNames = track_id, track_name
            comparatorFile = None
        elif int(comparatorOption) - 1 < len(self.cFiles):
            comparatorFile = self.cFiles[int(comparatorOption) - 1]
        
        return songFile, comparatorFile

    def displayKNN(self):
        predictions = self.runKNN()
        tempURIList, tempTrackNames = list(), list()
        for _ in range(len(predictions)):
            if predictions[_] == 1:
                tempURIList.append(self.comparatorURIList[_])
                tempTrackNames.append(self.comparatorTrackNames[_])

        comparatorPlayListUpdated = dataOrganization.buildDataFrame(tempURIList, tempTrackNames, [1] * len(tempURIList))
        comparatorPlayListUpdated = dataOrganization.roundAndMapValues(comparatorPlayListUpdated)
        comparatorPlayListUpdated = comparatorPlayListUpdated.drop_duplicates()

        analyticsTable = analytics.dataTable(self.songsDataFrameRounded.transpose(), comparatorPlayListUpdated.transpose())

        sns.pairplot(
            analyticsTable,
            hue = "Classification",
            corner = True,
            kind = 'reg'
        )
        plt.show()
