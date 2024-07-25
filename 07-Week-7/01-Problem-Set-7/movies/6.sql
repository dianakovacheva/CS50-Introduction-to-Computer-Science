-- write a SQL query to determine the average rating of all movies released in 2012

SELECT AVG(rating) FROM ratings AS r
JOIN movies AS m ON m.id = r.movie_id
WHERE m.year = 2012
