import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np

import datetime
import matplotlib.dates as mdates

def call_function():
    list_glitches = []
    n = int(input("glitches_number = Quantos glithes você quer escolher? "))

    for i in range(n):
        glitch = input(f"\nDigite o glitch {i+1}: ")
        list_glitches.append(glitch)

    print(f'\n{list_glitches}')
    
    x_letter = input(f"\nDigite a letra correspondente do eixo x: \n 'd' for 'daily',\n 'w' for 'weekly',\n 'm' for 'monthly',\n 'q' for 'quarterly',\n '2q' for 'half-yearly',\n 'y' for 'annual'\n")

    return n, list_glitches, x_letter

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
        print("Letra inválida.")
        return
        
    # for i in range(n):
    #     if glitches_chosen[i] not in data['label']:
    #         print("Glitch inválido.")
    
    # Verification
    
    valid_labels = set(data['label'].unique())
    invalid_labels = [nome for nome in glitches_chosen if nome not in valid_labels]
    
    if invalid_labels:
        print("Os seguintes nomes são inválidos ou foram digitados incorretamente:")
        for nome in invalid_labels:
            print(f"  - {nome}")
    else:
        print("Todos os nomes escolhidos são válidos!")

    # valid_labels = data['label'].unique()

    # invalidos = []
    # for nome in glitches_chosen:
    #     if nome not in valid_labels:
    #         print(f"Atenção: {nome} não está no dataframe atual, mas será aceito.")
            # Você pode ainda decidir: invalidos.append(nome) ou ignorar

    # Continue com a lógica desejada

def plot_function(data, glitches_number, glitches_chosen, time_key):
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

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()
        
    plt.ylabel('Numbers of Glitches')
    plt.title(f'O3a run events {freq_dict[time_key]}')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()