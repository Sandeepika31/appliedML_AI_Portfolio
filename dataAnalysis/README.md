\## Overview



This script performs an end-to-end exploratory data analysis (EDA) on in-vehicle coupon recommendation data to answer the core question:



> \*\*"Will a customer accept a coupon delivered to their car?"\*\*



It is based on the UCI / Amazon Mechanical Turk survey dataset (`coupons.csv`) and covers data cleaning, statistical segmentation, and visualization across multiple coupon types — with a deep-dive into \*\*Bar\*\* and \*\*Coffee House\*\* coupons.



\---



\## Table of Contents



1\. \[Project Structure](#project-structure)

2\. \[Requirements](#requirements)

3\. \[How to Run](#how-to-run)

4\. \[Script Walkthrough](#script-walkthrough)

5\. \[Generated Plots](#generated-plots)

6\. \[Key Findings](#key-findings)

7\. \[Configuration](#configuration)



\---



\## Project Structure



```

dataAnalysis/EDA\_CouponsBusiness

│

├── coupon\_analysis.py          ← Main analysis script (this file)

├── prompt.ipynb                ← Original assignment notebook

│

├── data/

│   └── coupons.csv             ← Source dataset (12,684 rows × 26 columns)

│

├── plots/                      ← Auto-generated output charts

│   ├── 01\_coupon\_distribution.png

│   ├── 02\_temperature\_histogram.png

│   ├── 03\_bar\_coupon\_acceptance\_segments.png

│   ├── 04\_coffeehouse\_heatmap\_time\_passenger.png

│   ├── 05\_coffeehouse\_acceptance\_by\_frequency.png

│   └── 06\_acceptance\_by\_coupon\_type.png

│



```



\---



\## Requirements



| Package      | Purpose                          |

|--------------|----------------------------------|

| `pandas`     | Data loading, cleaning, grouping |

| `numpy`      | Numeric operations               |

| `matplotlib` | Base plotting (non-interactive)  |

| `seaborn`    | Statistical visualizations       |



Install all dependencies with:



```bash

pip install pandas numpy matplotlib seaborn

```



> \*\*Python version:\*\* 3.8 or higher recommended.



\---



\## How to Run



```bash

\# From the project root directory

python coupon\_analysis.py

```



All six plots are saved automatically to the `plots/` directory. Console output shows acceptance rates and segment statistics at each analysis step.



\---



\## Script Walkthrough



\### Step 1 — Load Data

Reads `coupons.csv` into a Pandas DataFrame and prints shape and a preview.



\### Step 2 — Investigate Missing Data

Identifies columns with null values. Key finding: the `car` column is \*\*\~99% missing\*\* and is flagged for removal.



\### Step 3 — Handle Missing Data

\- \*\*Drops\*\* the `car` column entirely (insufficient data).

\- \*\*Fills\*\* missing values in five frequency columns (`Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50`) using the \*\*column mode\*\* (most frequent value).



\### Step 4 — Overall Acceptance Rate

Computes the proportion of all coupons that were accepted (`Y == 1`).



\### Step 5 — Coupon Type Distribution (Plot 01)

Bar chart showing the count of each coupon type in the dataset.



\### Step 6 — Temperature Distribution (Plot 02)

Histogram of the ambient temperature at the time of the survey.



\### Step 7 — Bar Coupon Deep-Dive

Filters to Bar coupons only and evaluates acceptance across multiple driver segments:



| Segment | Condition |

|---------|-----------|

| Visit frequency | ≤3 vs >3 bar visits/month |

| Age + frequency | >1 bar visit/month AND age > 25 |

| Lifestyle filter | >1 bar visit/month, no kid passenger, not in farming/fishing/forestry |

| Combined | Union of three compound conditions |



Produces \*\*Plot 03\*\* — a grouped bar chart comparing all segments.



\### Step 8 — Coffee House Independent Investigation

Filters to Coffee House coupons and analyses acceptance by:

\- Time of day

\- Passenger type

\- Visit frequency

\- Weather conditions



Produces \*\*Plot 04\*\* (heatmap: passenger × time) and \*\*Plot 05\*\* (acceptance by visit frequency).



\### Step 9 — Acceptance by Coupon Type (Plot 06)

Compares acceptance rates across all five coupon types with an overall average reference line.



\---



\## Generated Plots



| File | Description |

|------|-------------|

| `01\_coupon\_distribution.png` | Count of each coupon type in the dataset |

| `02\_temperature\_histogram.png` | Distribution of survey temperatures |

| `03\_bar\_coupon\_acceptance\_segments.png` | Bar coupon acceptance by driver segment |

| `04\_coffeehouse\_heatmap\_time\_passenger.png` | Coffee House acceptance: passenger × time heatmap |

| `05\_coffeehouse\_acceptance\_by\_frequency.png` | Coffee House acceptance by visit frequency |

| `06\_acceptance\_by\_coupon\_type.png` | Acceptance rate comparison across all coupon types |



\---



\## Key Findings



\### Bar Coupons

\- Drivers who visit bars \*\*more than once a month\*\*, are \*\*under 30 years old\*\*, travel \*\*without kids\*\*, and are \*\*not in farming/fishing/forestry\*\* occupations show significantly higher acceptance rates.

\- High-frequency bar visitors (>3 visits/month) accept bar coupons at a much higher rate than low-frequency visitors.



\### Coffee House Coupons

\- Acceptance is highest during \*\*morning and afternoon hours\*\*.

\- Drivers travelling \*\*with friends\*\* or \*\*alone\*\* accept more than those with kids or partners.

\- Regular coffee house visitors (1–3 or 4–8 visits/month) show the highest acceptance rates.



\### Overall

\- \*\*Carry-out \& Take Away\*\* and \*\*Restaurant (<$20)\*\* coupons have the highest overall acceptance rates.

\- \*\*Bar\*\* coupons have the lowest overall acceptance rate but show strong lift for targeted segments.



\---



\## Configuration



Two path constants at the top of the script can be updated to match your local environment:



```python

DATA\_PATH = r'path\\to\\data\\coupons.csv'

OUT\_DIR   = r'path\\to\\output\\plots'

```



The `OUT\_DIR` is created automatically if it does not exist.



\---



\## Author

Sandeepika

