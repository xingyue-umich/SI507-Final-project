# :notes: SI 507 Final project - Song recommendations based on features

This project is designed to recommend songs based on features, e.g. song's danceability and valence.
After implementing the interactive command line tool,
the users will be asked questions about how much they want the songs with specific features and they need to enter a number to quantify their request
then users will get recommendations in the form of track url based on their requests.

## Data collections

### Data source

- [Spotify API](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features)
- In order to get access to the data, you may need to obtain client id, client secret from [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)

### Data format

- Json

``` json
[
  {
    "danceability": 0.779,
    "energy": 0.64,
    "key": 7,
    "loudness": -8.415,
    "mode": 1,
    "speechiness": 0.159,
    "acousticness": 0.000155,
    "instrumentalness": 0.00077,
    "liveness": 0.101,
    "valence": 0.498,
    "tempo": 99.019,
    "type": "audio_features",
    "id": "4TsmezEQVSZNNPv5RJ65Ov",
    "uri": "spotify:track:4TsmezEQVSZNNPv5RJ65Ov",
    "track_href": "https://api.spotify.com/v1/tracks/4TsmezEQVSZNNPv5RJ65Ov",
    "analysis_url": "https://api.spotify.com/v1/audio-analysis/4TsmezEQVSZNNPv5RJ65Ov",
    "duration_ms": 246960,
    "time_signature": 4
  }, ...]
```

### Data features

Audio features are described in [Spotify's API documentation](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features) <br>
Following are two features used in this project:

- **Danceability** : describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **Valence**: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

## Installing

In order to configure this project, please follow these steps:

1. Clone the repository to your local system.

    ``` git
    git clone https://github.com/xingyue-umich/SI507-Final-project.git
    ```

2. Create the secrets.py file with the necessary API keys. *(This file was turned in to final project assignment on Canvas)* For other purpoes, please request a free API key from [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)

3. Put secrets.py at the root level in the final project directory.

## Run the application

The "final.py" file will initiate the program.

``` python
python3 FinProj.py
```

User will be asked two questions: <br>
:question: How much do you want a dance song? <br>
:question: How much do you want a cheerful song? <br>

User needs to input a number between 0 - 1 *(0 means absolutely not, 1 means definitely yes)*

Songs met users' requirement will be recommended in the format of sportify url link <br>

```
These songs are perfect for you:
https://api.spotify.com/v1/tracks/3FAJ6O0NOHQV8Mc5Ri6ENp
https://api.spotify.com/v1/tracks/0Otf1ZfYNIjhqFIuJk0fsy
```

## Data Structure

**Binary search tree** has been used to orgainze the data based on the features e.g. danceability, valence.<br>

### Node

- The **value** of the tree node is the value of associate feature of the song, e.g. danceability, valence. (rounded to 1-digit) <br>

- The **songlst** of the tree node is a list that stores all the songs have the same value of that feature (i.e. if value = 0.4, attribute = danceability, the songlst will store all the songs that have the danceability of 0.4)

``` python
class Node:
    def __init__(self, song, attribute, songlst = []):
        self.song = song
        self.attribute = attribute
        self.value = round(song[attribute],1)
        self.songlst = songlst
        self.left = None
        self.right = None
```

### Search and Insert

- Song that has the same value as the node will be inserted into the songlst of that node

- A list of songs (songlst) along with attributes associated will be returned when **search** function is called.

```
song_list = danceability_tree.search(0.1)
pprint(song_list)
```

``` 
[{'acousticness': 0.965,
  'analysis_url': 'https://api.spotify.com/v1/audio-analysis/7KsJkshpIjjeIwyKnkhQUc',
  'danceability': 0.147,
  'duration_ms': 266800,
  'energy': 0.215,
  'id': '7KsJkshpIjjeIwyKnkhQUc',
  'instrumentalness': 0.000928,
  'key': 3,
  'liveness': 0.184,
  'loudness': -14.594,
  'mode': 0,
  'speechiness': 0.0346,
  'tempo': 171.46,
  'time_signature': 3,
  'track_href': 'https://api.spotify.com/v1/tracks/7KsJkshpIjjeIwyKnkhQUc',
  'type': 'audio_features',
  'uri': 'spotify:track:7KsJkshpIjjeIwyKnkhQUc',
  'valence': 0.102}]
```

- User can also check whether the tree contains a value by calling contains function

``` python
if danceability_tree.contains(0.5):
    print('Yes! There are some songs with danceability of 0.5')
else:
    print('Nope! There are no songs with danceability of 0.5')
```

```
Yes! There are some songs with danceability of 0.5
```

## Built With


- Python3
- Packages:
  - [spotipy](https://spotipy.readthedocs.io/en/2.19.0/) package has been used to help fetch data from Spotify API
  - cache in [functools](https://docs.python.org/3/library/functools.html) package has been used to speed up the data access and storage
  - [pprint](https://docs.python.org/3/library/pprint.html) has been used to print well-formatted, more readable result
