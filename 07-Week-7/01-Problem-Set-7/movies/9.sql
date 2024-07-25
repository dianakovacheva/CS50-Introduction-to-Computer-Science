-- write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year

SELECT DISTINCT p.name FROM people AS p
JOIN stars AS s ON s.person_id = p.id
JOIN movies AS m ON m.id = s.movie_id
WHERE m.year = 2004
ORDER BY p.birth ASC
