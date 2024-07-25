-- write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred

SELECT DISTINCT p2.name FROM people AS p1
JOIN stars AS s1 ON s1.person_id = p1.id
JOIN movies AS m ON m.id = s1.movie_id
JOIN stars AS s2 ON s2.movie_id = m.id
JOIN people AS p2 ON p2.id = s2.person_id
WHERE p1.name = "Kevin Bacon" AND p2.name != "Kevin Bacon"
