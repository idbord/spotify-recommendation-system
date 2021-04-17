import dataOrganization

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

    artistList, trackList, uriList = dataOrganization.yearURIs(2020)

    dataFrame = dataOrganization.buildDataFrame(uriList, trackList)
    dataframe = dataOrganization.roundAndMapValues(dataFrame)
    print(dataframe)
