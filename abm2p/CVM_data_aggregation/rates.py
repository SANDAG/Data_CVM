import pandas as pd


def summarize_rates(
    trips: pd.DataFrame,
    totals: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'tours_per_emp': _summarize_tours_per_emp(totals=totals),
            'trips_per_tour': _summarize_trips_per_tour(totals=totals),
            'avg_trip_len': _summarize_avg_trip_len(totals=totals),
            'pct_light': _summarize_pct_light(totals=totals),
        }
    )


def _summarize_tours_per_emp(
    totals: pd.DataFrame,
) -> pd.Series:
    return totals.tours / totals.emp


def _summarize_trips_per_tour(
    totals: pd.DataFrame,
) -> pd.Series:
    return totals.trips / totals.tours


def _summarize_avg_trip_len(
    totals: pd.DataFrame,
) -> pd.Series:
    return totals.vmt / totals.trips


def _summarize_pct_light(
    totals: pd.DataFrame,
) -> pd.Series:
    return (totals.vmt - totals.med_heavy_vmt) / (totals.vmt)
