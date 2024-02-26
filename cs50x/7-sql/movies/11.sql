-- SELECT title
-- FROM movies, stars, people, ratings
-- WHERE ratings.movie_id = movies.id
--     AND movies.id = stars.movie_id
--     AND people.id = stars.person_id
--     AND name = 'Chadwick Boseman'
--     ORDER BY rating DESC LIMIT 5;

SELECT title FROM movies
JOIN ratings ON movies.id = ratings.movie_id
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE name = 'Chadwick Boseman'
ORDER BY rating DESC LIMIT 5;