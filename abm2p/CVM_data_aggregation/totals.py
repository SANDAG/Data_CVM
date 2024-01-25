import pandas as pd


def summarize_totals(
    emp: pd.DataFrame,
    tours: pd.DataFrame,
    trips: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        data={
            'emp': _summarize_emp(emp=emp),
            'tours': _summarize_tours(tours=tours),
            'trips': _summarize_trips(trips=trips),
            'vmt': _summarize_vmt(trips=trips),
            'med_heavy_vmt': _summarize_med_heavy_vmt(trips=trips),

        }
    )


def _summarize_emp(
    emp: pd.DataFrame,
) -> pd.Series:
    return emp.emp


def _summarize_tours(
    tours: pd.DataFrame,
) -> pd.Series:
    return (
        tours
        .reset_index()
        .groupby('industry')
        ['tour_id']
        .count()
    )


def _summarize_trips(
    trips: pd.DataFrame,
) -> pd.Series:
    # TODO: Weight if that's neccessary
    return (
        (
            trips
            .reset_index()
            .groupby('industry')
            ['weight_trip']
            .sum()
            .astype('int64')
        )
    )


def _summarize_vmt(
    trips: pd.DataFrame,
) -> pd.Series:
    return (
        (
            trips
            .assign(vmt=lambda df: df.weight_trip * df.distance)
            .groupby('industry')
            ['vmt']
            .sum()
        )
    )


def _summarize_med_heavy_vmt(
    trips: pd.DataFrame,
) -> pd.Series:
    return (
        (
            trips
            .assign(vmt=lambda df: df.weight_trip * df.distance)
            .query(
                "`mode` == 'Medium Heavy Duty Truck'"
                " or `mode` == 'Heavy Heavy Duty Truck'"
            )
            .groupby('industry')
            ['vmt']
            .sum()
        )
    )
