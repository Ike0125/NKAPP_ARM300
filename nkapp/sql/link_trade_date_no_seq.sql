ALTER TABLE trading_calendar
ALTER COLUMN trade_date_no SET DEFAULT nextval('trade_date_no_seq');
