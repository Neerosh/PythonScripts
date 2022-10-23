import lyricsgenius, mutagen , os
from decouple import config
from mutagen.id3 import USLT

def FindLyrics(filepath):
  genius = lyricsgenius.Genius(config('GENIUS_ACCESS_TOKEN'))
  #Token require
  
  try:
    filePropertiesEasy = mutagen.File(filepath,easy=True)
    
    song = genius.search_song(filePropertiesEasy["Title"][0], filePropertiesEasy["Artist"][0])
    
    fileProperties = mutagen.File(filepath)
    
    if filepath.endswith('.flac'):
      fileProperties['Lyrics'] = song.lyrics
    else:
      listKeysRemove = []
      for key in fileProperties.keys():
        if key.__contains__('USLT') or key.__contains__('COMM'):
          listKeysRemove.append(key)
          
      for key in listKeysRemove:
          fileProperties.pop(key)
      
      lyrics = song.lyrics
      
      if lyrics.lower().startswith(filePropertiesEasy["Title"][0].lower()+' lyrics'):
        length = len(filePropertiesEasy["Title"][0])+7
        lyrics = lyrics[length:]
        
      if lyrics.lower().endswith('embed'):
        length = len(lyrics)-5
        
        if lyrics[length].isnumeric():
          length -= 1
          
        lyrics = lyrics[0:length]
        
      if lyrics.lower().endswith('you might also like'):
        lyrics = lyrics[0:len(lyrics)-19]

      fileProperties["USLT"] = (USLT(encoding=3, text=lyrics))
      
    fileProperties.save()
  except Exception as ex:
    print(f'Error: {ex}, file: "{filepath}"')

def ScanFolder(folderPath):
  with os.scandir(folderPath) as entryList:
    for entry in entryList:
      if entry.is_file():
          if entry.path.endswith('.mp3') or entry.path.endswith('.flac'):
              FindLyrics(entry.path)
      if entry.is_dir():
          ScanFolder(entry.path)
                     
def Main():
  path = r"D:\Music\Anime"
  ScanFolder(path)
  path = r"D:\Music\Games"
  ScanFolder(path)
  
if __name__ == "__main__":
  Main()