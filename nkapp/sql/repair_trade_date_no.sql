DO $$
DECLARE
    row RECORD;
    counter INT := 10000; -- 開始値を10000に設定
BEGIN
    FOR row IN
        SELECT id FROM trading_calendar ORDER BY tradingdate
    LOOP
        UPDATE trading_calendar
        SET trade_date_no = counter
        WHERE id = row.id;
        counter := counter + 1;
    END LOOP;
END $$;
