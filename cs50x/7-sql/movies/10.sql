-- SELECT name
-- FROM people
-- WHERE id IN (
--     SELECT DISTINCT person_id
--     FROM directors
--     WHERE movie_id IN (
--         SELECT movie_id
--         FROM ratings
--         WHERE rating >= 9
--     )
-- )

SELECT DISTINCT name FROM people
    JOIN directors ON people.id = directors.person_id
    JOIN ratings ON directors.movie_id = ratings.movie_id
    WHERE rating >= 9;