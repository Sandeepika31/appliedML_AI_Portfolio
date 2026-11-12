# What Drives the Price of a Car?

**Practical Application II -- Used Car Pricing Analysis**

Full analysis script: [`prompt_II.py`](./prompt_II.py)

> This script runs the complete CRISP-DM workflow end-to-end as a plain Python script (no Jupyter required). Run it with:
> ```
> python prompt_II.py
> ```
> Console output includes all data summaries, model results, and the business report. All charts are saved as PNG files to the `output_plots/` folder.

---

## Business Understanding

Given ~426,000 used-vehicle listings described by numeric and categorical attributes (`year`, `odometer`, `manufacturer`, `model`, `condition`, `cylinders`, `fuel`, `title_status`, `transmission`, `drive`, `size`, `type`, `paint_color`, `region`/`state`), this is framed as a **supervised regression problem**: predict `price` from vehicle attributes, with the primary goal being **inference** -- quantifying which features move price up or down, holding other factors constant -- so the findings can be turned into actionable dealership recommendations.

## Data Understanding & Preparation (summary)

- Raw dataset: 426,880 rows / 18 columns, with major data-quality issues: `price` ranging from $0 to $3.7B, `odometer` up to 10,000,000 miles, `year` as early as 1900, and heavy missingness in `size` (72%), `cylinders` (42%), `condition` (41%), `VIN` (38%), `drive` (31%), `paint_color` (31%).
- Cleaning steps: dropped `id`/`VIN`/`model`/`region` (pure identifiers or excessive cardinality), filtered implausible `price` ($500-$150,000), `year` (1990-2022), and `odometer` (0-300,000) values, engineered an `age` feature, imputed missing categoricals as an explicit `'unknown'` level, mapped `cylinders` to a numeric feature, and log-transformed the right-skewed `price` and `odometer`.
- Final modeling dataset: **367,218 rows**, with 3 numeric features (`age`, `log_odometer`, `cylinders_num`) and 10 categorical features one-hot encoded.

## Modeling & Results

Five regression approaches were trained and compared (metrics on held-out test set, dollar scale):

| Model              | R² (log, test) | R² ($, test) | RMSE ($, test) | MAE ($, test) |
|--------------------|:--------------:|:------------:|:---------------:|:---------------:|
| Linear Regression  | 0.632          | 0.625        | 8,997           | 5,484            |
| Ridge (tuned)      | 0.632          | 0.623        | 9,021           | 5,492            |
| Lasso (tuned)      | 0.627          | 0.617        | 9,099           | 5,507            |
| **Random Forest**  | **0.808**      | **0.818**    | **6,263**        | **3,428**         |
| Poly(2) + Ridge    | 0.664          | 0.634        | 8,893            | 5,266            |

- The **Random Forest** benchmark achieves the highest accuracy, confirming meaningful non-linear/interaction effects (e.g. age x mileage, manufacturer x type) that linear models can't fully capture.
- Among interpretable (linear-family) models, **Poly(2)+Ridge** performs best, and was selected as the primary explanatory model for extracting business-meaningful coefficients.

### Top Price Drivers (from Poly(2)+Ridge coefficients on log price)

| Feature                  | Coefficient | Direction |
|---------------------------|:-----------:|:---------:|
| `manufacturer_porsche`    | +0.67       | ↑ premium brand |
| `condition_salvage`       | -0.65       | ↓ damaged title |
| `log_odometer²`           | -0.62       | ↓ non-linear mileage penalty |
| `log_odometer`            | +0.60*      | mileage/age interaction |
| `condition_fair`          | -0.56       | ↓ poor condition |
| `fuel_diesel`              | +0.54       | ↑ diesel premium |
| `manufacturer_tesla`      | +0.53       | ↑ premium brand |
| `manufacturer_fiat`       | -0.53       | ↓ budget brand |
| `title_status_missing`    | -0.46       | ↓ incomplete listing |
| `age`                     | -0.41       | ↓ every extra year reduces price |

*(see `output_plots/06_top_price_drivers.png` for the full top-25 chart; sign of `log_odometer` is interpreted jointly with its squared/interaction terms)*

## Evaluation Summary

- Regularized linear models (Ridge/Lasso) perform essentially on par with plain Linear Regression after data cleaning -- multicollinearity among one-hot dummy columns was not a major issue.
- Adding degree-2 polynomial terms on numeric predictors gives a modest R² lift, confirming some non-linearity in how age and mileage jointly affect price (mileage penalty is steeper on newer cars).
- Random Forest's independent feature-importance ranking broadly corroborates the linear coefficients (age, odometer, manufacturer, condition, fuel=diesel, drive=4wd all rank highly in both models) -- giving confidence these are genuine price drivers, not model artifacts.
- Residuals are reasonably well-behaved and roughly symmetric around zero for mid-range prices, with higher variance at the low/high ends of the price range (cheap salvage vehicles and rare premium/luxury vehicles).

## Deployment: Report for the Dealership

**Key Takeaways for Inventory & Pricing Decisions:**

1. **Age is the single strongest price driver.** Every additional year of vehicle age drives a substantial, consistent price drop -- prioritize newer trade-ins.
2. **Mileage matters, but its effect compounds with age.** The price penalty for high mileage is steeper on newer cars than older ones.
3. **Manufacturer brand tier has a large, persistent effect.** Premium/luxury marques (e.g. Porsche, Tesla) command a premium; budget brands (e.g. Fiat, Mercury) sit at a discount, even after controlling for age/mileage/condition.
4. **Condition and title status are strong, actionable signals.** "Excellent"/"like new" condition and clean titles carry meaningful premiums over "fair"/"salvage"/missing-title vehicles.
5. **Drivetrain and fuel type carry notable premiums.** 4WD and diesel vehicles price higher than FWD/RWD and gas, respectively.
6. **Vehicle body type matters for inventory positioning.** Pickups/trucks/SUVs tend to price higher than sedans/hatchbacks/coupes of comparable age and mileage.
7. **Complete listings command a premium.** Missing/unknown attribute levels (condition, cylinders, drive, size, title status) are themselves associated with lower sale prices -- data completeness is a lever dealers can pull.

**Recommended Next Steps:**
- Use the fitted model's predicted price as a pricing sanity-check tool (flag listings that deviate >15-20% from the model's prediction).
- Prioritize sourcing vehicles with the strongest positive price drivers identified above, subject to acquisition cost.
- Refresh training data periodically as market dynamics shift.
- Explore manufacturer x type interaction effects and regional price variation as follow-up analysis.

---

## Files in This Project

| File | Description |
|------|-------------|
| [`prompt_II.py`](./prompt_II.py) | **Standalone Python script** -- runs the full analysis end-to-end (`python prompt_II.py`), prints results to console, saves all charts to `output_plots/`. |
| `prompt_II.ipynb` | Original Jupyter notebook version of the same analysis. |
| `data/vehicles.csv` | Source dataset (~426K used-vehicle listings). |
| `output_plots/` | Generated charts (missing values, distributions, price relationships, model comparison, top price drivers, residuals, feature importances). |
