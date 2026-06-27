/*
    analytical_queries.sql

    Project: Online School ETL Pipeline
    Database: SQLite
*/


/* ============================================================
   1. Data overview
   ============================================================ */

-- 1.1 Count rows by table

SELECT 
    'users' AS table_name,
    COUNT(*) AS row_count
FROM users

UNION ALL

SELECT 
    'courses' AS table_name,
    COUNT(*) AS row_count
FROM courses

UNION ALL

SELECT 
    'leads' AS table_name,
    COUNT(*) AS row_count
FROM leads

UNION ALL

SELECT 
    'payments' AS table_name,
    COUNT(*) AS row_count
FROM payments

UNION ALL

SELECT 
    'lessons' AS table_name,
    COUNT(*) AS row_count
FROM lessons;


-- 1.2 Leads by status

SELECT 
   lead_status,
   COUNT(*) AS leads_count
FROM leads
GROUP BY lead_status
ORDER BY leads_count DESC;


-- 1.3 Payments by status

SELECT 
   payment_status,
   COUNT(*) AS payments_count
FROM payments 
GROUP BY payment_status
ORDER BY payments_count DESC;


-- 1.4 Lessons by attendance status

SELECT 
   attendance_status,
   COUNT(*) AS attendance_count
FROM lessons 
GROUP BY attendance_status
ORDER BY attendance_count DESC;


-- 1.5 Lessons by lesson type

SELECT 
   lesson_type,
   COUNT(*) AS lessons_count
FROM lessons 
GROUP BY lesson_type
ORDER BY lessons_count DESC;


/* ============================================================
   2. Revenue analysis
   ============================================================ */

-- 2.1 Total paid revenue

SELECT 
   SUM(amount) AS total_paid_revenue
FROM payments
WHERE payment_status = 'paid';


-- 2.2 Revenue by course

SELECT 
   courses.course_name AS course,
   SUM(payments.amount) AS revenue
FROM courses
JOIN payments
   ON courses.course_id = payments.course_id
WHERE payments.payment_status = 'paid'
GROUP BY 
   courses.course_id,
   courses.course_name
ORDER BY revenue DESC;


/* ============================================================
   3. Course demand analysis
   ============================================================ */

-- 3.1 Leads by course

SELECT 
   courses.course_name AS course,
   COUNT(leads.lead_id) AS leads_count
FROM courses
LEFT JOIN leads
   ON courses.course_id = leads.course_id
GROUP BY 
   courses.course_id, 
   courses.course_name
ORDER BY leads_count DESC;


-- 3.2 Leads by course and status

SELECT 
   courses.course_name AS course,
   leads.lead_status AS status,
   COUNT(*) AS leads_count
FROM courses
JOIN leads
   ON courses.course_id = leads.course_id
GROUP BY 
   courses.course_id, 
   courses.course_name, 
   leads.lead_status
ORDER BY 
   course,
   leads_count DESC;


/* ============================================================
   4. Conversion analysis
   ============================================================ */

-- 4.1 Lead-to-payment conversion by course

WITH total_leads_table AS (
   SELECT 
      courses.course_id,
      courses.course_name AS course,
      COUNT(leads.lead_id) AS total_leads
   FROM courses
   LEFT JOIN leads
      ON courses.course_id = leads.course_id
   GROUP BY
      courses.course_id,
      courses.course_name
), 

paid_payments_table AS (
   SELECT 
      courses.course_id,
      COUNT(payments.payment_id) AS paid_payments
   FROM courses
   LEFT JOIN payments
      ON courses.course_id = payments.course_id
      AND payments.payment_status = 'paid'
   GROUP BY
      courses.course_id
)

SELECT 
   total_leads_table.course AS course,
   total_leads_table.total_leads AS total_leads,
   COALESCE(paid_payments_table.paid_payments, 0) AS paid_payments,
   ROUND(
      1.0 * 
      COALESCE(paid_payments_table.paid_payments, 0) / 
      NULLIF(total_leads_table.total_leads, 0),
      4
   ) AS payment_conversion_rate
FROM total_leads_table
LEFT JOIN paid_payments_table
   ON total_leads_table.course_id = paid_payments_table.course_id
ORDER BY payment_conversion_rate DESC;


/* ============================================================
   5. Attendance analysis
   ============================================================ */

-- 5.1 Attendance rate by course

WITH lessons_count_by_course AS (
   SELECT
      courses.course_id,
      courses.course_name AS course,
      COUNT(lessons.lesson_id) AS total_lessons
   FROM courses
   LEFT JOIN lessons
      ON courses.course_id = lessons.course_id
   GROUP BY 
      courses.course_id, 
      courses.course_name
),

attendance_by_course AS (
   SELECT
      courses.course_id,
      COUNT(lessons.lesson_id) AS attended_lessons
   FROM courses
   LEFT JOIN lessons
      ON courses.course_id = lessons.course_id
      AND lessons.attendance_status = 'attended'
   GROUP BY 
      courses.course_id
)

SELECT
   lessons_count_by_course.course AS course,
   lessons_count_by_course.total_lessons AS total_lessons,
   COALESCE(attendance_by_course.attended_lessons, 0) AS attended_lessons,
   ROUND(
      1.0 *
      COALESCE(attendance_by_course.attended_lessons, 0) /
      NULLIF(lessons_count_by_course.total_lessons, 0),
      4
   ) AS attendance_rate
FROM lessons_count_by_course
LEFT JOIN attendance_by_course
   ON lessons_count_by_course.course_id = attendance_by_course.course_id
ORDER BY attendance_rate DESC;