SELECT 
    i.indexname AS index_name,
    i.tablename AS table_name
FROM 
    pg_indexes i
WHERE 
    schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY 
    table_name, index_name;
