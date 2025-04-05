import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Page Setup
st.set_page_config(page_title="Electricity Demand & Price Forecasting", layout="centered")
st.title("⚡ Electricity Demand & Price Forecasting using LSTM")
st.markdown("Upload your dataset and select a forecast range.")

# File Upload
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Fix date parsing using dayfirst format
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df = df[['date', 'demand_pos_RRP', 'RRP']]
    df.dropna(inplace=True)

    # Show sample data
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Date Range Selection
    min_date = df['date'].min() + timedelta(days=30)  # need 30 days history
    max_date = df['date'].max() + timedelta(days=1825)  # ~5 years ahead

    st.subheader("📆 Forecast Range Selection")
    start_date = st.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("To Date", value=start_date + timedelta(days=30), min_value=start_date, max_value=max_date)

    forecast_days = (end_date - start_date).days
    if forecast_days <= 0:
        st.warning("Please select a valid date range.")
        st.stop()

    # Preprocessing
    scaler_demand = MinMaxScaler()
    scaler_price = MinMaxScaler()

    df['demand_scaled'] = scaler_demand.fit_transform(df[['demand_pos_RRP']])
    df['price_scaled'] = scaler_price.fit_transform(df[['RRP']])

    seq_length = 30

    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    # Prepare data
    X_demand, y_demand = create_sequences(df['demand_scaled'].values, seq_length)
    X_price, y_price = create_sequences(df['price_scaled'].values, seq_length)

    X_demand = X_demand.reshape(X_demand.shape[0], seq_length, 1)
    X_price = X_price.reshape(X_price.shape[0], seq_length, 1)

    # Train-test split
    train_size = int(0.8 * len(X_demand))
    X_train_demand, X_test_demand = X_demand[:train_size], X_demand[train_size:]
    y_train_demand, y_test_demand = y_demand[:train_size], y_demand[train_size:]

    X_train_price, X_test_price = X_price[:train_size], X_price[train_size:]
    y_train_price, y_test_price = y_price[:train_size], y_price[train_size:]

    # Model definition
    def build_lstm_model():
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(seq_length, 1)),
            Dropout(0.2),
            LSTM(32),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    # Train models
    with st.spinner("Training Demand Forecasting Model..."):
        model_demand = build_lstm_model()
        model_demand.fit(X_train_demand, y_train_demand, epochs=10, batch_size=16, verbose=0)

    with st.spinner("Training Price Forecasting Model..."):
        model_price = build_lstm_model()
        model_price.fit(X_train_price, y_train_price, epochs=10, batch_size=16, verbose=0)

    # Forecasting function
    def forecast_from_date(model, full_scaled_data, date_series, scaler, forecast_days, start_date):
        # Get the last 30 days before the selected start_date
        last_idx = date_series[date_series < pd.to_datetime(start_date)].index.max()

        if last_idx is None or last_idx < seq_length:
            st.error("Not enough historical data before selected start date for forecasting.")
            st.stop()

        input_seq = full_scaled_data[last_idx - seq_length + 1:last_idx + 1].reshape(1, seq_length, 1)
        predictions = []

        for _ in range(forecast_days):
            pred = model.predict(input_seq, verbose=0)
            predictions.append(pred[0][0])
            input_seq = np.roll(input_seq, shift=-1, axis=1)
            input_seq[0, -1, 0] = pred[0][0]

        return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # Forecast using selected range
    with st.spinner("🔮 Forecasting future values..."):
        demand_forecast = forecast_from_date(
            model_demand, df['demand_scaled'].values, df['date'], scaler_demand, forecast_days, start_date
        )
        price_forecast = forecast_from_date(
            model_price, df['price_scaled'].values, df['date'], scaler_price, forecast_days, start_date
        )

    # Forecast dates from user-selected start
    future_dates = [start_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

    # Plotting
    st.subheader("📊 Forecast Results")

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))

    ax[0].plot(df['date'], df['demand_pos_RRP'], label="Actual Demand")
    ax[0].plot(future_dates, demand_forecast, label="Forecasted Demand", linestyle="dashed", color="orange")
    ax[0].set_title("Demand Forecast")
    ax[0].set_ylabel("Demand")
    ax[0].legend()

    ax[1].plot(df['date'], df['RRP'], label="Actual Price (RRP)")
    ax[1].plot(future_dates, price_forecast, label="Forecasted Price", linestyle="dashed", color="green")
    ax[1].set_title("Price Forecast")
    ax[1].set_ylabel("Price")
    ax[1].legend()

    plt.tight_layout()
    st.pyplot(fig)

    # Model Evaluation
    st.subheader("📈 Model Performance (on Test Data)")
    pred_demand_test = model_demand.predict(X_test_demand, verbose=0)
    pred_price_test = model_price.predict(X_test_price, verbose=0)

    actual_demand = scaler_demand.inverse_transform(y_test_demand.reshape(-1, 1))
    pred_demand = scaler_demand.inverse_transform(pred_demand_test)

    actual_price = scaler_price.inverse_transform(y_test_price.reshape(-1, 1))
    pred_price = scaler_price.inverse_transform(pred_price_test)

    st.line_chart({
        "Actual Demand": actual_demand.flatten(),
        "Predicted Demand": pred_demand.flatten()
    })

    st.line_chart({
        "Actual Price": actual_price.flatten(),
        "Predicted Price": pred_price.flatten()
    })
