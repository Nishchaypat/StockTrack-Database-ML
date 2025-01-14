# StockTrack: Machine Learning for Stock Market Insights  

This repository focuses on the **Machine Learning (ML)** components of StockTrack, a stock tracking platform designed to empower investors with **AI-driven predictions** and **sentiment analysis**. The ML models are the backbone of StockTrack's predictive capabilities, offering users actionable insights into stock price movements and market sentiment.

---

## Key Features  

### AI-Powered Stock Price Prediction  
- Utilizes an **XGBoost model** trained on historical OHLCV data and technical indicators such as SMA, EMA, RSI, MACD, Bollinger Bands, and ADX.  
- Achieves **93% accuracy** in predicting stock prices, enabling investors to make informed decisions.  

### Sentiment Analysis  
- Real-time sentiment analysis of financial news using **BERT + LSTM**, helping gauge market sentiment and identify potential trends.  

### Data Pipeline  
- Historical stock data preprocessing for feature engineering and technical indicator calculation.  
- Model evaluation includes metrics such as MAE, MSE, and RMSE for robust performance assessment.  

---

## Technical Stack  

- **Machine Learning Frameworks**: XGBoost, Scikit-learn  
- **Sentiment Analysis Models**: BERT + LSTM using TensorFlow and PyTorch  
- **Programming Language**: Python  
- **Libraries**: Pandas, NumPy, Matplotlib, NLTK, Hugging Face Transformers  

---

## Repository Highlights  

1. **Stock Price Prediction**  
   - Jupyter notebooks and Python scripts for training and testing the XGBoost model.  
   - Feature engineering using historical OHLCV data and technical indicators.  

2. **Sentiment Analysis**  
   - Pre-trained BERT model fine-tuned with LSTM for financial text sentiment classification.  
   - Python scripts for preprocessing text data and training the model.  

3. **Evaluation Metrics**  
   - Performance metrics like Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE) for stock prediction.  


