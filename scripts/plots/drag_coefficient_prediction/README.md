# Drag Coefficient Prediction

This script generates 50 random drag coefficient ($C_d$) samples and two corresponding sets of predicted values with small added random errors, simulating the output of two different prediction models. It fits a linear regression line to each dataset and plots both scatter clouds alongside their regression lines on a $C_d$ vs $C_{d,pred}$ axes, making it straightforward to assess model accuracy and compare the two predictors visually.

![output](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/e3c6d538-6bfc-4cb0-8a16-6a41c4da6564)

## Overview

- 50 randomly sampled $C_d$ values spanning a representative range
- Two predicted datasets with independent random perturbations (red and blue markers)
- Linear regression fit for each dataset displayed as a trend line
- Perfect-prediction identity line ($C_{d,pred} = C_d$) as a reference

## Mathematical Background

### Drag Coefficient

The drag coefficient non-dimensionalises the aerodynamic drag force $F_D$ acting on a body:

$$C_d = \frac{F_D}{\frac{1}{2}\rho U^2 A}$$

where $\rho$ is the fluid density, $U$ is the free-stream velocity, and $A$ is the reference area.

### Linear Regression

For each dataset, the slope $m$ and intercept $b$ are found by minimising the residual sum of squares:

$$\min_{m,\,b}\sum_{i=1}^{N}\!\left(C_{d,pred,i} - m\,C_{d,i} - b\right)^2$$

The analytical solution is $m = \frac{\sum(C_d - \bar{C}_d)(C_{d,pred} - \overline{C_{d,pred}})}{\sum(C_d - \bar{C}_d)^2}$, $b = \overline{C_{d,pred}} - m\bar{C}_d$.

### Perfect Prediction and R²

A perfect model satisfies $C_{d,pred} = C_d$ (slope = 1, intercept = 0). The coefficient of determination measures goodness of fit:

$$R^2 = 1 - \frac{\sum_i(C_{d,pred,i} - C_{d,i})^2}{\sum_i(C_{d,i} - \bar{C}_d)^2}$$

## Implementation

1. Generate 50 random $C_d$ samples uniformly in a chosen range.
2. Create two predicted datasets by adding small independent Gaussian noise to the samples.
3. Fit a least-squares linear regression to each dataset using `numpy.polyfit`.
4. Plot scatter points for both datasets and overlay the regression lines.
5. Draw the identity reference line and annotate with slope, intercept, and $R^2$ values.

## Output

The script displays and saves `drag_coefficient_prediction.png`: a scatter plot of $C_d$ vs $C_{d,pred}$ for two prediction models (red and blue markers) with their linear regression lines and the identity reference, enabling rapid visual comparison of prediction accuracy.

