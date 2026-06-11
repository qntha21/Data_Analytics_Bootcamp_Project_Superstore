# =============================================================================
# EXPLORATORY DATA ANALYSIS (EDA) - SUPERSTORE DATASET
# =============================================================================
# Description : In-depth exploration to understand sales patterns,
#               regional profitability, and the impact of discounts
#               on the Sample Superstore dataset (2014–2017)
#
# Core question:
#   "Where should Superstore focus its business strategy
#    to maximize profit?"
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# global chart settings
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams.update({
    'figure.dpi'       : 130,
    'axes.titlesize'   : 13,
    'axes.titleweight' : 'bold',
    'axes.labelsize'   : 11,
})


# =============================================================================
# 0. LOAD CLEAN DATA
# =============================================================================

df = pd.read_excel('Superstore_Clean.xlsx')

print("=" * 60)
print("EDA - SAMPLE SUPERSTORE")
print("=" * 60)
print(f"\nDataset loaded: {df.shape[0]:,} rows | {df.shape[1]} columns")
if 'order_date' in df.columns:
    print(f"Data period   : {df['order_date'].min().year} – {df['order_date'].max().year}\n")
else:
    print("Data period   : 2014 – 2017\n")


# =============================================================================
# 1. DESCRIPTIVE STATISTICS
# =============================================================================

print("=" * 60)
print("1. DESCRIPTIVE STATISTICS")
print("=" * 60)

numeric = df[['sales', 'quantity', 'discount', 'profit']]
print("\n", numeric.describe().round(2))

print(f"""
📌 Key observations:
   - Average discount : {df['discount'].mean():.1%} → approaching the danger zone
   - Average profit   : ${df['profit'].mean():.2f} per transaction
   - Minimum profit   : ${df['profit'].min():,.2f} (extreme loss)
   - Maximum profit   : ${df['profit'].max():,.2f}
""")


# =============================================================================
# 2. DISTRIBUTION OF NUMERIC VARIABLES
# =============================================================================

print("=" * 60)
print("2. DISTRIBUTION OF NUMERIC VARIABLES")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Distribution of Numeric Variables', fontsize=15, fontweight='bold', y=1.01)

cols_plot = {
    'sales'    : ('Sales per Transaction ($)', 'steelblue'),
    'profit'   : ('Profit per Transaction ($)', 'mediumseagreen'),
    'discount' : ('Discount Rate',              'tomato'),
    'quantity' : ('Quantity per Transaction',   'mediumpurple'),
}

for ax, (col, (title, color)) in zip(axes.flatten(), cols_plot.items()):
    sns.histplot(df[col], kde=True, ax=ax, color=color, bins=40)
    ax.set_title(title)
    ax.set_xlabel('')
    mean_val = df[col].mean()
    ax.axvline(mean_val, color='black', linestyle='--', linewidth=1.2,
               label=f'Mean: {mean_val:.2f}')
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('eda_1_distribution.png', bbox_inches='tight')
plt.show()
print("   ✅ Chart saved: eda_1_distribution.png")


# =============================================================================
# 3. CORRELATION BETWEEN NUMERIC VARIABLES
# =============================================================================

print("\n" + "=" * 60)
print("3. CORRELATION BETWEEN NUMERIC VARIABLES")
print("=" * 60)

corr = numeric.corr().round(2)
print("\n", corr)

fig, ax = plt.subplots(figsize=(7, 5))
# hide the lower triangle to avoid redundancy
mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)
for i in range(len(corr)):
    for j in range(i):
        mask.iloc[i, j] = True

sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.5, ax=ax,
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Between Numeric Variables')
plt.tight_layout()
plt.savefig('eda_2_correlation.png', bbox_inches='tight')
plt.show()

print(f"""
📌 Key observations:
   - Discount vs profit correlation : {corr.loc['discount','profit']:.2f}
     → Higher discounts tend to reduce profit
   - Sales vs profit correlation    : {corr.loc['sales','profit']:.2f}
     → High sales do not always guarantee high profit
""")
print("   ✅ Chart saved: eda_2_correlation.png")


# =============================================================================
# 4. REGIONAL PERFORMANCE
# =============================================================================

print("=" * 60)
print("4. REGIONAL PERFORMANCE")
print("=" * 60)

