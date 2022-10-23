import lyricsgenius, mutagen , os
from decouple import config
from mutagen.id3 import USLT

def CleanLyrics(song,filePropertiesEasy):
  artist = filePropertiesEasy["Artist"][0].lower().strip()
  title = filePropertiesEasy["Title"][0].lower().strip()
  songTitle = song.title.lower().strip()
  songArtist = song.artist.lower().strip()
  
  if (not songArtist.__contains__(artist)) or songTitle != title:
    print('Artist or Title do not match.')
    return ''
  
  lyrics = song.lyrics
  
  if lyrics.lower().startswith(filePropertiesEasy["Title"][0].lower()+' lyrics'):
    length = len(filePropertiesEasy["Title"][0])+7
    lyrics = lyrics[length:]
      
  if lyrics.lower().endswith('embed'):
    length = len(lyrics)-5
    
    if lyrics[length-1].isnumeric():
      length -= 1
    
    
    lyrics = lyrics[0:length]
    
  if lyrics.lower().endswith('you might also like'):
    lyrics = lyrics[0:len(lyrics)-19]
      
  return lyrics

def FindLyrics(filepath):
  genius = lyricsgenius.Genius(config('GENIUS_ACCESS_TOKEN'),skip_non_songs=True)
  #Token require
  
  try:
    filePropertiesEasy = mutagen.File(filepath,easy=True)
    if filePropertiesEasy == None:
      raise Exception("Error creating filePropertiesEasy")
    
    fileProperties = mutagen.File(filepath)
    if fileProperties == None:
      raise Exception("Error creating fileProperties")
    
    if filepath.endswith('.flac') and fileProperties.keys().__contains__('lyrics'):
      if len(fileProperties['Lyrics']) > 0:
        raise Exception("File Already contains lyrics skipping...")
    else:
      for key in fileProperties.keys():
        if key.__contains__('USLT'):
          raise Exception("File Already contains lyrics skipping...")
    

    song = genius.search_song(filePropertiesEasy["Title"][0], filePropertiesEasy["Artist"][0])
    if song == None:
      raise Exception("Error song not found")

    lyrics = CleanLyrics(song,filePropertiesEasy)
       
    if filepath.endswith('.flac'):
      fileProperties['Lyrics'] = lyrics
    else:
      listKeysRemove = []
      for key in fileProperties.keys():
        if key.__contains__('USLT') or key.__contains__('COMM'):
          listKeysRemove.append(key)
          
      for key in listKeysRemove:
          fileProperties.pop(key)

      fileProperties["USLT"] = (USLT(encoding=3, text=lyrics))
      
    fileProperties.save()
  except Exception as ex:
    print(f'{ex}, file: "{filepath}"')

def ScanFolder(folderPath):
  with os.scandir(folderPath) as entryList:
    for entry in entryList:
      if entry.is_file():
          if entry.path.endswith('.mp3') or entry.path.endswith('.flac'):
              FindLyrics(entry.path)
      if entry.is_dir():
          ScanFolder(entry.path)
                     
def Main():
  #path = r"D:\Music\Anime"
  #ScanFolder(path)
  #path = r"D:\Music\Games"
  #ScanFolder(path)
  path = r'D:\Music\Anime\Jeff Williams - RWBY\RWBY Volume 1 (2013)\CD1 - Soundtrack'
  ScanFolder(path)
  
if __name__ == "__main__":
  Main()