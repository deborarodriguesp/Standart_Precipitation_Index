import sys
import os
import pandas as pd
from standard_precip.spi import SPI
import numpy as np

def load_dataframe(file_path):
    df = pd.read_csv(file_path, delimiter='\t')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df.set_index('Date', inplace=True)
    return df
    
    
def write_precipitation_data_to_file(output_filename, daily_mean_precip_df, station_name):
    
    with open(output_filename, 'w') as output_file:
        initial_info = (
            'SERIE_INITIAL_DATA :  2022 01 01 00 00 00\n'
            'TIME_UNITS         : DAYS\n\n'
            '!time dry wet normal\n'
            '<BeginTimeSerie>\n'
        )
        output_file.write(initial_info) 

        for i, (index, row) in enumerate(daily_mean_precip_df.iterrows()):
            time_step = i
            dry_value = row[f'Precip_Dry_{station_name}']
            wet_value = row[f'Precip_Wet_{station_name}']
            normal_value = row[f'Precip_Normal_{station_name}']

            line_to_write = f'{time_step} {dry_value} {wet_value} {normal_value}\n'
            output_file.write(line_to_write)

        # Write end of time series
        output_file.write('<EndTimeSerie>\n')


def calculate_spi(df_yearly):
    spi_calculator = SPI()
    df_combined = pd.DataFrame({'Date': df_yearly['Date']})
    spi_stations = [] 
    
    for coluna in df_yearly.columns[1:]:
        station_name = coluna
        station_series = df_yearly[['Date', coluna]].rename(columns={coluna: 'acc_precip'})
        #print (station_series)
        
        if not station_series['acc_precip'].isna().all() and not (station_series['acc_precip'] == 0).all():
            # Replace zeros with NaN before calculating SPI
            station_series['acc_precip'].replace(0, np.nan, inplace=True)
            
            spi_station = spi_calculator.calculate(station_series, 'Date', 'acc_precip', freq="M", scale=1, fit_type="lmom", dist_type="gam")
            spi_station.rename(columns={'acc_precip': f'ACC_Precip_{station_name}', 'acc_precip_calculated_index': f'SPI_{station_name}'}, inplace=True)
            
            dry = (spi_station[f'SPI_{station_name}'] <= -1.0)
            normal = (spi_station[f'SPI_{station_name}'] >= -0.999999) & (spi_station[f'SPI_{station_name}'] <= 0.9999999)
            wet = (spi_station[f'SPI_{station_name}'] >= 1.0)
        
            conditions = [dry, normal, wet]
            values = ['Dry', 'Normal', 'Wet']
            # Apply conditions for each station separately
            spi_station[f'SPI_Category_{station_name}'] = np.select(conditions, values, default=np.nan)
            df_combined = pd.merge(df_combined, spi_station, on='Date', how='left')

    return df_combined[:-2]


def calculate_daily_mean_precipitation(df, df_combined, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for coluna in df_combined.columns:
        if coluna.startswith('SPI_Category'):
           
            station_name = coluna.split('_')[-1]
            valid_values_count = df_combined[~df_combined[f'SPI_Category_{station_name}'].isnull()][f'SPI_Category_{station_name}'].count()
            
            if valid_values_count >= min_values:
                daily_mean_precip_df = pd.DataFrame({'Date': pd.date_range(start='2022-01-01', end='2022-12-31')})
                df_station = df[[station_name]].copy()
                df_station['Date'] = df_station.index
                df_station['Date'] = pd.to_datetime(df_station['Date'])
                df_station.set_index('Date', inplace=True)
                df_station['Month_Day'] = df_station.index.strftime('%m-%d')
                
                # extracting the unique years for which the SPI category for the specified station is "Extreme_Dry"
                # selects only the rows corresponding to the years classified as "Extreme_Dry"
                # creating a new column in the daily_mean_precip_df DataFrame to store the calculated daily mean precipitation values
                
                dry_years = df_combined[df_combined[f'SPI_Category_{station_name}'] == 'Dry']['Date'].dt.year.unique()
                dry_daily_mean = df_station[df_station.index.year.isin(dry_years) & ~df_station[station_name].isna()].groupby('Month_Day')[station_name].mean()
                #dry_daily_mean = df_station[df_station.index.year.isin(dry_years)].groupby('Month_Day')[station_name].mean()
                # Check if mean contains NaN values
                if not dry_daily_mean.isna().any():
                    daily_mean_precip_df[f'Precip_Dry_{station_name}'] = daily_mean_precip_df['Date'].dt.strftime('%m-%d').map(dry_daily_mean)
                
                wet_years = df_combined[df_combined[f'SPI_Category_{station_name}'] == 'Wet']['Date'].dt.year.unique()
                wet_daily_mean = df_station[df_station.index.year.isin(wet_years) & ~df_station[station_name].isna()].groupby('Month_Day')[station_name].mean()
                #wet_daily_mean = df_station[df_station.index.year.isin(wet_years)].groupby('Month_Day')[station_name].mean()
                if not wet_daily_mean.isna().any():
                    daily_mean_precip_df[f'Precip_Wet_{station_name}'] = daily_mean_precip_df['Date'].dt.strftime('%m-%d').map(wet_daily_mean)
    
                normal_years = df_combined[df_combined[f'SPI_Category_{station_name}'] == 'Normal']['Date'].dt.year.unique()
                normal_daily_mean = df_station[df_station.index.year.isin(normal_years) & ~df_station[station_name].isna()].groupby('Month_Day')[station_name].mean()
                #normal_daily_mean = df_station[df_station.index.year.isin(normal_years)].groupby('Month_Day')[station_name].mean()
                if not normal_daily_mean.isna().any():
                    daily_mean_precip_df[f'Precip_Normal_{station_name}'] = daily_mean_precip_df['Date'].dt.strftime('%m-%d').map(normal_daily_mean)
                
                station_output_folder = os.path.join(output_folder)
                output_filename = os.path.join(station_output_folder, f'daily_mean_precipitation_{station_name}.txt')
                
                if not daily_mean_precip_df.isna().any().any():
                    write_precipitation_data_to_file(output_filename, daily_mean_precip_df, station_name)

if __name__ == "__main__":
   
    min_values = 30
       
    df = load_dataframe('E:\METEOROLOGIA\Precipitation_scenarious\dataframe_precip.txt')
    df_yearly = df.resample('Y').sum()
    df_yearly.to_csv('yearly.csv', sep='\t', index=False, na_rep="NaN")
    df_yearly.reset_index(inplace=True)
    
    df_combined = calculate_spi(df_yearly)
    df_combined.to_csv('spi_results_combined.csv', sep='\t', index=False, na_rep="NaN")

    output_folder = 'Precipitation_time_series'
    calculate_daily_mean_precipitation(df, df_combined, output_folder)
    
    print ('\n')
    print ('Script has finished to run')
    print ('\n')
