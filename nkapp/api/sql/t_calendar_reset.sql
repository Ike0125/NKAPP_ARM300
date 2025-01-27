DO $$
DECLARE
    rec RECORD;
    new_no INT := 1;
BEGIN
    FOR rec IN
        SELECT id
        FROM trading_calendar
        ORDER BY tradingdate
    LOOP
        UPDATE trading_calendar
        SET trade_date_no = new_no
        WHERE id = rec.id;
        new_no := new_no + 1;
    END LOOP;
END $$;
