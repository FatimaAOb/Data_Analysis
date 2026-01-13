--Q1. Table structure, data types, nullability
EXEC sp_help 'thread_app';


--Q2. Nulls, distinct values, total rows
SELECT
    COUNT(*) AS total_rows,
    COUNT(thumbs_up) AS non_null_count,
    COUNT(DISTINCT thumbs_up) AS distinct_count,
    SUM(CASE WHEN thumbs_up IS NULL THEN 1 ELSE 0 END) AS null_count
FROM thread_app;

--Q3. Frequency distribution
SELECT
    thumbs_up,
    COUNT(*) AS frequency
FROM thread_app
GROUP BY thumbs_up
ORDER BY frequency DESC;

--Q4. Leading/trailing spaces & empty strings
SELECT *
FROM thread_app
WHERE
    thumbs_up LIKE ' %'
    OR thumbs_up LIKE '% '
    OR thumbs_up = ''
    --OR thumbs_up IS NULL;

--Q5. Min/Max length
SELECT
    MIN(LEN(thumbs_up)) AS min_length,
    MAX(LEN(thumbs_up)) AS max_length
FROM thread_app
WHERE thumbs_up IS NOT NULL;

--Q6. Explicit constraints
--EXEC sp_helpconstraint 'thread_app';