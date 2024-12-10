SELECT date, code, COUNT(*)
FROM daily_quotes
GROUP BY date, code
HAVING COUNT(*) > 1;
