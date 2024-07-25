-- write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated

SELECT m.title FROM movies AS m
JOIN stars AS s ON s.movie_id = m.id
JOIN people AS p ON p.id = s.person_id
JOIN ratings AS r ON r.movie_id = m.id
WHERE p.name = "Chadwick Boseman"
ORDER BY r.rating DESC
LIMIT 5
