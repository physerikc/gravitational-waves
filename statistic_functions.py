import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def inputs_dependences(data, n, glitches_chosen, chave):
    
    freq_dict = dict([
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
        ('q', 'quarterly'),
        ('2q', 'half-yearly'),
        ('y', 'annual')
    ])
    if chave not in freq_dict:
        print("Invalid key.")
        return
    
    valid_labels = set(data['label'].unique())
    invalid_labels = [nome for nome in glitches_chosen if nome not in valid_labels]
    
    if invalid_labels:
        print("The following names are invalid or misspelled: \n")
        for nome in invalid_labels:
            print(f"  - {nome}")
    else:
        print("All chosen names are valid.")

def plot_function(data, glitches_number, glitches_chosen, time_key, run):
    
    freq_dict = dict([
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
        ('q', 'quarterly'),
        ('2q', 'half-yearly'),
        ('y', 'annual')
    ])
    
    gps_epoch = pd.Timestamp('1980-01-06 00:00:00', tz='UTC')

    plt.figure(figsize=(10,5))
    
    for i in range(glitches_number):
        
        df = data[data['label'] == glitches_chosen[i]].copy()
        df.index = gps_epoch + pd.to_timedelta(df['GPStime'], unit='s')
        
        x_axis = df.resample(time_key).size()
        
        plt.plot(x_axis.index, x_axis.values, marker='o', linestyle='-', label=glitches_chosen[i])
  
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # plt.gcf().autofmt_xdate()

    plt.ylabel('Numbers of Glitches')
    plt.title(f'{run} run events {freq_dict[time_key]}')

    # ax.savefig('images/time_tracking.png')

    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()

def plot_function_per_rate(data, glitches_number, glitches_chosen, time_key, run):
    
    freq_dict = dict([
        ('d', 'daily'),
        ('w', 'weekly'),
        ('m', 'monthly'),
        ('q', 'quarterly'),
        ('2q', 'half-yearly'),
        ('y', 'annual')
    ])
    
    gps_epoch = pd.Timestamp('1980-01-06 00:00:00', tz='UTC')
    
    plt.figure(figsize=(10,5))
    
    for i in range(glitches_number):
        
        df = data[data['label'] == glitches_chosen[i]].copy()
        df.index = gps_epoch + pd.to_timedelta(df['GPStime'], unit='s')

        count_series = df.resample(time_key).size()
        duration_series = df['duration'].resample(time_key).sum()

        rate_series = count_series / duration_series.replace(0, np.nan)
        
        # x_axis = df.resample(time_key).size()
        
        plt.plot(rate_series.index, rate_series.values, marker='o', linestyle='-', label=glitches_chosen[i])
    
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # plt.gcf().autofmt_xdate()
    
    plt.ylabel('Numbers of Glitches per Rate')
    plt.title(f'{run} run events {freq_dict[time_key]}')
    
    # ax.savefig('images/time_tracking.png')
    
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()

def count_glitch(data, time, glitch):

    # tam = len(data)
    # time_begin = data['GPStime'][0]
    # time_end = data['GPStime'][tam-1]
    # time_range = time_end - time_begin
    
    # hours_number = int(time_range/3600)
    
    print(time)
    bins = time
    
    # Filtra apenas os eventos do tipo de glitch desejado
    data_filtered = data[data['label'] == glitch]
    
    # Divide os tempos filtrados em faixas
    data_binned = pd.cut(data_filtered['GPStime'], bins=bins)
    
    # Conta quantos eventos por faixa
    counts = data_binned.value_counts().sort_index()
    
    return counts