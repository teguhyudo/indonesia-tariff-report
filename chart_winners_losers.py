import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Data from Sector-Level ETR Comparison table (vs. Deal column)
sectors = [
    'Rubber (HS 40)',
    'Palm Oil (HS 15)',
    'Coffee (HS 09)',
    'Cocoa (HS 18)',
    'Electronics (HS 85)',
    'Steel (HS 72–73)',
    'Aluminum (HS 76)',
    'Knit Apparel (HS 61)',
    'Woven Apparel (HS 62)',
    'Footwear (HS 64)',
    'Furniture (HS 94)',
    'Machinery (HS 84)',
]

vs_deal = [15.0, 15.0, 15.0, 15.0, 2.7, 0.0, 0.0, -2.1, -2.1, -4.0, -4.0, -4.0]
trade_values = [1.96, 1.74, 0.50, 0.32, 4.51, 0.30, 0.20, 2.20, 2.02, 2.57, 1.57, 1.01]

# Sort by vs_deal descending (losers at top, winners at bottom)
sorted_idx = np.argsort(vs_deal)
sectors = [sectors[i] for i in sorted_idx]
vs_deal = [vs_deal[i] for i in sorted_idx]
trade_values = [trade_values[i] for i in sorted_idx]

# Colors
colors = []
for v in vs_deal:
    if v > 0:
        colors.append('#C0392B')   # red for losers (higher tariff vs deal)
    elif v < 0:
        colors.append('#27AE60')   # green for winners (lower tariff vs deal)
    else:
        colors.append('#7F8C8D')   # gray for unchanged

fig, ax = plt.subplots(figsize=(10, 7))

y_pos = np.arange(len(sectors))
bars = ax.barh(y_pos, vs_deal, color=colors, edgecolor='white', linewidth=0.5, height=0.65)

# Add value labels on bars
for i, (bar, val, tv) in enumerate(zip(bars, vs_deal, trade_values)):
    if val >= 0:
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2,
                f'+{val:.1f} pp  (${tv:.2f}B)',
                va='center', ha='left', fontsize=9, color='#2C3E50', fontweight='medium')
    else:
        ax.text(bar.get_width() - 0.4, bar.get_y() + bar.get_height()/2,
                f'{val:.1f} pp  (${tv:.2f}B)',
                va='center', ha='right', fontsize=9, color='#2C3E50', fontweight='medium')

ax.set_yticks(y_pos)
ax.set_yticklabels(sectors, fontsize=10)
ax.set_xlabel('Change in ETR vs. Post-Deal (percentage points)', fontsize=11, fontweight='medium')
ax.set_title('Winners and Losers: S122 at 15% vs. the Bilateral Deal',
             fontsize=13, fontweight='bold', pad=15)

# Vertical line at zero
ax.axvline(x=0, color='#2C3E50', linewidth=0.8, linestyle='-')

# Annotations for regions — placed in empty space away from bars
ax.text(16.0, 5.5, 'LOSERS',
        fontsize=11, color='#C0392B', fontweight='bold',
        ha='center', va='center', fontstyle='italic', alpha=0.35)
ax.text(-5.5, 5.5, 'WINNERS',
        fontsize=11, color='#27AE60', fontweight='bold',
        ha='center', va='center', fontstyle='italic', alpha=0.35)

# Style
ax.set_xlim(-8, 22)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False)
ax.grid(axis='x', alpha=0.2, linestyle='--')

# Subtitle / note
fig.text(0.12, 0.02,
         'Note: Positive values indicate sectors worse off under S122 at 15% compared to the bilateral deal. '
         'Values in parentheses are 2024 U.S. import values.\n'
         'Source: Authors\' calculation based on USITC DataWeb, USITC HTS, WTO Tariff Profiles, and ART deal exemption schedule.',
         fontsize=7.5, color='#7F8C8D', va='bottom', ha='left', wrap=True)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('/Users/yudo/Library/CloudStorage/GoogleDrive-teguh.wicaksono@uiii.ac.id/My Drive/UIII/Oped/Tariff/report/winners_losers.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/Users/yudo/Library/CloudStorage/GoogleDrive-teguh.wicaksono@uiii.ac.id/My Drive/UIII/Oped/Tariff/report/winners_losers.pdf',
            bbox_inches='tight', facecolor='white')
print('Charts saved successfully.')
