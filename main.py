# run 'pip install yfinance'
import yfinance as yahoo_finance
import time
import os
import sys

if __name__ == '__main__':
    try:
        while True:
            tickerStr = input('\nEnter ticker (GOLD, BTC-USD ... or q): ')

            if tickerStr == 'q':
                break

            period = input('Enter period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max): ')
            interval = input('Enter interval (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo): ')
            tickerBase = yahoo_finance.Ticker(tickerStr)
            historyDataFrame = tickerBase.history(period=period, interval=interval)

            if historyDataFrame.empty:
                continue

            historyDataFrame.reset_index(names=['Date'], inplace=True)
            historyDataFrame['Date'] = historyDataFrame['Date'].dt.strftime('%Y-%m-%d')
            print(historyDataFrame.to_string() if len(historyDataFrame) < 100 else historyDataFrame)
            save_as = input('\nSave as (csv, txt, dat, all, none - n): ')
            supported_options = ['csv', 'txt', 'dat', 'all']
            supported_formats = supported_options[0:-1]

            if save_as not in supported_options:
                continue

            print('\nColumns with indexes:')
            column_names = historyDataFrame.columns
            for i in range(len(column_names)):
                print(f'{i}: {column_names[i]}')

            selected_col_indexes = list(
                map(int, input(f'\nEnter indexes to save (0 1 2 3 ... {len(column_names) - 1}): ').split()))
            selected_columns = [column_names[i] for i in selected_col_indexes]
            current_dir = os.getcwd()
            file_label = f'{tickerStr}-{time.strftime("%Y%m%d-%H%M%S")}'

            if save_as in supported_formats:
                file_name = f'{file_label}.{save_as}'
                historyDataFrame.to_csv(file_name,
                                        columns=selected_columns,
                                        sep=',' if save_as == 'csv' else ' ',
                                        index=False,
                                        mode='w')
                print(f'Successfully saved {file_name} to {current_dir}'
                      if os.path.exists(f'{current_dir}/{file_name}') else 'An error occurred while saving...')
            elif save_as == 'all':
                for ext in supported_formats:
                    historyDataFrame.to_csv(f'{file_label}.{ext}',
                                            columns=selected_columns,
                                            sep=',' if ext == 'csv' else ' ',
                                            index=False,
                                            mode='w')
                    print(f'Successfully saved file {file_label}.{ext} to {current_dir}' if os.path.exists(
                        f'{current_dir}/{file_label}') else 'An error occurred while saving...')
    except KeyboardInterrupt:
        sys.exit(0)
