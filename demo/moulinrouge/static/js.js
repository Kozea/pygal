import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_candlestick_chart(symbol, start_time, end_time, period):
    # Découpage des données en temps et lieu
    data = pd.read_csv('data/' + symbol + '_history')
    
    # Calcul des OHLC pour le period
    ohlc = data[['open', 'high', 'low', 'close']].values / 100.0
    
    plt.figure(figsize=(10, 6))
    plt.plot(ohlc, color='blue')
    plt.title(f'{symbol} OHLC Candlestick Chart')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

# Exemple d'utilisation
symbol = 'BTC-USD'
start_time = '2023-01-01'
end_time

ACTUAL REPO CODE (use these exact function names, imports, and patterns):
// FILE: .github/workflows/ci.yml
name: CI
concurrency:
  group: check-${{ github.ref }}
  cancel-in-progress: true
on:
  push:
    branches:
      - master
    tags:
      - v*
  pull_request:
    branches:
      - master
jobs:
  test:
    runs-on: '${{ matrix.os }}'
    strategy:
      matrix:
        os:
          - ubuntu-latest