import motionData as md
import adaptiveJerkPaceBuffer as ajpb
import adaptiveJerkPaceThreshold as ajpt
import adaptiveStepJerkThreshold as asjt
import matplotlib.pyplot as plt
from utils import calcEnergy

md.walkData['accz'] = md.walkData['accz'] * 9.8
md.walkData['energy'] = calcEnergy(md.walkData)
r = md.walkData['energy'].values
timestamps = md.walkData['timestamp'].values

# Adaptive Step Jerk Threshold
jumps, avgs = asjt.adaptive_step_jerk_threshold(r, timestamps)
ts = [jump['ts'] for jump in jumps]
val = [jump['val'] for jump in jumps]
print("Adaptive Step Jerk Threshold 2 Steps:", len(jumps))
print("Final Step Jerk Average:", avgs[-1][1])

plt.plot(timestamps, r, 'b-', linewidth=2)
plt.plot(ts, val, 'ro')
plt.plot(avgs.T[0], avgs.T[1], 'r--', linewidth=2)
plt.plot(avgs.T[0], avgs.T[2], 'g--', linewidth=2)
plt.title(" - Adaptive Step Jerk Threshold 2")
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show()

# Adaptive Step Jerk Buffer
peaks, troughs, avgs = ajpb.adaptive_jerk_pace_buffer(r, timestamps)
peak_ts = [peak['ts'] for peak in peaks]
peak_val = [peak['val'] for peak in peaks]
trough_ts = [trough['ts'] for trough in troughs]
trough_val = [trough['val'] for trough in troughs]
print("Adaptive Jerk Pace Buffer Steps:", len(troughs))
# print("Final Step Jerk Average:", avgs[-1][1])

plt.plot(timestamps, r, 'b-', linewidth=2)
plt.plot(peak_ts, peak_val, 'go')
plt.plot(trough_ts, trough_val, 'ro')
plt.plot(avgs.T[0], avgs.T[1], 'r--', linewidth=2)
plt.plot(avgs.T[0], avgs.T[2], 'g--', linewidth=2)
plt.title(" - Adaptive Jerk Pace Buffer")
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show()