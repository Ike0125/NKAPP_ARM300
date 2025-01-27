-- `trading_calendar` テーブルの最大値を取得
SELECT MAX(trade_date_no) FROM trading_calendar;

-- シーケンスを最大値にリセット（例: 最大値が 590 の場合）
ALTER SEQUENCE trade_date_no_seq RESTART WITH 591;
