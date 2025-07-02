CREATE DATABASE SPOTIFY_DB_FINAL

// making connection of s3 and snowflake

   CREATE OR REPLACE STORAGE INTEGRATION s3_init2
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::647163884928:role/spotify-spark-role'
STORAGE_ALLOWED_LOCATIONS = ('s3://spotify-etl-glue-project/')
COMMENT = 'Creating connection with S3';

desc integration s3_init2

//create file format

create or replace file format csv_fileformat
type = csv
field_delimiter = ','
skip_header = 1
null_if = ('NULL','null')
empty_field_as_null = TRUE;


// stage

CREATE OR REPLACE STAGE spotify_stage2
URL = 's3://spotify-etl-glue-project/transformed_data/'
STORAGE_INTEGRATION = s3_init2
FILE_FORMAT = csv_fileformat;

list@spotify_stage2/songs

// create tables
create or replace  table tbl_album(
   album_id string,
   album_name string,
   album_release_date date,
   album_total_tracks int,
   url string
   );

create or replace  table tbl_artist(
   artist_id string,
   artist_name string,
   url string
   );

create or replace table tbl_songs(
   song_id string,
   song_name string,
   duration_ms int,
   song_popularity int,
   song_added date,
   album_id string,
   url string,
   artist_id string
   
   );

   select * from tbl_songs

   copy into tbl_songs
   from @spotify_stage2/songs_data/song_transformed_2025-06-30/run-1751295463493-part-r-00000 

      
   
copy into tbl_artist
   from @spotify_stage2/artist_data/artist_transformed_2025-06-30/run-1751275531753-part-r-00000 

COPY INTO tbl_songs 
   FROM @spotify_stage2/songs_data/song_transformed_2025-06-30/run-1751295463493-part-r-00000 
   FILE_FORMAT = (
   TYPE = 'CSV',
   FIELD_OPTIONALLY_ENCLOSED_BY = '"',
   SKIP_HEADER = 1
   );

copy into tbl_album
   from @spotify_stage2/album_data/album_transformed_2025-06-30/run-1751275521778-part-r-00000 


   // create pipeline

   create or replace schema pipe

   CREATE OR REPLACE PIPE pipe.tbl_songs_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO SPOTIFY_DB_FINAL.PUBLIC.TBL_SONGS
  FROM @SPOTIFY_DB_FINAL.PUBLIC.spotify_stage2/songs_data
  FILE_FORMAT = ( 
    TYPE = 'CSV',
    FIELD_OPTIONALLY_ENCLOSED_BY = '"',
    SKIP_HEADER = 1
  );

  create or replace pipe pipe.tbl_artist_pipe
  auto_ingest = TRUE
  as
  copy into SPOTIFY_DB_FINAL.PUBLIC.tbl_artist
  from @SPOTIFY_DB_FINAL.PUBLIC.spotify_stage2/artist_data

  create or replace pipe pipe.tbl_album_pipe
  auto_ingest = TRUE
  as
  copy into SPOTIFY_DB_FINAL.PUBLIC.tbl_album
  from @SPOTIFY_DB_FINAL.PUBLIC.spotify_stage2/album_data

DESC PIPE PIPE.TBL_ARTIST_PIPE
   

SELECT COUNT(*) FROM TBL_ARTIST
select count(*) from tbl_album
select count(*)  from tbl_songs

SELECT SYSTEM$PIPE_STATUS('PIPE.TBL_ARTISTS_PIPE')
   

LIST@spotify_stage2/artist_data;
