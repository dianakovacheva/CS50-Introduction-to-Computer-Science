/* write a SQL query that returns the average energy of songs that are by Drake. */

SELECT AVG(energy) FROM songs AS s
JOIN artists AS a ON s.artist_id == a.id
WHERE a.name = "Drake";
