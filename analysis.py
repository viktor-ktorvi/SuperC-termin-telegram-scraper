import math
from pathlib import Path

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt

def filter_out_strings_in_messages(df: pd.DataFrame, banned_strings: list[str]) -> pd.DataFrame:
    """
    Filter out messages that contain specific strings.
    Parameters
    ----------
    df: pd.DataFrame
        Data frame.
    banned_strings: list[str]
        Banned strings.

    Returns
    -------
        Filtered data frame.
    """
    for banned_string in banned_strings:
        df = df[df["message"].str.contains(banned_string) == False]

    return df


def main():
    """
    Analyze the times at which the appointments are given out.
    Returns
    -------

    """
    matplotlib.rcParams.update({"font.size": 22})

    filepath = Path("@aachen_termin/@aachen_termin.csv")
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")

    df = df.tz_localize("UTC")
    df = df.tz_convert("Europe/Berlin")

    df.to_csv(Path(''.join(filepath.parts[:-1])) / f"{filepath.stem}_CET{filepath.suffix}")


    df = filter_out_strings_in_messages(df, ["Hello!", "No appointment available", "Familien", "Mitarbeitende"])

    df = df.loc["2025-01-01 00:00:00":]

    fig, axs = plt.subplots(1, 2, figsize=(20, 12))
    # fig.tight_layout()
    fig.suptitle("Common appointment times 2025")
    
    df["id"].groupby(df.index.dayofweek).count().plot(kind="bar", ax=axs[0])
    days_of_the_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    axs[0].set_xlabel("Day of week")
    axs[0].set_xticklabels(days_of_the_week, rotation=30)

    hour_histogram = df["id"].groupby(df.index.hour).count()
    hour_histogram.plot(kind="bar", ax=axs[1], rot=0)
    axs[1].set_xlabel("Hour of day")

    fig.savefig("day_of_week_and_hour_of_day_2025.png", bbox_inches="tight")

    square_num_most_common_hours = 4
    most_common_hours = sorted(hour_histogram.nlargest(square_num_most_common_hours).index.tolist())

    n_rows = int(math.sqrt(square_num_most_common_hours))
    fig, axs = plt.subplots(n_rows, n_rows, figsize=(20, 12))
    fig.suptitle("Common appointment minutes in the most common hours")
    for i in range(n_rows):
        for j in range(n_rows):
            hour = most_common_hours[i * n_rows + j]
            ax = axs[i, j]
            ax.set_title(f"{hour}h")
            hour_specific_df = df.loc[df.index.hour == hour]
            hour_specific_df["id"].groupby(hour_specific_df.index.minute).count().reindex(range(60), fill_value=0).plot.bar(ax=ax)
            ax.set_xticks([0, 15, 30, 45])
            ax.set_xlabel("minute")

    fig.tight_layout()

    fig.savefig("most_common_hours_by_minute_2025.png", bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()