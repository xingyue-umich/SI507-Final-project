#################################
##### Name: Xingyue Zhang   #####
##### Uniqname: xingyuez    #####
##### SI 507 Final Project   ####
##### Song recommendations  #####
#################################

import json
import spotipy
import secrets
from functools import cache
from spotipy.oauth2 import SpotifyClientCredentials 
from pprint import pprint


# Step 1
# Get json data from spotify API
@cache
def get_api_data(playlist_id):
    cid = secrets.cid
    client_secret = secrets.client_secret
    playlist_id = playlist_id
    user_id = secrets.user_id

    sp = spotipy.Spotify() 

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=client_secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
    sp.trace=False 
    playlist = sp.user_playlist(user_id, playlist_id) 
    # pprint(playlist)

    songs = playlist["tracks"]["items"] 
    ids = [] 

    for i in range(len(songs)): 
        ids.append(songs[i]["track"]["id"]) 
        
    features = sp.audio_features(ids) 
    
    return features

def combind_play_list(list_of_playlist):
    combined_list = []
    for playlist in list_of_playlist:
        combined_list.extend(playlist)
    return combined_list
# Step 2
# Orgainze data into tree according to the danceability (0-1), energy (0-1)

class Node:
    def __init__(self, song, attribute, songlst = []):
        self.song = song
        self.attribute = attribute
        self.value = round(song[attribute],1)
        self.songlst = songlst
        self.left = None
        self.right = None
       
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, song, attribute):
        new_node = Node(song, attribute, songlst = [])
        if self.root == None:
            self.root = new_node
            self.root.songlst.append(self.root.song)
            return True
        
        temp = self.root
        
        while True:
            if new_node.value == temp.value:
                temp.songlst.append(new_node.song)
                return False
            
            if new_node.value < temp.value:
                if temp.left == None:
                    temp.left = new_node
                    temp.left.songlst.append(new_node.song)
                    return True
                temp = temp.left

            if new_node.value > temp.value:
                if temp.right == None:
                    temp.right = new_node
                    temp.right.songlst.append(new_node.song)
                    return True
                temp = temp.right
    
    def search(self, value):
        temp = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return temp.songlst
        return False
    
    def contains(self, value):
        temp = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False

# Step 3 
# Ask user for input 
def get_user_input():
    print("Song recommendation:\n")
    
    while True:
        danceability = input("How much do you want a dance song? Please input a number from 0 - 1, 0 means absolutely not, 1 means definitely yes: ")
        try:
            danceability = round(float(danceability),1)

        except ValueError:
            print("Please input a number from 0 - 1")
            continue
        
        if danceability < 0 or danceability > 1:
            print("Please input a number from 0 - 1")
            continue
        
        else:
            break
    
    while True:
        valence = input("How much do you want a cheerful song? Please input a number from 0 - 1, 0 means absolutely not, 1 means definitely yes: ")
        try:
            valence = round(float(valence),1)

        except ValueError:
            print("Please input a number from 0 - 1")
            continue
        
        if valence < 0 or valence > 1:
            print("Please input a number from 0 - 1")
            continue
        
        else:
            break
         
    return danceability, valence

# Step 4
# Recommend songs for users 
def get_recommendation(dancebility, valence):

    final_lst = []
    first_lst = danceability_tree.search(dancebility)
    second_lst = valence_tree.search(valence)

# pprint(first_lst)
# pprint(second_lst)

    for song in second_lst:
        if song in first_lst:
            final_lst.append(song)

    return final_lst

def print_songs(final_lst):
    if not final_lst:
        print("Sorry, we don't have recommendations for you now.")
    else:
        print("These songs are perfect for you:")
        for song in final_lst:
            print(song['track_href'])
            
# Implementation            
# Get songs features from play list - "The 1000 best songs on spotify" (But only 100 songs can be extracted, no solutions for now)
features_1 = get_api_data("2S2bAjLaE0CN2V0cTwAeEL")

# Get songs features from play list - "Top tracks of 2020" (50 songs)
features_2 = get_api_data("37i9dQZF1DX7Jl5KP2eZaS")

# Get songs features from play list - "Top tracks of 2021" (50 songs)
features_3 = get_api_data("37i9dQZF1DX18jTM2l2fJY")

# Get songs features from play list - "Jazz classics" (100 songs)
features_4 = get_api_data("37i9dQZF1DXbITWG1ZJKYt")

# Get songs features from play list - "Funk & Soul classic " (80 songs)
features_5 = get_api_data("37i9dQZF1DWWvhKV4FBciw")

features = combind_play_list([features_1, features_2, features_3, features_4, features_5])

# print(len(features))
# pprint(features)

# write feature into json
result = json.dumps(features, indent=2)
# pprint(result)

with open('spotify_data.json', 'w') as file:
    file.write(result)


dancebility, valence = get_user_input() # Ask user for input
# print(dancebility)
# print(valence)

danceability_tree = BinarySearchTree()
for song in features:
    danceability_tree.insert(song, "danceability")
    
# print(danceability_tree.root.songlst)
# print(danceability_tree.root.left.songlst)

# print(danceability_tree.contains(0.6))
# print(danceability_tree.search(0.4))

valence_tree = BinarySearchTree()
for song in features:
    valence_tree.insert(song, "valence")

# print(valence_tree.root.songlst)
# print(valence_tree.root.left.songlst)