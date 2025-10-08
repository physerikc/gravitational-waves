import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib.ticker import ScalarFormatter
from astropy.time import Time

from celluloid import Camera # importando a camera
import seaborn as sns
import warnings
from IPython.display import HTML # para mostrar o vídeo no jupyter

# Count the glitches ocorrence
def count_glitches(data, glitch_name, interval):
    glitch = data[data['label'] == glitch_name].copy()

    if glitch.empty:   # <-- Evita o erro
        return np.array([]), np.array([])

    times = np.sort(glitch['GPStime'].values)
    bins = np.arange(times[0], times[-1] + interval, interval)

    # Converter GPS para datetime usando astropy
    bins_dt = Time(bins[1:], format='gps').to_datetime()
    counts, _ = np.histogram(times, bins=bins)

    return counts, bins_dt

# Calculate the rate of glitches per interval
def rate_glitches(data, glitch_name, active, interval):
    counts, bins_rate = count_glitches(data, glitch_name, interval)

    if len(counts) == 0:   # <-- Se não tem glitches, não tem taxa
        return np.array([]), np.array([])

    active_week = active * 168
    rate = counts / active_week

    return rate, bins_rate

# Calculate the operation time
def time_active(df, interval):
  start_obs = df['start'].min()
  end_obs = df['end'].max()

  week_edges = np.arange(start_obs, end_obs + interval, interval)

  active_time_per_week = []

  for i in range(len(week_edges) - 1):
      week_start = week_edges[i]
      week_end = week_edges[i + 1]
      total_on = 0

      for _, row in df.iterrows():
          seg_start = row['start']
          seg_end = row['end']

          inter_start = max(week_start, seg_start)
          inter_end = min(week_end, seg_end)

          if inter_start < inter_end:
              total_on += inter_end - inter_start

      active_time_per_week.append(total_on)

  result = pd.DataFrame({
      'week_start': week_edges[:-1],
      'week_end': week_edges[1:],
      'active_time': active_time_per_week
  })

  active = result['active_time'].values/interval
  return active


# Add tracks by station
def adicionar_faixa(ax, inicio, fim, cor, label=None):
    ax.axvspan(inicio, fim, color=cor, alpha=0.2, label=label)

def celluloid(xaxis, yaxis, xlim, ylim, title, ylabel, xlabel, interval, type):
    
    fig, ax = plt.subplots(figsize=(6, 4)) # criando minha fig    
    camera = Camera(fig)# a camera recebe a figura que vamos usar

    if type == 'curve':
        for i in range(len(xaxis)):
            ax.set_title(f'{title}')
            ax.set_xlim(-0.05*xlim, xlim)
            ax.set_ylim(-0.05*ylim, ylim)
            ax.grid()
    
            new_xaxis = xaxis[:i]
            new_yaxis = yaxis[:i]

            formatter = ScalarFormatter(useOffset=False)
            formatter.set_scientific(False)

            ax.yaxis.set_major_formatter(formatter)
            ax.ticklabel_format(style='sci', axis='y', scilimits=(3, 3))
            
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            
            ax.plot(new_xaxis, new_yaxis, c='tab:blue')

            xreta = np.linspace(0, max(xaxis), 100)
            yreta = np.linspace(0, max(xaxis)/(7*24), 100)

            plt.plot(xreta, yreta, linestyle='--', c='black')
            
            plt.grid(linestyle='-', alpha=0.7)
            plt.tight_layout()  # Ajusta o layout para evitar cortes
            camera.snap() # tirar foto da fig
    
    animation = camera.animate(interval=interval) # animação pronta!
    plt.close(fig)
    return HTML(animation.to_html5_video()) #mostrando a animação no notebook



