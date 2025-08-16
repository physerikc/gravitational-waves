import pandas as pd
import numpy as np

from astropy.time import Time

# Count the glitches ocorrence
def count_glitches(data, glitch_name, interval):
    glitch = data[data['label'] == glitch_name].copy()

    times = np.sort(glitch['GPStime'].values)
    bins = np.arange(times[0], times[-1] + interval, interval)

    # Converter GPS para datetime usando astropy
    bins_dt = Time(bins[1:], format='gps').to_datetime()
    counts, _ = np.histogram(times, bins=bins)

    return counts, bins_dt

# Calculate the rate of glitches per interval
def rate_glitches(data, glitch_name, active, interval):

  counts, bins_rate = count_glitches(data, glitch_name, interval)
  active_week = active*168
  rate = counts/active_week

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



