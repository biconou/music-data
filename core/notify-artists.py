#!/usr/bin/python
import inotify.adapters
from allmusic_index_discography import *

i = inotify.adapters.InotifyTree('/mnt/DATA/develop/music-data/data/allmusic/artist/')

for event in i.event_gen(yield_nones=False):
  (_, type_names, path, filename) = event
  for event_type in type_names:
    if event_type == 'IN_CREATE': 
      print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format( path, filename, type_names))
      indexArtist(filename)
