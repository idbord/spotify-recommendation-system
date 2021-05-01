import UserInterface

if __name__ == '__main__':
    """
    If you want to make your own playlist or comparator playlist, please add the
    file name to the lists below.

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
