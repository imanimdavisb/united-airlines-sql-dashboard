-- Executive KPIs
SELECT
 ROUND(100.0 * SUM(CASE WHEN cancelled=0 AND arrival_delay_minutes<=15 THEN 1 ELSE 0 END)
 / NULLIF(SUM(CASE WHEN cancelled=0 THEN 1 ELSE 0 END),0),2) AS on_time_pct,
 ROUND(AVG(CASE WHEN cancelled=0 THEN arrival_delay_minutes END),2) AS average_delay,
 SUM(cancelled) AS cancelled_flights
FROM flight_operations;

-- Most delayed airport
SELECT origin_airport, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations
WHERE cancelled=0
GROUP BY origin_airport
ORDER BY average_delay DESC
LIMIT 1;

-- Delay reasons
SELECT delay_reason, COUNT(*) AS delayed_flights
FROM flight_operations
WHERE cancelled=0 AND arrival_delay_minutes>15
GROUP BY delay_reason
ORDER BY delayed_flights DESC;

-- Delays by airline
SELECT airline, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations
WHERE cancelled=0
GROUP BY airline
ORDER BY average_delay DESC;

-- Delays by month
SELECT month, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations
WHERE cancelled=0
GROUP BY month
ORDER BY month;

-- Top 10 airports
SELECT origin_airport, COUNT(*) AS total_flights,
 ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations
WHERE cancelled=0
GROUP BY origin_airport
HAVING COUNT(*)>=20
ORDER BY average_delay DESC
LIMIT 10;
