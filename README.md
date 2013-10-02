# tvSort v2.1

Version 2.1 Changelog
---
* ext check now checks for last ext (fixes issues with multiple ext's)

Version 2.0 Changelog
---
* updated with safer copy-then-delete method
* will continue to the next file if the first file already exists in the destination
* added progress bar (http://code.activestate.com/recipes/168639/)

Version 1.1 Changelog
---
* tweaked so that episode 24 of shows are no longer mistaken for the show named 24
* this will no longer work with episodes of the show 24 unless your folder and the episodes are named Twenty Four.

Run tvSort
---
* **you must have python installed on your machine to run this**  
* modify the config file for your setup (see HOW-TO below)  
   you can do this with notepad. I suggest Notepad++  
* run tvSort.pyc  

The config file looks like this:
```
# enter path of show folders
D:\SERVER\TV\
# enter the path of downloaded shows
C:\Users\Kartik\Downloads\
# enter file-exts (space separated)
avi mkv mpg mpeg vob mp4
```

Configure tvSort
---
you need to modify the lines without #'s in them  
the first line should be the path of your folder that contains  
folders with the names of your shows. Example:  
```
D:\SERVER\TV\  
|---Louie\  
|---The Office\  
|...
```
the second line should be the path of your folder that contains  
your downloaded shows, this folder can be unorganized.  
  
the third line should contain all the file exts of shows you download. the ones  
already there should be fine for most.  