region_summary = df.groupby('region').agg(
    total_sales    = ('sales',    'sum'),
    total_profit   = ('profit',   'sum'),
    order_count    = ('profit',   'count'),
    loss_orders    = ('is_loss',  'sum'),
    avg_discount   = ('discount', 'mean'),
).assign(
    profit_margin  = lambda x: (x['total_profit'] / x['total_sales'] * 100).round(1),
    loss_pct       = lambda x: (x['loss_orders']  / x['order_count'] * 100).round(1),
    avg_discount   = lambda x: (x['avg_discount'] * 100).round(1)
).sort_values('profit_margin', ascending=False)

print("\n", region_summary[['total_sales', 'total_profit',
                             'profit_margin', 'avg_discount', 'loss_pct']]
     .rename(columns={
         'total_sales'   : 'Sales ($)',
         'total_profit'  : 'Profit ($)',
         'profit_margin' : 'Margin (%)',
         'avg_discount'  : 'Avg Discount (%)',
         'loss_pct'      : 'Loss Orders (%)'
     }))

# visualize
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Regional Performance Overview', fontsize=15, fontweight='bold')

colors = ['#4E79A7', '#59A14F', '#EDC948', '#E15759']

# sales & profit side-by-side
x     = region_summary.index
x_pos = range(len(x))
w     = 0.38
axes[0].bar([i - w/2 for i in x_pos], region_summary['total_sales'],
            width=w, label='Sales', color='#4E79A7', alpha=0.85)
axes[0].bar([i + w/2 for i in x_pos], region_summary['total_profit'],
            width=w, label='Profit', color='#59A14F', alpha=0.85)
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(x)
axes[0].set_title('Sales vs Profit by Region')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
axes[0].legend()

# profit margin
bars = axes[1].bar(x, region_summary['profit_margin'], color=colors, alpha=0.85)
axes[1].axhline(region_summary['profit_margin'].mean(),
                color='black', linestyle='--', linewidth=1.2, label='Average')
axes[1].set_title('Profit Margin by Region (%)')
axes[1].set_ylabel('Margin (%)')
axes[1].legend()
for bar, val in zip(bars, region_summary['profit_margin']):
    axes[1].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.15, f'{val}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

# % loss orders
bars2 = axes[2].bar(x, region_summary['loss_pct'], color=colors, alpha=0.85)
axes[2].set_title('Loss Order Rate by Region (%)')
axes[2].set_ylabel('Loss Orders (%)')
for bar, val in zip(bars2, region_summary['loss_pct']):
    axes[2].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.3, f'{val}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('eda_3_region.png', bbox_inches='tight')
plt.show()

print(f"""
📌 Key observations:
   - West    : highest margin ({region_summary.loc['West','profit_margin']}%),
               lowest loss order rate ({region_summary.loc['West','loss_pct']}%)
   - Central : paradox — 2nd highest sales but lowest margin
               ({region_summary.loc['Central','profit_margin']}%),
               highest loss order rate ({region_summary.loc['Central','loss_pct']}%)
""")
print("   ✅ Chart saved: eda_3_region.png")


# =============================================================================
# 5. PROFIT & LOSS CONCENTRATION (HEATMAPS)
# =============================================================================

print("=" * 60)
print("5. PROFIT & LOSS CONCENTRATION BY REGION & CATEGORY")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(16, 4))

# profit heatmap
pivot_profit = df.pivot_table(
    values='profit', index='category',
    columns='region', aggfunc='sum'
).round(0)

sns.heatmap(pivot_profit, annot=True, fmt='.0f', cmap='BuPu',
            linewidths=0.5, linecolor='white', ax=axes[0])
axes[0].set_title('Profit Concentration by Region & Category')
axes[0].set_xlabel('Region')
axes[0].set_ylabel('Category')

# loss heatmap
loss_only  = df[df['profit'] < 0]
pivot_loss = loss_only.pivot_table(
    values='profit', index='category',
    columns='region', aggfunc='sum'
).round(0)

sns.heatmap(pivot_loss, annot=True, fmt='.0f', cmap='RdPu_r',
            linewidths=0.5, linecolor='white', ax=axes[1])
axes[1].set_title('Loss Concentration by Region & Category')
axes[1].set_xlabel('Region')
axes[1].set_ylabel('Category')

plt.tight_layout()
plt.savefig('eda_4_heatmap.png', bbox_inches='tight')
plt.show()

print("""
📌 Key observations:
   - West & East : Office Supplies and Technology are most profitable
   - Central     : largest losses in Office Supplies (-33,484)
                   and Furniture (-19,554)
   - Furniture   : losses spread across all regions
""")
print("   ✅ Chart saved: eda_4_heatmap.png")


