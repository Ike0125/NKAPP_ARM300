-- シーケンスの状態確認
SELECT * FROM information_schema.sequences WHERE sequence_name = 'trade_date_no_seq';

-- テーブルのデフォルト値確認
SELECT column_name, column_default
FROM information_schema.columns
WHERE table_name = 'trading_calendar';
