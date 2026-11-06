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
    alpha = 0.05  # significance level
    number_of_bins = 8  # number of bins for histogram
    participant = "F"  # participant ID for Task 3

    # Read in the RSI data from the csv file
    df = pd.read_csv("../../data/drop-jump/all_participant_data_rsi.csv")
    # ======================================================
    # Task 1 - Paired T-Test
    # ======================================================
    print("\nTASK 1")
    print("--------------------")

    # Get both RSI values for both methods
    force_plate = df["force_plate_rsi"]
    accelerometer = df["accelerometer_rsi"]

    # Perform paired t-test since both measure same jumps
    t_stat, p_value = stats.ttest_rel(force_plate, accelerometer)

    
    print("Null Hypothesis (H0):")
    print("The mean force plate RSI equals the mean accelerometer RSI")

    print("\nAlternative Hypothesis (Ha):")
    print("The mean force plate RSI does not equal the mean accelerometer RSI")

    # Print test results
    print(f"\nt statistic = {t_stat:.4f}")
    print(f"p value = {p_value:.6f}")
    print(f"Alpha level = {alpha}")

    # Check statistical significance
    if p_value < alpha:
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

    
    accel_data = df["accelerometer_rsi"]

    # Fit a normal distribution by estimating the mean
    # and the standard deviation from the data
    mean, std = stats.norm.fit(accel_data)
    print(f"Fitted mean = {mean:.4f}")
    print(f"Fitted standard deviation = {std:.4f}")

    # Create histogram data
    # observed is how many values are in each bin
    # bins are the bin edges
    observed , bins = np.histogram(accel_data, bins=number_of_bins)

    expected = []

    # Find the expected frequencies assuming data follows normal distribution
    for i in range(number_of_bins):

        if i == 0:
            # First bin: everything below the right edge of bin
            # Normal curve continues to negative infinity
            # So left edge treated as negative infinity
            probability = stats.norm.cdf(bins[1], mean, std)

        elif i == number_of_bins - 1:
            # Last bin: everything above the left edge of bin
            # Normal curve continues to positive infinity
            # So right edge treated as positive infinity
            probability = 1 - stats.norm.cdf(bins[i], mean, std)

        else:
            # Middle bins: everything between the left and right edges of the bin
            probability = (
            stats.norm.cdf(bins[i + 1], mean, std)
            - stats.norm.cdf(bins[i], mean, std)
            )
        # Expected count = probability * total number of observations
        expected.append(probability * len(accel_data))

    
    expected = np.array(expected)

    # Perform chi-square goodness of fit test
    # ddof = 2 because we estimated two parameters (mean and std) from the data
    chi2_stat, p_value = stats.chisquare(observed, expected, ddof=2)
    degrees_of_freedom = number_of_bins - 1 - 2 
    print(f"\nDegrees of freedom = {degrees_of_freedom}")
    print("\nObserved counts:", observed)
    print("Expected counts:", np.round(expected, 2))

    print(f"\nChi-square statistic = {chi2_stat:.4f}")
    print(f"p value = {p_value:.6f}")
    print(f"Alpha level = {alpha}")

    # Determine whether the normal distribution is a good fit
    if p_value < alpha:
        print("Conclusion: Data is NOT a good normal fit")
    else:
        print("Conclusion: Data is a good normal fit")

    # ------------------------------------------------------------
    # Histogram with fitted normal distribution
    # -------------------------------------------------------------

    # Points used to plot the normal curve
    x = np.linspace(min(accel_data), max(accel_data), 300)

    plt.figure(figsize=(8,5))

    # Draw histogram of accelerometer RSI values
    plt.hist(accel_data, bins=number_of_bins, density=True, alpha=0.7, edgecolor="black", label="Accelerometer RSI")

    # Fitted normal distribution curve
    plt.plot(x, stats.norm.pdf(x, mean, std), color="red", linewidth=2, label="Fitted Normal Curve")
    plt.xlabel("Accelerometer RSI")
    plt.ylabel("Density")
    plt.title("Histogram of Accelerometer RSI with Fitted Normal Curve")
    plt.legend()
    plt.grid(True)
    plt.show()

    # ===================================================================
    # Task 3 - SELECTED PARTICIPANT
    # ===================================================================

    print("\nTASK 3")
    print("---------------------------")

    # Select only the rows belonging to the selected participant
    # The trial names start with the participant letter, like "F_trial_1"
    participant_data = df[df["trial"].str.startswith(participant + "_")]

    
    print(f"\nParticipant {participant} Data:")
    print(participant_data)

    # Get Participant's measurements
    force_f = participant_data["force_plate_rsi"]
    accel_f = participant_data["accelerometer_rsi"]

    # Confidence interval using t-distribution
    confidence = 1 - alpha

    force_ci = stats.t.interval(
        confidence,
        df=len(force_f) - 1,
        loc=np.mean(force_f),
        scale=stats.sem(force_f)
    )

    accel_ci = stats.t.interval(
        confidence,
        df=len(accel_f) - 1,
        loc=np.mean(accel_f),
        scale=stats.sem(accel_f)
    )
    print(f"\nForce Plate RSI Mean: {np.mean(force_f):.4f}")
    print(f"Force Plate RSI 95% Confidence Interval: "
        f"{force_ci[0]:.4f} to {force_ci[1]:.4f}")
    print(f"\nAccelerometer RSI Mean: {np.mean(accel_f):.4f}")
    print(f"Accelerometer RSI 95% Confidence Interval: "
        f"{accel_ci[0]:.4f} to {accel_ci[1]:.4f}")
        
if __name__ == "__main__":
    main()