import userInterface

if __name__ == '__main__':
    sFiles = ["songs.csv", "songs2.csv", "songs3.csv"]
    cFiles = ["comparator.csv", "comparator2.csv", "comparator3.csv"]
    needHelp = False

    Demo = userInterface.Demo(sFiles, cFiles, needHelp)
    Demo.run()