# =============================================================================
# 6. PROFIT BY SUB-CATEGORY
# =============================================================================

print("=" * 60)
print("6. PROFIT BY SUB-CATEGORY")
print("=" * 60)

subcat = (df.groupby('sub_category')['profit']
          .sum()
          .sort_values()
          .reset_index())

bar_colors = ['#E15759' if v < 0 else '#59A14F' for v in subcat['profit']]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(subcat['sub_category'], subcat['profit'],
               color=bar_colors, alpha=0.85)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_title('Total Profit by Sub-Category')
ax.set_xlabel('Total Profit ($)')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))

for bar, val in zip(bars, subcat['profit']):
    ax.text(val + (500 if val >= 0 else -500),
            bar.get_y() + bar.get_height() / 2,
            f'${val:,.0f}',
            va='center',
            ha='left' if val >= 0 else 'right',
            fontsize=8)

plt.tight_layout()
plt.savefig('eda_5_subcategory.png', bbox_inches='tight')
plt.show()

loss_subcat = subcat[subcat['profit'] < 0]
print(f"""
📌 Key observations:
   Loss-making sub-categories:
{loss_subcat[['sub_category','profit']].to_string(index=False)}
""")
print("   ✅ Chart saved: eda_5_subcategory.png")


# =============================================================================
# 7. DISCOUNT IMPACT ON PROFIT
# =============================================================================

print("=" * 60)
print("7. DISCOUNT IMPACT ON PROFIT")
print("=" * 60)

bucket_order  = ['0%', '1-10%', '11-20%', '21-30%', '31-50%', '51-80%']
disc_analysis = (df.groupby('discount_bucket')['profit']
                 .mean()
                 .reindex(bucket_order)
                 .reset_index())
disc_analysis.columns = ['Discount Range', 'Avg Profit']

print("\n", disc_analysis.round(2).to_string(index=False))

disc_colors = ['#59A14F' if v >= 0 else '#E15759'
               for v in disc_analysis['Avg Profit']]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(disc_analysis['Discount Range'],
              disc_analysis['Avg Profit'],
              color=disc_colors, alpha=0.85, width=0.6)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Average Profit per Discount Range')
ax.set_xlabel('Discount Range')
ax.set_ylabel('Average Profit ($)')

for bar, val in zip(bars, disc_analysis['Avg Profit']):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (1 if val >= 0 else -4),
            f'${val:.2f}',
            ha='center',
            va='bottom' if val >= 0 else 'top',
            fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('eda_6_discount_profit.png', bbox_inches='tight')
plt.show()

loss_zone = disc_analysis[disc_analysis['Avg Profit'] < 0]
print(f"""
📌 Key observations:
   - 0% discount   : highest average profit per order
   - Discount >20% : starts generating losses per order
   - Loss zone     : {', '.join(loss_zone['Discount Range'].tolist())}
""")
print("   ✅ Chart saved: eda_6_discount_profit.png")


# =============================================================================
# 8. AVERAGE DISCOUNT BY REGION & CATEGORY
# =============================================================================

print("=" * 60)
print("8. AVERAGE DISCOUNT BY REGION & CATEGORY")
print("=" * 60)

pivot_disc = df.pivot_table(
    values='discount', index='category',
    columns='region', aggfunc='mean'
).round(3) * 100  # convert to percentage

print("\n", pivot_disc.round(1))

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(pivot_disc, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=0.5, linecolor='white', ax=ax,
            cbar_kws={'label': 'Discount (%)'})
ax.set_title('Average Discount (%) by Region & Category')
ax.set_xlabel('Region')
ax.set_ylabel('Category')

plt.tight_layout()
plt.savefig('eda_7_discount_region.png', bbox_inches='tight')
plt.show()

print("""
📌 Key observations:
   - Central Furniture      : 30% — highest, 2x more than West (13%)
   - Central Office Supplies: 25% — above all other regions
   - Technology             : stable at 11–14% across all regions
""")
print("   ✅ Chart saved: eda_7_discount_region.png")


# =============================================================================
# 9. ANNUAL SALES TREND BY REGION
# =============================================================================

print("=" * 60)
print("9. ANNUAL SALES TREND BY REGION")
print("=" * 60)

if 'order_date' not in df.columns:
    print("   ⏭️  Column 'order_date' not available — trend analysis skipped.")
    print("      Use the full 21-column dataset to enable this section.\n")
