# Data_Analytics_Bootcamp_Project_Superstore
Bootcamp project analyzing Superstore profitability by region using  Python &amp; Tableau. Key finding: discounts above 20% always generate  losses. Central region's 24% avg discount explains its poor 7.9%  margin vs West's 14.9%. Potential profit recovery: +$197K (+68%).

## Superstore Regional Profitability & Discount Analysis

This project is the capstone dashboard assignment from the Dibimbing 
Data Analytics Offline Bootcamp (Batch #3), built using Python and 
Tableau Public on the Sample Superstore dataset (2014–2017).

The analysis began during Exploratory Data Analysis in Python, where 
a significant profitability gap was discovered across US regions — 
confirmed statistically via ANOVA testing (p = 0.049) and a 
Coefficient of Variation of 25.07%. This finding motivated a 
regional lens to investigate where and why the business was losing 
money despite overall healthy performance ($2.3M Sales, 12.47% 
Profit Margin).

The core finding: any discount above 20% consistently generates 
losses (-$45 to -$156 per order), yet Central region applies an 
average discount of 24% — placing the majority of its orders 
structurally in the loss zone. West region, by contrast, maintains 
an 11% average discount and achieves a 14.9% profit margin. Michigan 
(Central region) proves geography is not destiny — with 1% discount 
it achieves 32% margin.

Three interactive Tableau dashboards were built to tell this story: 
a Regional Overview (KPIs, map, trend, scatter), a Regional Sales 
Analysis (bar chart, treemap), and a Profitability & Discount 
Analysis (sub-category bar, margin dot plot, discount heatmap, 
discount-profit bar). The analysis concludes with data-backed 
tailored recommendations for each of the four regions, with a 
potential profit recovery of +$197,000 (+68%) through discount 
policy reform alone.

**Tools:** Python (Pandas, Matplotlib, Seaborn, SciPy) · Tableau Public  
**Dataset:** Sample Superstore · 9,994 rows · 13 features · 2014–2017  
**Key Skills:** EDA, Statistical Testing, Data Visualization, Dashboard Design, Business Storytelling
