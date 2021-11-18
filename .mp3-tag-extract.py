import os
from tinytag import TinyTag, TinyTagException
from pymongo import MongoClient
from mongoengine import *
connect('musics')
import datetime

def mongo_conn():
    try:
        conn = MongoClient(host="127.0.0.1", port=27017)
        print("MongoDB connected", conn)
        return conn.musics
    except Exception as e:
        print("Error in connection", e)

db = mongo_conn()
songs_collections = db['songs']

class SongsInfo(Document):
    title = StringField(required=True)
    artist = ListField(StringField())
    album = StringField()
    year = StringField()
    duration_in_sec = IntField()
    bitrate = IntField()
    lyric = StringField(default=None)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

# print(songs_collections.find({}).count)

def main() :
    print("Start")

    for root, dirs , files, in os.walk('D:\Songs-Zip-File\Hindi\Hindi'): # D:\Songs-Zip-File\Hindi\Hindi'):
        for name in files:
            if name.endswith((".mp3",".m4a")):
                try:
                    temp_track = TinyTag.get(root+ "\\" + name)

                    title = temp_track.title
                    artist = temp_track.artist
                    album = temp_track.album
                    year = temp_track.year
                    duration =  temp_track.duration
                    bitrate = temp_track.bitrate
                    
                    song = SongsInfo(title = title, artist = [artist], album = album, year = year,
                        duration_in_sec = duration, bitrate = bitrate)
                    song.save()
                    # save_all_songs_info.append(song)

                except TinyTagException:
                    print("Error")

    # songs_collections.insert_many(save_all_songs_info)

if __name__ == "__main__":
    main()