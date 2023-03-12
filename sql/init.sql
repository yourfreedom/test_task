CREATE TABLE IF NOT EXISTS test_table(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company VARCHAR(20) NOT NULL,
    fact_Qliq_data1 INTEGER NOT NULL,
    fact_Qliq_data2 INTEGER NOT NULL,
    fact_Qoil_data1 INTEGER NOT NULL,
    fact_Qoil_data2 INTEGER NOT NULL,
    forecast_Qliq_data1 INTEGER NOT NULL,
    forecast_Qliq_data2 INTEGER NOT NULL,
    forecast_Qoil_data1 INTEGER NOT NULL,
    forecast_Qoil_data2 INTEGER NOT NULL,
    date DATE
);
