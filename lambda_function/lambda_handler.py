import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    playlist_link = "https://open.spotify.com/playlist/3jBzuxVcBq3AJAYGDKyhgz"
    playlist_uri = playlist_link.split("/")[-1]

    data = sp.playlist_tracks(playlist_uri)
    
   

    client = boto3.client('s3')
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    client.put_object(
        Bucket = "spotify-etl-glue-project",
        Key = "raw_data/to_processed/" + filename,
        Body = json.dumps(data) 
    )

    glue = boto3.client('glue')
    gluejobname = "spotify_transformation_job"

    try:
        runid = glue.start_job_run(JobName=gluejobname)
        status = glue.get_job_run(JobName=gluejobname, RunId=runid['JobRunId'])
        print("Job Status: ", status['JobRun']['JobRunState'])
    except Exception as e:
        print(e)
