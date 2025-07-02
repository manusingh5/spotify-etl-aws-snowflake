import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
from pyspark.sql.functions import explode,col,to_date
from datetime import datetime

s3_path = "s3://spotify-etl-glue-project/raw_data/to_processed/"
source_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": [s3_path]},
    
)
spotify_df = source_df.toDF()
df = spotify_df
def process_albums(df):
    df = df.withColumn("items",explode("items")).select(
        col("items.track.album.id").alias("album_id"),
        col("items.track.album.name").alias("album_name"),
        col("items.track.album.release_date").alias("album_release_date"),
        col("items.track.album.total_tracks").alias("album_total_tracks"),
        col("items.track.album.external_urls.spotify").alias("url")
    ).drop_duplicates(['album_id'])
    return df
    

  

    


def process_artists(df):
   df_artist_exploded = df.select(explode(col("items")).alias("item")).select(explode(col("item.track.artists")).alias("artists"))
   df_artist_final = df_artist_exploded.select(
     col("artists.id").alias("artist_id"),
     col("artists.name").alias("artist_name"),
     col("artists.external_urls.spotify").alias("url")
   ).drop_duplicates(['artist_id'])
   return df_artist_final
from pyspark.sql.functions import explode, col, to_date, expr

def process_song(df):
    df_explode = df.select(explode(col("items")).alias("item"))

    df_song = df_explode.select(
        col("item.track.id").alias("song_id"),
        col("item.track.name").alias("song_name"),
        col("item.track.duration_ms").alias("duration_ms"),
        col("item.track.popularity").alias("song_popularity"),
        col("item.added_at").alias("song_added"),
        col("item.track.album.id").alias("album_id"),
        expr("transform(item.track.artists, x -> x.id)").alias("artist_ids"),
        col("item.track.external_urls.spotify").alias("url")
    )

    # Convert artist_ids array to comma-separated string
    df_song = df_song.withColumn("artist_id", expr("concat_ws(',', artist_ids)")) \
                     .drop("artist_ids") \
                     .drop_duplicates(['song_id'])

    df_song = df_song.withColumn("song_added", to_date(col("song_added")))
    
    return df_song


album_df = process_albums(spotify_df)
album_df.show()
artist_df = process_artists(spotify_df)
artist_df.show()
song_df = process_song(spotify_df)
song_df.show(5)
from awsglue.dynamicframe import DynamicFrame

def write_to_s3(df, path_suffix, format_type="csv"):
    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")
    
    glueContext.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        connection_options={"path": f"s3://spotify-etl-glue-project/transformed_data/{path_suffix}/"},
        format=format_type
    )

write_to_s3(album_df, "album_data/album_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")
write_to_s3(artist_df, "artist_data/artist_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")
write_to_s3(song_df, "songs_data/song_transformed_{}".format(datetime.now().strftime("%Y-%m-%d")), "csv")
import boto3

def list_s3_objects(bucket, prefix):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.json')]

bucket_name = 'spotify-etl-glue-project'
prefix = 'raw_data/to_processed/'
spotify_keys = list_s3_objects(bucket_name, prefix)

def move_and_delete_files(spotify_keys, bucket_name):
    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source = {
            'Bucket': bucket_name,  # ✅ FIXED: was 'bucket' which is undefined
            'Key': key
        }
        destination_key = 'raw_data/processed/' + key.split('/')[-1]
       
        # COPY to new location
        s3_resource.meta.client.copy(copy_source, bucket_name, destination_key)

        # DELETE original file
        s3_resource.Object(bucket_name, key).delete()

# ✅ Run this to actually invoke the function
move_and_delete_files(spotify_keys, bucket_name)

job.commit()
