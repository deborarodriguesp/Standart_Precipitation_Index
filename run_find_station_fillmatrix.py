import os
import pandas as pd

def extract_station_names(folder_path):

    #Extracts station names from files in the specified folder.

    station_names = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.lower().endswith('.txt') and filename.startswith('daily_mean_precipitation_'):
            station_name = filename.split('_')[-1].split('.')[0]
            station_names.append(station_name)

    return station_names


def write_station_info(station_names, stations_files, column_headers, output_file_path):

    #Writes station information to the output file based on the provided station names and CSV files.

    with open(output_file_path, 'w') as output_file, open(qgis_output_file_path, 'w') as qgis_output_file:
        # Write initial information
        initial_info = (
            'PROPERTY_NAME           : precipitation\n'
            'PROPERTY_UNITS          : mm\n'
            'VARIABLE_IN_TIME        : 1\n'
            'START                   : 2022 01 01 00 00 00\n'
            'END                     : 2023 01 01 00 00 00\n'
            'OUTPUT_TIME             : 0 86400\n'
            'OUTPUT_FILE             : Precip_.hdf5\n'
            'GRID_DATA_FILE          : dtm_para_v1_edit.dat\n'
            'FILL_OUTSIDE_POINTS     : 1\n'
            'MAX_TIME_SPAN           : 86400\n'
            'INTERPOLATION_METHOD    : 2\n'
            'MAX_DISTANCE            : 1000\n'
            'IWD_N                   : 4.0\n'
            'SKIP_NULLVALUES         : 0\n'
            '\n'
        )
        
        output_file.write(initial_info) 
        
        qgis_output_file.write('station,x,y\n')
        
        for station_name in station_names:
            station_found = False

            for csv_file_path in stations_files:
                df = pd.read_csv(csv_file_path, usecols=column_headers)

                if any(df['CODIGO'] == int(station_name)):
                    matching_rows = df[df['CODIGO'] == int(station_name)]

                    if not matching_rows.empty:
                        station_row = matching_rows.iloc[0]
                        x_coord = str(station_row['x'])
                        y_coord = str(station_row['y'])

                        line_to_write = (
                            '<begin_station>\n'
                            f'NAME                    : {station_name}\n'
                            f'X                       : {x_coord}\n'
                            f'Y                       : {y_coord}\n'
                            'VALUE_TYPE              : TIMESERIE\n'
                            f'FILENAME                : {folder_path}\daily_mean_precipitation_{station_name}.txt\n'
                            f'DATA_COLUMN             : {str(2)}\n'
                            '<end_station>\n\n'
                        )
                        output_file.write(line_to_write)
                        
                        qgis_output_file.write(f'{station_name},{x_coord},{y_coord}\n')
                        
                        break
    print(f"Output written to {output_file_path}")
    print(f"QGIS output written to {qgis_output_file_path}")

# Set the path to the folder containing precipitation time series files
folder_path = r'E:\METEOROLOGIA\Precipitation_scenarious\Precipitation_time_series'

stations_files = [
    r'D:\DOUTORAMENTO\EstacoesPluvi\Amazonas_filtered.csv',
    r'D:\DOUTORAMENTO\EstacoesPluvi\Atlantico_filtered.csv',
    r'D:\DOUTORAMENTO\EstacoesPluvi\Parana_filtered.csv',
    r'D:\DOUTORAMENTO\EstacoesPluvi\SaoFrancisco_filtered.csv',
    r'D:\DOUTORAMENTO\EstacoesPluvi\Tocantins_filtered.csv'
]

column_headers = ['CODIGO', 'x', 'y']

# Output file path
output_file_path = 'FillMatrix.dat'
qgis_output_file_path = 'station_list.txt'

# Extract station names and write station information to the output file
station_names = extract_station_names(folder_path)
write_station_info(station_names, stations_files, column_headers, output_file_path)


