import UserInterface

if __name__ == '__main__':
<<<<<<< HEAD
    songData = readFile("./Playlists/songs2.csv")
    songsURIList, songsTrackNames, songsClassification = dataOrganization.playlistReader(songData)
    songsDataFrame = dataOrganization.buildDataFrame(songsURIList, songsTrackNames, songsClassification)
    songsDataFrameRounded = dataOrganization.roundAndMapValues(songsDataFrame)
    songsDataFrameTestNumpy = songsDataFrameRounded.to_numpy()

    comparatorData = readFile("./Playlists/comparator2.csv")
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
=======
    """
    If you want to make your own playlist or comparator playlist, please add the
    file name to the lists below.
>>>>>>> 185d8767790b75c43644c3f596a6be59fb17ccee

    sFiles = Song files
    sFile format: song,artist,like or not like (1 = like, 0 = do not like) 
    sFile Example: The Box,Roddy Ricch,0

    cFiles = Comparator files
    cFile format: song,artist
    cFile Example: The Box,Roddy Ricch

    Once you are ready to start, just run this main.py file.
    """
    sFiles = ["songs.csv", "songs2.csv"]
    cFiles = ["comparator.csv", "comparator2.csv"]

    Demo = UserInterface.Demo(sFiles, cFiles)
    Demo.run()
