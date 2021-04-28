import UserInterface

if __name__ == '__main__':
    sFiles = ["songs.csv", "songs2.csv"]
    cFiles = ["comparator.csv", "comparator2.csv"]

    Demo = UserInterface.Demo(sFiles, cFiles)
    Demo.run()
