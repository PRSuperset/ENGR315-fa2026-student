"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def main():

    # Read in the RSI data from the csv file
    df = pd.read_csv("data/drop-jump/all_participant_data_rsi.csv")
    # ======================================================
    # Task 1 - Paired T-Test
    # ======================================================
    print("\nTASK 1")
    print("--------------------")

    # Store the two RSI measurement methods as variables
    force_plate = df["force_plate_rsi"]
    accelerometer = df["accelerometer_rsi"]
    t_stat, p_value = stats.ttest_rel(force_plate, accelerometer)

    # Print hypotheses as required by assignment
    print("Null Hypothesis (H0):")
    print("The mean force plate RSI equals the mean accelerometer RSI")

    print("\nAlternative Hypothesis (Ha):")
    print("The mean force plate RSI does not equal the mean accelerometer RSI")

    # Print test results
    print(f"\nt statistic = {t_stat:.4f}")
    print(f"p value = {p_value:.6f}")
    print(f"Alpha level = 0.05")

    # Compare p value to the alpha level of 0.05
    if p_value < 0.05:
        print("\nDecision: Reject H0")
        print("The two measurement methods are significantly different.")
    else:
        print("\nDecision: Fail to Reject H0")
        print("No significant difference was detected.")

    # ========================================================================
    # Task 2 - CHI SQUARE GOODNESS OF FIT TEST
    # ========================================================================

    print("\nTASK 2")
    print("---------------------------")

    # Use only the accelerometer RSI values
    accel_data = df["accelerometer_rsi"]

    # Fit a normal distribution by estimating the mean
    # and the standard deviation from the data
    mean, std = stats.norm.fit(accel_data)

    # Create histogram data
    # observed is how many values are in each bin
    # bins are the bin edges
    observed , bins = np.histogram(accel_data, bins=8)

    # Create a list to store the expected frequencies
    expected = []

    # Find the expected frequencies assuming data follows normal distribution
    for i in range(len(bins) - 1):
        probability = (
            stats.norm.cdf(bins[i + 1], mean, std)
            - stats.norm.cdf(bins[i], mean, std)
        )

        expected.append(probability * len(accel_data))

    # Convert list to numpy array
    expected = np.array(expected)

    # Scale expected counts so total number of expected observations equals total observed
    expected = expected * (sum(observed) / sum(expected))

    # Perform chi-square goodness of fit test
    chi2_stat, p_value = stats.chisquare(observed, expected)

    print("Chi-square statistic =", round(chi2_stat, 4))
    print("p value =", round(p_value, 6))
    print(f"Alpha level = 0.05")

    # Determine whether the normal distribution is a good fit
    if p_value < 0.05:
        print("Conclusion: Data is NOT a good normal fit")
    else:
        print("Conclusion: Data is a good normal fit")

    # ------------------------------------------------------------
    # Histogram with fitted normal distribution
    # -------------------------------------------------------------

    # Create x values for the smooth normal curve
    x = np.linspace(min(accel_data), max(accel_data), 300)

    plt.figure(figsize=(8,5))

    # Draw histogram of accelerometer RSI values
    plt.hist(accel_data, bins=8, density=True, alpha=0.7, label="Accelerometer RSI")

    # Fitted normal distribution curve
    plt.plot(x, stats.norm.pdf(x, mean, std), color="red", linewidth=2, label="Fitted Normal Curve")
    plt.xlabel("Accelerometer RSI")
    plt.ylabel("Density")
    plt.title("Histogram of Accelerometer RSI with Fitted Normal Curve")
    plt.legend()
    plt.grid(True)
    plt.show()

    # ===================================================================
    # Task 3 - PARTICIPANT F
    # ===================================================================

    print("\nTASK 3")
    print("---------------------------")

    # Select only the rows belonging to participant F
    # The trial names start with "F_"
    participant_f_data = df[df["trial"].str.startswith("F_")]

    # Print participant F dataframe
    print("\nParticipant F Data:")
    print(participant_f_data)

    # Seperate the force plate and accelerometer RSI values
    force_f = participant_f_data["force_plate_rsi"]
    accel_f = participant_f_data["accelerometer_rsi"]

    force_ci = stats.t.interval(
        confidence=0.95,
        df=len(force_f) - 1,
        loc=np.mean(force_f),
        scale=stats.sem(force_f)
    )

    accel_ci = stats.t.interval(
        confidence=0.95,
        df=len(accel_f) - 1,
        loc=np.mean(accel_f),
        scale=stats.sem(accel_f)
    )

    print(
        f"Force Plate RSI 95% Confidence Interval: {force_ci[0]:.4f} to {force_ci[1]:.4f}"
    )
    print(
        f"Accelerometer RSI 95% Confidence Interval: {accel_ci[0]:.4f} to {accel_ci[1]:.4f}"
    )
if __name__ == "__main__":
    main()