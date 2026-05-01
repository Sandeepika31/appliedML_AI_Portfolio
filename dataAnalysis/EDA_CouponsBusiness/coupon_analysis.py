# -*- coding: utf-8 -*-
"""
Assignment 5.1 — Will the Customer Accept the Coupon?
Addresses all prompts from prompt.ipynb
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = r'C:\Users\sandeepi\OneDrive - Qualcomm\Desktop\devC\AI_ML_PG_Course\assignment5_1_starter\data\coupons.csv'
OUT_DIR   = r'C:\Users\sandeepi\OneDrive - Qualcomm\Desktop\devC\AI_ML_PG_Course\assignment5_1_starter\plots'
os.makedirs(OUT_DIR, exist_ok=True)

def savefig(name):
    p = os.path.join(OUT_DIR, name)
    plt.savefig(p, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  📊 {name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Read data
# ═══════════════════════════════════════════════════════════════════════════════
data = pd.read_csv(DATA_PATH)
print(f"Shape: {data.shape}")
print(data.head())

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Investigate missing / problematic data
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── Missing values ──────────────────────────────────────")
missing = data.isnull().sum()
print(missing[missing > 0])
print(f"\n'car' column: {data['car'].notna().sum()} non-null out of {len(data)} "
      f"({data['car'].notna().mean()*100:.1f}% filled) → DROP column")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Handle missing data
# ═══════════════════════════════════════════════════════════════════════════════
# Drop 'car' (99% missing — not useful)
data = data.drop(columns=['car'])

# Fill frequency columns with mode (small % missing)
freq_cols = ['Bar', 'CoffeeHouse', 'CarryAway', 'RestaurantLessThan20', 'Restaurant20To50']
for col in freq_cols:
    mode_val = data[col].mode()[0]
    n_filled = data[col].isna().sum()
    data[col] = data[col].fillna(mode_val)
    print(f"  Filled {n_filled} NaN in '{col}' with mode='{mode_val}'")

print(f"\nRemaining NaN: {data.isnull().sum().sum()}")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Overall coupon acceptance rate
# ═══════════════════════════════════════════════════════════════════════════════
accept_rate = data['Y'].mean()
print(f"\n── Overall acceptance rate: {accept_rate*100:.1f}%  "
      f"({data['Y'].sum():,} accepted / {len(data):,} total)")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Bar plot of coupon column
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
coupon_counts = data['coupon'].value_counts()
bars = ax.bar(coupon_counts.index, coupon_counts.values,
              color=sns.color_palette('Set2', len(coupon_counts)), edgecolor='black')
ax.set_xlabel('Coupon Type', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Distribution of Coupon Types', fontsize=13, fontweight='bold')
ax.tick_params(axis='x', rotation=15)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
savefig('01_coupon_distribution.png')

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Histogram of temperature column
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))
ax.hist(data['temperature'], bins=[25, 42, 67, 85], edgecolor='black',
        color='steelblue', rwidth=0.7)
ax.set_xlabel('Temperature (°F)', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Distribution of Temperature', fontsize=13, fontweight='bold')
ax.set_xticks([30, 55, 80])
plt.tight_layout()
savefig('02_temperature_histogram.png')

# ═══════════════════════════════════════════════════════════════════════════════
# BAR COUPON ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("BAR COUPON ANALYSIS")

# 1. Create bar coupon DataFrame
bar_df = data[data['coupon'] == 'Bar'].copy()
print(f"Bar coupon rows: {len(bar_df):,}")

# 2. Proportion of bar coupons accepted
bar_accept = bar_df['Y'].mean()
print(f"Bar coupon acceptance rate: {bar_accept*100:.1f}%")

# 3. Acceptance: ≤3 visits/month vs >3 visits/month
freq_map = {'never': 0, 'less1': 0.5, '1~3': 2, '4~8': 6, 'gt8': 9}
bar_df['Bar_num'] = bar_df['Bar'].map(freq_map)

low_bar  = bar_df[bar_df['Bar_num'] <= 3]
high_bar = bar_df[bar_df['Bar_num'] > 3]
print(f"\nAcceptance ≤3 bar visits/month : {low_bar['Y'].mean()*100:.1f}%  (n={len(low_bar):,})")
print(f"Acceptance >3 bar visits/month : {high_bar['Y'].mean()*100:.1f}%  (n={len(high_bar):,})")

# 4. >1 bar visit/month AND age > 25 vs all others
bar_df['age_num'] = pd.to_numeric(bar_df['age'], errors='coerce')
# age column has strings like '21', '26', 'below21', '50plus'
bar_df['age_num'] = bar_df['age'].replace({'below21': 18, '50plus': 55}).apply(
    lambda x: float(x) if str(x).replace('.','').isdigit() else np.nan)

grp_a = bar_df[(bar_df['Bar_num'] > 1) & (bar_df['age_num'] > 25)]
grp_b = bar_df[~((bar_df['Bar_num'] > 1) & (bar_df['age_num'] > 25))]
print(f"\n>1 bar/month AND age>25        : {grp_a['Y'].mean()*100:.1f}%  (n={len(grp_a):,})")
print(f"All others                     : {grp_b['Y'].mean()*100:.1f}%  (n={len(grp_b):,})")

# 5. >1 bar/month, no kid passenger, not farming/fishing/forestry
grp_c = bar_df[
    (bar_df['Bar_num'] > 1) &
    (bar_df['passanger'] != 'Kid(s)') &
    (~bar_df['occupation'].isin(['Farming Fishing & Forestry']))
]
grp_d = bar_df[~(
    (bar_df['Bar_num'] > 1) &
    (bar_df['passanger'] != 'Kid(s)') &
    (~bar_df['occupation'].isin(['Farming Fishing & Forestry']))
)]
print(f"\n>1 bar/month, no kid, not farm : {grp_c['Y'].mean()*100:.1f}%  (n={len(grp_c):,})")
print(f"All others                     : {grp_d['Y'].mean()*100:.1f}%  (n={len(grp_d):,})")

# 6. Combined conditions
bar_df['RestaurantLessThan20_num'] = bar_df['RestaurantLessThan20'].map(freq_map)
bar_df['income_low'] = bar_df['income'].isin([
    'Less than $12500', '$12500 - $24999', '$25000 - $37499', '$37500 - $49999'])

cond1 = ((bar_df['Bar_num'] > 1) & (bar_df['passanger'] != 'Kid(s)') &
         (bar_df['maritalStatus'] != 'Widowed'))
cond2 = ((bar_df['Bar_num'] > 1) & (bar_df['age_num'] < 30))
cond3 = ((bar_df['RestaurantLessThan20_num'] > 4) & bar_df['income_low'])

combined = bar_df[cond1 | cond2 | cond3]
print(f"\nCombined conditions (cond1|2|3): {combined['Y'].mean()*100:.1f}%  (n={len(combined):,})")

# ── Bar coupon acceptance summary plot ────────────────────────────────────────
groups = {
    'All Bar\nCoupons'         : bar_df['Y'].mean(),
    '≤3 bar\nvisits/mo'        : low_bar['Y'].mean(),
    '>3 bar\nvisits/mo'        : high_bar['Y'].mean(),
    '>1 visit &\nAge>25'       : grp_a['Y'].mean(),
    'Others\n(Q4)'             : grp_b['Y'].mean(),
    '>1 visit,\nno kid,\nnot farm': grp_c['Y'].mean(),
    'Combined\nconditions'     : combined['Y'].mean(),
}
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#4C72B0' if v >= bar_accept else '#DD8452' for v in groups.values()]
bars = ax.bar(groups.keys(), [v*100 for v in groups.values()],
              color=colors, edgecolor='black', alpha=0.85)
ax.axhline(bar_accept*100, color='red', linestyle='--', linewidth=1.5,
           label=f'Overall bar acceptance ({bar_accept*100:.1f}%)')
ax.set_ylabel('Acceptance Rate (%)', fontsize=12)
ax.set_title('Bar Coupon Acceptance Rate by Driver Segment', fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
ax.legend(fontsize=10)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
savefig('03_bar_coupon_acceptance_segments.png')

# ═══════════════════════════════════════════════════════════════════════════════
# INDEPENDENT INVESTIGATION — Coffee House Coupons
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("INDEPENDENT INVESTIGATION — Coffee House Coupons")

ch_df = data[data['coupon'] == 'Coffee House'].copy()
ch_df['CoffeeHouse_num'] = ch_df['CoffeeHouse'].map(freq_map)
ch_df['age_num'] = ch_df['age'].replace({'below21': 18, '50plus': 55}).apply(
    lambda x: float(x) if str(x).replace('.','').isdigit() else np.nan)

print(f"Coffee House coupon rows: {len(ch_df):,}")
print(f"Overall acceptance rate : {ch_df['Y'].mean()*100:.1f}%")

# Acceptance by time of day
print("\nAcceptance by time of day:")
print(ch_df.groupby('time')['Y'].mean().mul(100).round(1).to_string())

# Acceptance by passenger type
print("\nAcceptance by passenger type:")
print(ch_df.groupby('passanger')['Y'].mean().mul(100).round(1).to_string())

# Acceptance by coffee house visit frequency
print("\nAcceptance by coffee house visit frequency:")
print(ch_df.groupby('CoffeeHouse')['Y'].mean().mul(100).round(1).to_string())

# Acceptance by weather
print("\nAcceptance by weather:")
print(ch_df.groupby('weather')['Y'].mean().mul(100).round(1).to_string())

# ── Coffee House heatmap: time × passenger ────────────────────────────────────
pivot = ch_df.pivot_table(values='Y', index='passanger', columns='time', aggfunc='mean') * 100
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
            linewidths=0.5, cbar_kws={'label': 'Acceptance Rate (%)'})
ax.set_title('Coffee House Coupon Acceptance Rate\nby Passenger Type × Time of Day',
             fontsize=13, fontweight='bold')
plt.tight_layout()
savefig('04_coffeehouse_heatmap_time_passenger.png')

# ── Coffee House acceptance by visit frequency ────────────────────────────────
order = ['never', 'less1', '1~3', '4~8', 'gt8']
ch_freq = ch_df.groupby('CoffeeHouse')['Y'].mean().reindex(order) * 100
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(ch_freq.index, ch_freq.values, color=sns.color_palette('Blues_d', len(ch_freq)),
       edgecolor='black')
ax.set_xlabel('Coffee House Visits per Month', fontsize=12)
ax.set_ylabel('Acceptance Rate (%)', fontsize=12)
ax.set_title('Coffee House Coupon Acceptance\nby Visit Frequency', fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
for i, v in enumerate(ch_freq.values):
    ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
savefig('05_coffeehouse_acceptance_by_frequency.png')

# ── Overall acceptance by coupon type ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
acc_by_coupon = data.groupby('coupon')['Y'].mean().sort_values(ascending=False) * 100
colors = sns.color_palette('Set2', len(acc_by_coupon))
bars = ax.bar(acc_by_coupon.index, acc_by_coupon.values, color=colors, edgecolor='black')
ax.axhline(data['Y'].mean()*100, color='red', linestyle='--', linewidth=1.5,
           label=f'Overall ({data["Y"].mean()*100:.1f}%)')
ax.set_ylabel('Acceptance Rate (%)', fontsize=12)
ax.set_title('Coupon Acceptance Rate by Coupon Type', fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
ax.legend(fontsize=10)
ax.tick_params(axis='x', rotation=10)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
savefig('06_acceptance_by_coupon_type.png')

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("SUMMARY")
print(f"  Overall acceptance rate          : {data['Y'].mean()*100:.1f}%")
print(f"  Bar coupon acceptance            : {bar_df['Y'].mean()*100:.1f}%")
print(f"  Coffee House coupon acceptance   : {ch_df['Y'].mean()*100:.1f}%")
print(f"\nHypothesis — Bar coupon acceptors:")
print("  Drivers who go to bars >1x/month, are under 30, have no kids,")
print("  and are not in farming/fishing/forestry occupations are significantly")
print("  more likely to accept bar coupons (acceptance rate well above average).")
print(f"\nPlots saved to: {OUT_DIR}")
