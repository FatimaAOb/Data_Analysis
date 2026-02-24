--Students performance data profiling

--1 Basic overview
SELECT COUNT(*) AS TOTAL_STUDENT
FROM STUDENTS_DATA

SELECT COUNT(DISTINCT id) AS UNIQUE_IDS
FROM STUDENTS_DATA

--2. Check for missing values
SELECT
SUM(CASE WHEN first_name IS NULL THEN 1 ELSE 0 END) AS MISSING_FIRST_NAME, 
SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) AS MISSING_LAST_NAME,
SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS MISSING_GENDER,
SUM(CASE WHEN Grade IS NULL THEN 1 ELSE 0 END) AS MISSING_GRADE,
SUM(CASE WHEN absence_days IS NULL THEN 1 ELSE 0 END) AS MISSING_ABSENCE,
SUM(CASE WHEN tardy_days IS NULL THEN 1 ELSE 0 END) AS MISSING_TARDY,
SUM(CASE WHEN math_grade IS NULL THEN 1 ELSE 0 END) AS MISSING_MATH_GRADE,
SUM(CASE WHEN science_grade IS NULL THEN 1 ELSE 0 END) AS MISSING_SCIENCE_GRADE,
SUM(CASE WHEN english_grade IS NULL THEN 1 ELSE 0 END) AS MISSING_ENGLISH_GRADE,
SUM(CASE WHEN it_grade IS NULL THEN 1 ELSE 0 END) AS MISSING_IT_GRADE
FROM STUDENTS_DATA

--3 Grade level distribution
SELECT Grade, COUNT(*) AS GRADES_COUNT
FROM STUDENTS_DATA
GROUP BY Grade
ORDER BY Grade

--4 Gender distribution
SELECT gender, COUNT(*) AS GENDER_COUNTS
FROM STUDENTS_DATA
GROUP BY gender

--5 Attendance anomolies 
SELECT COUNT(*)	 AS IMPOSSIBLE_RECORDS
FROM STUDENTS_DATA
WHERE (tardy_days + absence_days) >=180
--SELECT id, first_name, last_name, absence_days, tardy_days
--FROM STUDENTS_DATA
--WHERE (tardy_days + absence_days) >180

--6 Grade validity check, grades should be 0-100
SELECT 
COUNT(CASE WHEN math_grade<0 or math_grade>100 THEN 1 END) AS INVALID_MATH,
COUNT(CASE WHEN science_grade>100 or science_grade<0 THEN 1 END) AS INVALID_SCIENCE,
COUNT(CASE WHEN english_grade>100 or english_grade<0 THEN 1 END) AS INVALID_ENGLISH,
COUNT(CASE WHEN it_grade>100 or it_grade<0 THEN 1 END) AS INVALID_IT
FROM STUDENTS_DATA

--7 Failing grades, grades between 0-49
SELECT
SUM(CASE WHEN math_grade >=0 AND math_grade<=49 THEN 1 END) AS FAILING_MATH,
SUM(CASE WHEN science_grade >=0 AND science_grade<=49 THEN 1 END) AS FAILING_SCIENCE,
SUM(CASE WHEN english_grade>=0 AND english_grade<=49 THEN 1 END) AS FAILING_ENGLISH,
SUM(CASE WHEN it_grade>=0 AND it_grade<=49 THEN 1 END) AS FAILING_IT
FROM STUDENTS_DATA

--8 Absence count
SELECT 
SUM(CASE WHEN absence_days =0 THEN 1 ELSE 0 END) AS zero_Days_absence,
SUM(CASE WHEN absence_days BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS days1_5_absence, 
SUM(CASE WHEN absence_days BETWEEN 6 AND 10 THEN 1 ELSE 0 END) AS days6_10_absence,
SUM(cASE WHEN absence_days BETWEEN 11 AND 20 THEN 1 ELSE 0 END) AS days11_20_absence,
SUM(cASE WHEN absence_days >20 THEN 1 ELSE 0 END) AS days_20_plus_absence
FROM STUDENTS_DATA

--9 Grade statistics by subject
SELECT 'Math' AS subject,
AVG(CAST(math_grade AS float)) AS avg_grade,
MIN(math_grade) AS min_grade,
MAX(math_grade) AS max_grade,
STDEV(math_grade) AS std_dev
FROM STUDENTS_DATA
UNION ALL
SELECT 'Science',
AVG(CAST(science_grade AS float)),
MIN(science_grade),
MAX(science_grade),
STDEV(science_grade)
FROM STUDENTS_DATA
UNION ALL
SELECT 'English',
AVG(CAST(english_grade AS float)),
MIN(english_grade),
MAX(english_grade),
STDEV(english_grade)
FROM STUDENTS_DATA
UNION ALL
SELECT 'IT',
AVG(CAST(it_grade AS float)),
MIN(it_grade),
MAX(it_grade),
STDEV(it_grade)
FROM STUDENTS_DATA

--10 Name formatting issues(spaces, special characters)
SELECT id, first_name, last_name
FROM STUDENTS_DATA
WHERE first_name LIKE ' %' OR first_name LIKE '% ' 
	OR last_name LIKE ' %' OR last_name LIKE '% '
	OR first_name LIKE '% %' OR last_name LIKE '% %'