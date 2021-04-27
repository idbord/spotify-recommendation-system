import dataOrganization
import numpy
from NaiveBayes import *
from KNearestNeighbor import *
from RandomForest import *
from sklearn.ensemble import RandomForestClassifier

def readFile(path):
    try:
        fptr = open(path)
        result = []
        for line in fptr.readlines():
            result.append(line[:-1].split(","))
        return result

    except:
        return []


if __name__ == '__main__':
    songData = readFile("./songs2.csv")
    songsURIList, songsTrackNames, songsClassification = dataOrganization.playlistReader(songData)
    songsDataFrame = dataOrganization.buildDataFrame(songsURIList, songsTrackNames, songsClassification)
    songsDataFrameRounded = dataOrganization.roundAndMapValues(songsDataFrame)
    songsDataFrameTestNumpy = songsDataFrameRounded.to_numpy()

    comparatorData = readFile("./comparator2.csv")
    comparatorURIList, comparatorTrackNames = dataOrganization.playlistReaderCompare(comparatorData)
    comparatorDataFrame = dataOrganization.buildDataFrameCompare(comparatorURIList, comparatorTrackNames)
    comparatorDataFrameRounded = dataOrganization.roundAndMapValues(comparatorDataFrame)
    comparatorsDataFrameTestNumpy = comparatorDataFrameRounded.to_numpy() # Could probably add this to a method in organization


    dataFrameTrainX = songsDataFrameTestNumpy[:,0:11]
    dataFrameTrainY = songsDataFrameTestNumpy[:,11:]
    dataFrameTrainY = numpy.concatenate(dataFrameTrainY, axis=0)
    dataFrameTestX = comparatorsDataFrameTestNumpy[:,0:11]


    nb = NaiveBayes(dataFrameTrainX,dataFrameTrainY)
    nb.fit(dataFrameTrainX,dataFrameTrainY)
    y_pred = nb.predict(dataFrameTestX)

    tempURIList, tempTrackNames = list(), list()
    for _ in range(len(y_pred)):
        if y_pred[_] == 1:
            tempURIList.append(comparatorURIList[_])
            tempTrackNames.append(comparatorTrackNames[_])

    comparatorPlayListUpdated = dataOrganization.buildDataFrame(tempURIList, tempTrackNames, [1] * len(tempURIList))
    comparatorPlayListUpdated = dataOrganization.roundAndMapValues(comparatorPlayListUpdated)

    songsTable = analytics.findAverage(songsDataFrameRounded, "Songs")
    analyticsTable = analytics.dataTable(songsTable, comparatorPlayListUpdated.transpose())
    print(analyticsTable)


    KNNTest = KNN(3)
    KNNTest.fit(dataFrameTrainX, dataFrameTrainY)
    predictions = KNNTest.predict(dataFrameTestX)
    print(predictions)

    rf = RandomForest(100)
    rf.fitLocal(dataFrameTrainX,dataFrameTrainY)
    print(rf.prediction(dataFrameTestX))