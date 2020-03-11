# Technical Report

Details the technical approach taken for the project including:
- [Problem Statement](#Problem-Statement)
- [Cleaning & Transforming Data](#Cleaning-&-Transforming-Data)
  - Data Sources & Summary
  - Cleaning
  - Transforming
- [Modeling](#Modeling)
  - Assumptions
  - Baseline
  - Models & Tuning
  - Evaluation Metrics
- [Summary Metrics](#Summary-Metrics)
  - Evaluation Statistics
  - Predictions by Hour
- [Production Model](#Production-Model)
  - Model Discussion
  - Performance
- [Future Work](#Future-Work)

## Problem Statement

Predict electricity prices in Spain for each hour of the upcoming day more accurately than estimates provided by the Spanish transmission agent and operator. 

Use information available during the 2pm-3pm window the previous day during which generators in Spain submit their bids. 

## Cleaning & Transforming Data

**Data Sources & Summary**<br>
The primary data set for this project was provide on [kaggle](https://www.kaggle.com/nicholasjhana/energy-consumption-generation-prices-and-weather) by Nicholas Jhana and contains 29 columns of electricity price & generation data for all of Spain for every hour from January 1, 2014 to December 31, 2018 (35064 unique hours of data). 

Additionally Nicholas provided actual weather data for the same time period for the 5 largest cities in Spain, which was not included due to it being actual rather than forecasted data. However, I hope to include either that data or source weather predictions for future iterations.

The final data included in the is daily crude oil prices in euros, scraped from [exchangerates.org.uk](https://www.exchangerates.org.uk/commodities/OIL-EUR-history.html). This data was gathered due to supplement the generation, load and price data as fuel burning sources are often the [price setters](https://www.businessjuice.co.uk/energy-guides/what-drives-the-price-of-electricity/) in electric markets.

**Cleaning**:<br>
Minimal cleaning of data was required with a maximum of 19 missing data points out of 35064 for any variable used for modeling. The method used to fill any missing data was *linear interpolation*. This method was chosen due to the variable, time series nature of the data and the gaps in data being small. Thus, linear interpolation allowed us to connect the previous non-missing data point and the next non-missing data point. While this is not a perfect method and likely understates the variance of the underlying data it seemed to be superior to other potential methods and overall should not have a large effect on our results since there was very little missing data.

Plots showing the filling of missing data using linear interpolation. Note that this shows the only gap larger than 1 hour in the data and the resulting plot is quite 'believable' apart from the solar data. Additionally there were no missing data points in our variables used currently in the model, with the exception of 2 missing days of oil prices.

*Before Linear Interpolation*
![Before Linear Interpolation](./Visuals/top_gen_missing.png)

*After Linear Interpolation*
![After Linear Interpolation](./Visuals/top_generation.png)

**Transforming**:<br>
The only transformation of data performed was to get all of our X and y variables onto the same row of the data frame in order to facilitate modeling. This was accomplished using the *shift* method and resulted in each day having a single row with the following data points:
- The actual, hourly electric prices for the next day (our target)
- The projected, hourly total load and wind generation for the next day (information available from the operator)
- The actual, hourly electric prices from the begining of the previous day up to and including the 2pm-3pm time slot (known previous prices)
- The projected, hourly prices for the current day from 3pm - midnight (results of previous days bids)
- The actual crude oil price for the current day

These transformations also got rid of all of our detailed information on generation from different sources. This is because that generation is determined based on the auction (with the exception of wind and solar which produce what they produce) and thus can't be known until the auction is completed and further the day ahead actually procedes and any spikes / dips in demand occur.

Additionally, given time constraints, weather projections have not been included in the analysis as of yet, but this is a near-term area of further iteration and improvement.

## Modeling

**Assumptions**<br>
*Time Series*<br>
The primary assumption necessary for time series models is that we are modeling a stationary process ([a stochastic process whose unconditional joint probability distribution does not change when shifted in time](https://en.wikipedia.org/wiki/Stationary_process)). I tested this assumption using an ADFuller test on our target variable of electric prices. The resultant p-value was 2.75E-15, an extremely low value was sufficient for me to reject the null hypothesis of the data not being stationary and allowed for modeling directly using price, without need for differencing or another technique to generate stationarity.

![energy prices](./Visuals/prices.png)

*Linear Modeling Assumptions*

*TBU*

**Baseline & Evaluation Metrics**:<br>
The baseline against which we compared our models was day ahead prices provided in the original data set. These prices were not particularly accurate, generally underestimating the actual price, with a correlation of 0.73 with the actual prices and the following scores on the 2 metrics we used for evaluation:
- RMSE: €13.25
- R-Squared: 0.13

**Models & Tuning**<br>
The models tested fell broadly into 3 groups: standard regressors, vector auto regressors and neural nets. For all models the 4 years of data was split into 3 years of train data and 1 year of test data and the grid searches used sklearn's TimeSeriesSplit with 4 splits to determine the best model. 

Below is a summary of the various models within each group and the hyperparameters tuned for each one (tuned parameter values in parentheses).

*Standard Regressors*<br>
A grouping of widely used regressors found in the sklearn library
- Linear Regression
  - No tuning
- Elastic Net Regression
  - alpha: regularization strength (0.01)
  - l1 ratio: LASSO vs Ridge regularization (1)
- K Nearest Neighbors Regression
  - n neighbors: how many neighbors are considered when predicting (11)
- Random Forest
  - n estimators: number of trees created (100)
  - max depth: how deep each tree can go (None)
  - min samples leaf: fewest number of samples allowed at each leaf node (1)
  - warm start: whether to reuse the solution to the previous call to fit and add more estimators (False)
  - min_samples_split: minimum number of samples at a leaf to allow splitting further (2)
- AdaBoost
  - loss: loss function used (linear)
  - n estimators: number of estimators (100)
- Support Vector Regressor
  - C: inverse regularization strength (1)
  - kernel: kernel type used in the algorithm (linear)
  - gamma: kernel coefficient (not used with linear kernel)
  
*Vector Auto Regressors*<br>
A family of popular regressors that use past y variables to predict new ones simultaneously. Due to difficulties in incorporating new observations in predictions it is difficult to make a 1 to 1 comparison with other model types and full evaluation of these model types is a future project. Model types that will be considered.
- VAR
- VARMAX (VAR model that also includes exogeneous variables)

*Neural Networks*<br>
Three neural networks that are common in time series analysis were fit to the data. All models used dropouts to avoid overfitting and a single hidden layer after the network specific layer (i.e. convolutional layer(s) for a CNN)
- Recurrent Neural Network (RNN)
  - adsf
- Convolutional Neural Network (CNN)
  - kernel size: length of 1D convlution window (15)
  - pool size: size of pooling window (2)
  - dropout: % of nodes that are dropped while fitting (0.25)
  - units: nodes in hidden layer (80)
- Long Short Term Memory (LSTM)
  - lstm layer size (103)
  - units: nodes in hidden layer (80)
  - dropout: % of nodes that are dropped while fitting (0.5)
  
## Evaluation

**Summary Metrics**<br>
| **Model**   | **Baseline** | **Linear Regression** | **Elastic Net** | **KNN** | **Random Forest** | **AdaBoost** | **SVR** | **VAR** | **VARMAX** | **RNN** | **CNN** | **LTSM** |
|-------------|--------------|-----------------------|-----------------|---------|-------------------|--------------|---------|---------|------------|---------|---------|----------|
| *Test RMSE* | €13.25       | €5.98                 | €5.94           | €7.47   | €6.89             | €7.12        | €5.86   | *TBU*   | *TBU*      | *TBU*   | €6.41   | €9.20    |
| *Train r2*  | *NA*         | 0.844                 | 0.843           | 0.753   | 0.966             | 0.811        | 0.830   | *TBU*   | *TBU*      | *TBU*   | 0.779   | 0.501    |
| *Test r2*   | 0.130        | 0.699                 | 0.703           | 0.543   | 0.610             | 0.579        | 0.713   | *TBU*   | *TBU*      | *TBU*   | 0.658   | 0.309    |

*Note*: Metrics besides baseline are the mean value for said metrics that were originally calculated for each hour

**Predictions by Hour**<br>
One of the peculiarities of this problem is that all 24 hours of next day prices must be predicted by the same deadline. This naturally leads to an imbalance of known data for predicting and potentially less certainty when predicting the later hours vs the early hours of the day.

*Plot of hourly errors TBU*

## Production Model

*TBU RNN*

## Future Work
