# Movie Recommendations in BigQuery ML


----
### Notes

__ **Collaborative Filtering**

- Used to generate product recommendations
    - for users
    - for targeting users for a given product

- Need three columns of data
    - userid, itemid, rating

- Data table can be sparse
    - users don't have to rate all products

- Based on ratings, uses Matrix Factorization to find similar users or
  similar products and predicts ratings for unseen product

- Matrix Factorizaton relies on two vectors, called:
    - user factors: a low-dimensional representation of `user_id`
    - item factors: a low-dimensional representation of `item_id`

- Use BigQuery `model_type='matrix_factorization'`
    - Model creation is CPU intensive and takes up to 40 minutes for a
      dataset with 20M ratings, 138K users and 27K items
..

__ **Steps**

1. Create a dataset and load ratings data into it

2. Explore the ratings data

3. Train the model

4. Use the trained model to make recommendations

5. Make product predictions
..

__ **Load and explore the data**

- Create a dataset using CLI
    - `bq mk --location=EU --dataset movies`

- Load the ratings source files from CSV in Cloud Storage 
    ```
        bq load \
            --source_format=CSV \
            --autodetect \
            --location=EU \
            movies.movielens_ratings \
            gs://dataeng-movielens/ratings.csv
    ```

- Load the movies data from CSV in Cloud Storage
    ```
        bq load \
            --source_format=CSV \
            --autodetect \
            --location=EU \
            movies.movielens_movies_raw \
            gs://dataeng-movielens/movies.csv
    ```

- Explore the data
    ```
        ----- Check uniqueness and counts -----
        SELECT
          COUNT(DISTINCT userId) numUsers,
          COUNT(DISTINCT movieId) numMovies,
          COUNT(*) totalRatings
        FROM
          movies.movielens_ratings


        ----- Look at the records -----
        SELECT
          *
        FROM
          movies.movielens_movies_raw
        WHERE
          movieId < 5


        ----- Create new table with genres column as an ARRAY
        CREATE OR REPLACE TABLE
          movies.movielens_movies AS
        SELECT
          * REPLACE(SPLIT(genres, "|") AS genres)
        FROM
          movies.movielens_movies_raw
    ```
..

__ **Create the model**

- Run query below to create the model:
    ```
        ----- Skip this query cos it takes up to 40mins -----
        CREATE OR REPLACE MODEL
            movies.movie_recommender
        OPTIONS (
            model_type='matrix_factorizatoin',
            user_col='userid',
            item_col='movieid',
            rating_col='rating',
            l2_reg=0.2,
            num_factors=16
        )
        AS
        SELECT userid,
               movieid,
               rating
          FROM movies.movielens_ratings
    ```

- Evaluate the model:
    ```
        SELECT * FROM ML.EVALUATE(
            MODEL `cloud-training-prod-bucket.movies.movie_recommender`
        )
    ```
..

__ **Make recommendations: Recommend movies to user**

- Find best comedy movies for `userId=903`:
    ```
        SELECT *
        FROM ML.PREDICT (
          `cloud-training-prod-bucket.movies.movie_recommender`,
          (
            -- Generate rows of movieId, userId, misc columns like title
            -- and ML.PREDICT will generate ratings field
            SELECT
              movieId,
              title,
              903 as userId
            FROM
              movies.movielens_movies,
              UNNEST(genres) g
            WHERE
              g = 'Comedy'
          )
        )
        ORDER BY
          predicted_rating DESC
        LIMIT
          5
    ```
    - The data is from `movielens_movies` which may include movies that
      user 903 may have rated before.
    - Query below excludes these seen movies
    ```
        SELECT *
        FROM ML.PREDICT (
          `cloud-training-prod-bucket.movies.movie_recommender`,
          (
            WITH seen AS (
              SELECT
                ARRAY_AGG(movieId) AS movies
              FROM
                movies.movielens_ratings
            )
            SELECT
              movieId,
              title,
              903 as userId
            FROM
              movies.movielens_movies,
              UNNEST(genres) g,
              seen
            WHERE
              g = 'Comedy'
              AND movieId NOT IN UNNEST(seen.movies)
          )
        )
        ORDER BY
          predicted_rating DESC
        LIMIT
          5
    ```


..

__ **Make recommendations: Customer targeting (Recommend users to
movie)**

- Scenario: A movie has few ratings, identify users (targets) who will
  likely enjoy that movie
    ```
        SELECT *
        FROM ML.PREDICT(
          `cloud-training-prod-bucket.movies.movie_recommender`,
          (
            WITH allUsers AS (
              SELECT DISTINCT userId
                FROM movies.movielens_ratings
            )
            SELECT
              96481 AS movieID,
              (
                SELECT title
                  FROM movies.movielens_movies
                 WHERE movieId = 96481
              ) AS title,
              userId
            FROM
              allUsers
          )
        )
        ORDER BY
          predicted_rating DESC
        LIMIT 100
    ```
..

__ **Make batch predictions**

```
    SELECT
      *
    FROM
      ML.RECOMMEND(MODEL `cloud-training-prod-bucket.movies.movie_recommender`)
    LIMIT 
      100000
```
..

