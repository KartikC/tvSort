"""
file: tvSort.py
language: python3
authors: Kartik Sathappan
description: sort tv shows
version: 2.0
"""
import os
import shutil
import time
import sys

TOP_PATH = ""
DOWNLOAD_PATH = ""
WRITE_SPEED = 0
LIST_OF_EXTS = []
LIST_OF_SHOWS = {}
LIST_OF_EPISODES = []

class Episode(object):
    """
     An Episode with a tag, and filename, and destination
    """
    __slots__ = ('tag', 'source', 'filename', 'destination')
    
    def __init__(self, tag, source, filename, destination):
        """
        __init__: Episode * String * String * String * String -> Episode
        """
        self.tag = tag
        self.source = source
        self.filename = filename
        self.destination = destination
        
    def __str__(self):
        """
        __str__ : Episode -> String
        """
        return self.tag + "\n" + self.filename + "\n" + self.destination

def getPaths():
    global TOP_PATH
    global DOWNLOAD_PATH
    global LIST_OF_EXTS
    global WRITE_SPEED
    file = open( "config.cfg" )
    for i, line in enumerate(file):
        if i == 1:
            TOP_PATH = line.strip().lower()
        elif i == 3:
            DOWNLOAD_PATH = line.strip().lower()
        elif i == 5:
            LIST_OF_EXTS = line.strip().split()
        elif i > 5:
            break
    file.close()
    #word = word.strip(",.\"\';:-!?").lower()

def getShows():
    global LIST_OF_SHOWS
    for filename in os.listdir(TOP_PATH):
        if os.path.isdir(TOP_PATH + filename):
            temp = ''.join(e for e in filename if e.isalnum() or e == '(' or e == ')')
            if temp.find('(') != -1:
                temp = temp[:temp.find('(')]
            key = temp.lower()
            LIST_OF_SHOWS[key] = TOP_PATH + filename + "\\"

def getEpisodes():
    global LIST_OF_EPISODES
    for filename in os.listdir(DOWNLOAD_PATH):
        for ext in LIST_OF_EXTS:
            if ext in filename[len(filename)-4:]:
                for key in LIST_OF_SHOWS:
                    temp = ''.join(e for e in filename if e.isalnum())
                    if key in temp.lower():
                        temp = Episode( key, DOWNLOAD_PATH + filename, filename, LIST_OF_SHOWS[key] + filename )
                        LIST_OF_EPISODES.append( temp )

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('transfer time: ' + str(int(te-ts)) + 's')
        return result

    return timed

def moveFiles():
    for episode in LIST_OF_EPISODES:
        if episode.tag != '24':
            print("moving: " + episode.tag)
            move(episode.source, episode.destination)
            print("done!")
            print("\n")
            
@timeit
def move(src, dst):
    if os.path.isfile(dst):
        print(dst + ' already exists!')
    else:
        copy_with_prog(src, dst)
	
class ProgressBar:
    # From http://code.activestate.com/recipes/168639/
    def __init__(self, minValue = 0, maxValue = 10, totalWidth=12):
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done 
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = round(percentDone)
        percentDone = int(percentDone)

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # build a progress bar with hashes and spaces
        self.progBar = "[" + '#'*numHashes + ' '*(allFull-numHashes) + "]"

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone)) 
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = (self.progBar[0:percentPlace] + percentString
                        + self.progBar[percentPlace+len(percentString):])

    def __str__(self):
        return str(self.progBar)

def copy_with_prog(src_file, dest_file, overwrite = False, block_size = 16384):
    if not overwrite:
        if os.path.isfile(dest_file):
            raise IOError("File exists, not overwriting")
    
    # Open src and dest files, get src file size
    src = open(src_file, "rb")
    dest = open(dest_file, "wb")

    src_size = os.stat(src_file).st_size
    
    # Set progress bar
    prgb = ProgressBar(totalWidth = 79, maxValue = src_size)
    
    # Start copying file
    cur_block_pos = 0 # a running total of current position
    while True:
        cur_block = src.read(block_size)
        
        # Update progress bar
        prgb.updateAmount(cur_block_pos)
        cur_block_pos += block_size
        
        sys.stdout.write(
            '\r%s\r' % str(prgb)
        )
        
        # If it's the end of file
        if not cur_block:
            # ..write new line to prevent messing up terminal
            sys.stderr.write('\n')
            break
        else:
            # ..if not, write the block and continue
            dest.write(cur_block)
    #end while

    # Close files
    src.close()
    dest.close()

    # Check output file is same size as input one!
    dest_size = os.stat(dest_file).st_size

    if dest_size != src_size:
        raise IOError(
            "New file-size does not match original (src: %s, dest: %s)" % (
            src_size, dest_size)
        )
    else:
        os.remove(src_file)

    

def main():
    getPaths()
    print(TOP_PATH)
    print(DOWNLOAD_PATH)
    print(LIST_OF_EXTS)
    print("\n")
    getShows()
    getEpisodes()
    moveFiles()
    if len(LIST_OF_EPISODES) < 1:
        print('No files to move')
    os.system("pause")

if __name__ == "__main__":
    main()
