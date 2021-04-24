import dataOrganization
import numpy
from NaiveBayes import *
from KNearestNeighbor import *
from KMeans import *

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
    data = readFile("./songs.csv")
    turiList, ttrackName, values = dataOrganization.playlistReader(data)
    dataFrameTest = dataOrganization.buildDataFrame(turiList, ttrackName, values)
    dataFrameTest = dataOrganization.roundAndMapValues(dataFrameTest)
    dataFrameTest = dataFrameTest.to_numpy()

    data = readFile("./comparator.csv")
    turiList, ttrackName = dataOrganization.playlistReaderCompare(data)
    dataFrameTest2 = dataOrganization.buildDataFrameCompare(turiList, ttrackName)
    dataFrameTest2 = dataOrganization.roundAndMapValues(dataFrameTest2)
    dataFrameTest2 = dataFrameTest2.to_numpy() # Could probably add this to a method in organization


    dataFrameTrainX = dataFrameTest[:,0:11]
    dataFrameTrainY = dataFrameTest[:,11:]
    dataFrameTrainY = numpy.concatenate(dataFrameTrainY, axis=0)

    dataFrameTestX = dataFrameTest2[:,0:11]


    nb = NaiveBayes(dataFrameTrainX,dataFrameTrainY)
    nb.fit(dataFrameTrainX,dataFrameTrainY)
    y_pred = nb.predict(dataFrameTestX)


    print("Possible playlist:")
    for _ in range(len(y_pred)):
        status = "No"
        if y_pred[_] == 1:
            status = "Yes"
        print(f"{ttrackName[_]} by {ttrackName[_]}: {status}")

    KNNTest = KNN(3)
    KNNTest.fit(dataFrameTrainX, dataFrameTrainY)
    predictions = KNNTest.predict(dataFrameTestX)
    print(predictions)
