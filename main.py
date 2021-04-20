import dataOrganization
import numpy
from NaiveBayes import *
import pandas

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
    print(y_pred)








