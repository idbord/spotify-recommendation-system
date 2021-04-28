import dataOrganization
import numpy
from NaiveBayes import *
from KNearestNeighbor import *
from RandomForest import *
from sklearn.ensemble import RandomForestClassifier
import analytics

class Demo:
    def __init__(self, sFiles, cFiles):
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

    def readFile(self, path):
        try:
            fptr = open(path)
            result = []
            for line in fptr.readlines():
                result.append(line[:-1].split(","))
            return result
        except:
            return []

    def collectData(self, songPath, comparatorPath):
        songData = self.readFile(songPath)
        self.songsURIList, self.songsTrackNames, self.songsClassification = dataOrganization.playlistReader(songData)
        self.songsDataFrame = dataOrganization.buildDataFrame(self.songsURIList, self.songsTrackNames, self.songsClassification)
        self.songsDataFrameRounded = dataOrganization.roundAndMapValues(self.songsDataFrame)
        self.songsDataFrameTestNumpy = self.songsDataFrameRounded.to_numpy()

        if comparatorPath != None:
            self.comparatorData = self.readFile(comparatorPath)
            self.comparatorURIList, self.comparatorTrackNames = dataOrganization.playlistReaderCompare(self.comparatorData)

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

    def displayAnalytics(self, predictions):
        tempURIList, tempTrackNames = list(), list()
        for _ in range(len(predictions)):
            if predictions[_] == 1:
                tempURIList.append(self.comparatorURIList[_])
                tempTrackNames.append(self.comparatorTrackNames[_])

        comparatorPlayListUpdated = dataOrganization.buildDataFrame(tempURIList, tempTrackNames, [1] * len(tempURIList))
        comparatorPlayListUpdated = dataOrganization.roundAndMapValues(comparatorPlayListUpdated)

        songsTable = analytics.findAverage(self.songsDataFrameRounded, "Songs")
        analyticsTable = analytics.dataTable(songsTable, comparatorPlayListUpdated.transpose())
        return analyticsTable

    def run(self):
        sFile, cFile = self.getFiles()
        print("---- Loading Data ---")
        self.collectData(sFile, cFile)
        while 1:
            print("Choose an Algorithm")
            for index, algo in enumerate(self.algorithms):
                print(f"{index + 1}. {algo[0]}")
            print("Q. Quit")
            option = input("Choose a playlist: ")

            if option == "q" or option == "Q":
                break
            
            if int(option) > 0 and int(option) <= len(self.algorithms):
                print()
                self.chooseAlgorithm(self.algorithms[int(option) - 1][1])
            else:
                print("Not a valid command")

            print("\n----------------------------------\n")

        print("Enjoy your new music!")

    def chooseAlgorithm(self, Algorithm):
        predictions = list()
        if Algorithm == "NB": predictions = self.runNaiveBayes()
        elif Algorithm == "KNN": predictions = self.runKNN()
        elif Algorithm == "RF": predictions = self.runRandomForest()
        
        if predictions != []:
            print(self.displayAnalytics(predictions))

    def getFiles(self):
        songFile = "songs.csv"
        comparatorFile = "comparator.csv"

        print("Song Playlists: ")
        for index, playlist in enumerate(self.sFiles):
            print(f"{index + 1}. {playlist}")
        songOption = input("Choose playlist: ")

        if int(songOption) - 1 < len(self.sFiles):
            songFile = self.sFiles[int(songOption) - 1]

        print("Comparator Playlists: ")
        for index, playlist in enumerate(self.cFiles):
            print(f"{index + 1}. {playlist}")
        print(f"{len(self.cFiles) + 1}. Choose a year (2019 or earlier)") #2020 will not work for some reason, but 2019 will
        comparatorOption = input("Choose playlist: ")
        
        if int(comparatorOption) == len(self.cFiles) + 1:
            year = int(input("Input a year: "))
            artist_name, track_name, track_id, values = dataOrganization.yearURIs(year)
            self.comparatorURIList, self.comparatorTrackNames = track_id, track_name
            comparatorFile = None
        elif int(comparatorOption) - 1 < len(self.cFiles):
            comparatorFile = self.cFiles[int(comparatorOption) - 1]
        
        return songFile, comparatorFile



