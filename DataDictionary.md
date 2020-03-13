# Data Dictionary

## Variables Used for Modeling

| **Feature**                         | **Type** | **Units**    | **Description**                                                                  |
|-------------------------------------|----------|--------------|----------------------------------------------------------------------------------|
| **Time**                            | DateTime | Hourly       | Time of measurements, used as index                                              |
| **price_actual**                    | Float    | Euros/MWh    | Actual price of one MWh of electricity                                           |
| **price_day_ahead**                 | Float    | Euros/MWh    | Provided forecast price for one MWh of electricity                               |
| **total_load_forecast**             | Float    | MW           | Forecasted MW of electric load demand for each hour from RED Electrica Espana    |
| **forecast_wind_onshore_day_ahead** | Float    | MW           | Forecasted MW of onshore wind generation for each hour from RED Electrica Espana |
| **oil_price**                       | Float    | Euros/Barrel | Historical daily price of a barrel of crude oil                                  |

## Addtional Variables

*TBU*
