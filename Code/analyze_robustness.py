import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import re
from datetime import datetime

# Parse robustness_log.txt
data = []
with open(r"D:\Desktop\Update_Project\robustness_log.txt") as file:
    for line in file:
        #timestamp_match = re.search(r'^(.*?) -', line)
        timestamp_match = re.search(r'INFO:root:(.*?) -', line)
        scenario_match = re.search(r'- (.*?) - (.*?)$', line.strip())
        if scenario_match and timestamp_match:
            timestamp = datetime.strptime(timestamp_match.group(1).strip(), "%Y-%m-%d %H:%M:%S.%f")
            scenario = scenario_match.group(1).strip()
            detected = 1 if "Faces Detected" in scenario_match.group(2) else 0
            data.append({'timestamp': timestamp, 'scenario': scenario, 'detected': detected})

# Convert to DataFrame
df = pd.DataFrame(data)

# Group data
grouped = df.groupby('scenario').agg(total_frames=('detected', 'count'), detections=('detected', 'sum'))
grouped['detection_rate (%)'] = (grouped['detections'] / grouped['total_frames']) * 100

# 1️⃣ Stacked Bar Chart
fig1, ax1 = plt.subplots()
ax1.bar(grouped.index, grouped['total_frames'], label='Total Frames', alpha=0.5)
ax1.bar(grouped.index, grouped['detections'], label='Detections (False Positives)', alpha=0.9)
ax1.set_ylabel('Frame Count')
ax1.set_title('Stacked Bar Chart - Total Frames vs Detections')
ax1.legend()

# 2️⃣ Percentage Bar Chart
fig2, ax2 = plt.subplots()
ax2.bar(grouped.index, grouped['detection_rate (%)'])
ax2.set_ylabel('Detection Rate (%)')
ax2.set_title('Percentage Bar Chart - Detection Rates by Scenario')

# 3️⃣ Heatmap
heatmap_data = grouped[['total_frames', 'detections', 'detection_rate (%)']]
fig3, ax3 = plt.subplots()
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax3)
ax3.set_title('Heatmap - Robustness Metrics')

# 4️⃣ Line Plot (Time Trends)
time_data = df.groupby([df['timestamp'].dt.floor('min'), 'scenario']).sum().reset_index()
pivot = time_data.pivot(index='timestamp', columns='scenario', values='detected').fillna(0)
fig4, ax4 = plt.subplots()
pivot.plot(ax=ax4)
ax4.set_ylabel('Detections')
ax4.set_title('Line Plot - Detections Over Time')
ax4.legend(title='Scenario')

# Show all plots
plt.show()
