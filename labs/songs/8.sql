-- Lists the names of the songs that feature other artists
-- In the name column of songs that feature other artists, there is often a artist_name(feat. another_artist_name)
SELECT name FROM songs WHERE name LIKE '%feat.%';