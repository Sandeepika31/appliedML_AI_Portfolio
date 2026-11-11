CAPSTONE ML PROJECT — Capacity Expansion Candidate Prediction

This script REUSES the cell-level KPI dataset produced by
`r_project_analysis_v2_prb_phase3.py` (the "r_cell_info_merged_*.csv" file)
and turns it into a complete, textbook end-to-end Machine-Learning
pre-processing + modelling pipeline, covering the three techniques the
capstone specifically asks for:

    1. Missing-value & data-inconsistency handling   (STEP 3)
    2. Train / Test split methodology                (STEP 6)
    3. Categorical encoding techniques for ML models  (STEP 5)

...plus a full workflow around them (EDA, target engineering, baseline
model training & evaluation) so the result is a genuine, runnable
capstone deliverable rather than just a cleaning script.

Pipeline
--------
STEP 1  Load baseline cell-level dataset (output of phase3 pipeline)
STEP 2  Missing-value / inconsistency AUDIT (before cleaning)
STEP 3  DATA CLEANING
          3a. Remove exact duplicate rows
          3b. Remove duplicate Cell Name rows
          3c. Fix out-of-range / impossible values -> NaN
          3d. Standardise categorical text (trim, unify blanks)
          3e. Impute missing values
                - numeric      -> median imputation (SimpleImputer)
                - categorical  -> mode / 'Unknown' imputation
          3f. Outlier capping (IQR method) on key KPIs
STEP 4  FEATURE ENGINEERING — define the ML target
          Capacity_Expansion_Needed = 1 if Avg DL PRB Util > threshold else 0
          + CQI_bin (ordinal bucket of Avg CQI)
STEP 5  ENCODING TECHNIQUES
          - One-Hot Encoding       -> nominal categorical features
                                      (ClutterType, TYPE, O-RU, Region, ...)
          - Ordinal/Label Encoding -> CQI_bin (has a natural order)
          - StandardScaler         -> numeric features
STEP 6  TRAIN / TEST SPLIT (stratified, 80/20, reproducible random_state)
STEP 7  BASELINE MODEL TRAINING (Logistic Regression + Random Forest)
STEP 8  MODEL EVALUATION (accuracy / precision / recall / F1 / ROC-AUC,
         confusion matrix, feature importance)
STEP 9  SAVE ARTIFACTS (cleaned data, train/test CSVs, encoders, models,
         plots) for reuse in downstream notebooks / deployment.

Input
-----
  r_cell_info_merged_*.csv   (produced by r_project_analysis_v2_prb_phase3.py)
  falls back to r_cell_info_merged.csv (produced by data_cleaning_BBH.py)

