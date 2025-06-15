# traffic_accident_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load dataset
df = pd.read_csv("NYPD_Motor_Vehicle_Collisions.csv")

# Convert column names to uppercase and strip spaces (optional but helpful)
df.columns = df.columns.str.strip().str.upper()

# --- Initial Cleaning ---
# Convert date and time columns
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M', errors='coerce').dt.time

# Drop rows without location info
df.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

# Extract hour from time
df['HOUR'] = pd.to_datetime(df['TIME'], format='%H:%M:%S', errors='coerce').dt.hour

# --- Visualization 1: Accidents by Hour ---
plt.figure(figsize=(10, 5))
sns.countplot(x='HOUR', data=df, palette='magma')
plt.title('Number of Accidents by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.savefig('accidents_by_hour.png')
plt.close()

# --- Visualization 2: Top Contributing Factors (Vehicle 1) ---
top_factors = df['VEHICLE 1 FACTOR'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_factors.values, y=top_factors.index, palette='coolwarm')
plt.title('Top 10 Contributing Factors (Vehicle 1)')
plt.xlabel('Number of Accidents')
plt.ylabel('Contributing Factor')
plt.tight_layout()
plt.savefig('top_contributing_factors.png')
plt.close()

# --- Visualization 3: Heatmap of Accident Locations ---
map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]
m = folium.Map(location=map_center, zoom_start=11)
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df.iterrows()]
HeatMap(heat_data[:10000]).add_to(m)  # limit for performance
m.save('accident_hotspots_map.html')

print("✅ Analysis complete. Charts saved as PNG, map saved as HTML.")