else:
    df['year'] = df['order_date'].dt.year

    trend = df.groupby(['year', 'region'])['sales'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    for region, grp in trend.groupby('region'):
        ax.plot(grp['year'], grp['sales'], marker='o',
                linewidth=2, markersize=6, label=region)
        ax.annotate(f"${grp['sales'].iloc[-1]/1000:.0f}K",
                    xy=(grp['year'].iloc[-1], grp['sales'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points',
                    fontsize=9, fontweight='bold')

    ax.set_title('Annual Sales Trend by Region (2014–2017)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Sales ($)')
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
    ax.legend(title='Region')
    ax.set_xticks(trend['year'].unique())

    plt.tight_layout()
    plt.savefig('eda_8_trend.png', bbox_inches='tight')
    plt.show()

    for region in trend['region'].unique():
        g      = trend[trend['region'] == region].sort_values('year')
        start  = g['sales'].iloc[0]
        end    = g['sales'].iloc[-1]
        growth = (end - start) / start * 100
        print(f"   {region:8} | Growth 2014 → 2017: +{growth:.1f}%")

    print()
    print("   ✅ Chart saved: eda_8_trend.png")


# =============================================================================
# 10. SCATTER: SALES VS PROFIT BY STATE
# =============================================================================

print("=" * 60)
print("10. SCATTER: SALES VS PROFIT BY STATE")
print("=" * 60)

state_summary = df.groupby(['state', 'region']).agg(
    sales  = ('sales',  'sum'),
    profit = ('profit', 'sum')
).reset_index()

region_colors = {
    'West'   : '#4E79A7',
    'East'   : '#59A14F',
    'Central': '#E15759',
    'South'  : '#EDC948'
}

fig, ax = plt.subplots(figsize=(12, 7))
for region, grp in state_summary.groupby('region'):
    ax.scatter(grp['sales'], grp['profit'],
               color=region_colors[region], s=70,
               alpha=0.8, label=region)
    for _, row in grp.iterrows():
        # label only notable states (high sales or large loss/profit)
        if abs(row['profit']) > 15000 or row['sales'] > 200000:
            ax.annotate(row['state'],
                        xy=(row['sales'], row['profit']),
                        xytext=(4, 4), textcoords='offset points',
                        fontsize=8)

ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Sales vs Profit Distribution by State')
ax.set_xlabel('Total Sales ($)')
ax.set_ylabel('Total Profit ($)')
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))
ax.legend(title='Region')

plt.tight_layout()
plt.savefig('eda_9_scatter_state.png', bbox_inches='tight')
plt.show()

danger_states = state_summary[state_summary['profit'] < -10000].sort_values('profit')
print("\n   States with losses exceeding $10,000:")
print(danger_states[['state', 'region', 'sales', 'profit']].to_string(index=False))
print()
print("   ✅ Chart saved: eda_9_scatter_state.png")


# =============================================================================
# 11. EDA SUMMARY
# =============================================================================

print("\n" + "=" * 60)
print("EDA SUMMARY")
print("=" * 60)

total_sales       = df['sales'].sum()
total_profit      = df['profit'].sum()
total_loss_amount = df[df['profit'] < 0]['profit'].sum()
loss_order_pct    = df['is_loss'].mean() * 100
avg_discount      = df['discount'].mean() * 100

print(f"""
  BUSINESS OVERVIEW
  ─────────────────────────────────────────────
  Total Sales         : ${total_sales:>12,.0f}
  Total Profit        : ${total_profit:>12,.0f}
  Profit Margin       : {total_profit/total_sales*100:>11.2f}%
  Avg Discount        : {avg_discount:>11.2f}%
  Total Losses        : ${total_loss_amount:>12,.0f}
  Loss Order Rate     : {loss_order_pct:>11.1f}%

  KEY FINDINGS
  ─────────────────────────────────────────────
  1. The business is PROFITABLE (margin {total_profit/total_sales*100:.2f}%),
     but {loss_order_pct:.1f}% of orders generate losses

  2. West    → best margin ({region_summary.loc['West','profit_margin']}%),
               lowest loss order rate ({region_summary.loc['West','loss_pct']}%)

  3. Central → paradox: 2nd highest sales,
               lowest margin ({region_summary.loc['Central','profit_margin']}%),
               highest loss order rate ({region_summary.loc['Central','loss_pct']}%)

  4. Discounts above 20% consistently generate losses per order

  5. Central applies 30% discount on Furniture —
     2x higher than West (13%)

  → Further analysis continued in Tableau Dashboard
""")

print("=" * 60)
print("EDA complete. All charts saved to the working directory.")
print("=" * 60)
