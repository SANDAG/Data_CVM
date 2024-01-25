from pathlib import Path

import pandas as pd


def extract_emp_data(path: str | Path) -> pd.DataFrame:
    
    # TODO: Figure out why Fleet Allocator isn't in this and add it.
    return (
        pd.read_csv(
            path,
            usecols=[
                'TAZ',
                'CVM_IN',
                'CVM_RE',
                'CVM_SV',
                'CVM_TH',
                'CVM_WH',
                'CVM_GO',
            ]
        )
        .pipe(_rename_industry_cols)
        .pipe(_melt_industry_cols)
        .pipe(_aggregate_industry_cols)
    )


def _rename_industry_cols(emp: pd.DataFrame) -> pd.DataFrame:
    mapper = {
        'CVM_IN': 'Industry',
        'CVM_RE': 'Retail',
        'CVM_SV': 'Service',
        'CVM_TH': 'Transport',
        'CVM_WH': 'Wholesale',
        'CVM_GO': 'Government\\Office',
    }
    return emp.rename(columns=mapper)


def _melt_industry_cols(emp: pd.DataFrame) -> pd.DataFrame:
    return emp.melt(id_vars='TAZ', var_name='industry', value_name='emp')


def _aggregate_industry_cols(emp: pd.DataFrame) -> pd.DataFrame:
    return (
        emp
        .set_index('TAZ')
        .assign(
            industry=lambda df: df.industry.astype(
                pd.CategoricalDtype(
                    categories=[
                        'Industry',
                        'Wholesale',
                        'Retail',
                        'Government\\Office',
                        'Service',
                        'Transport',
                        'Fleet Allocator',
                    ]
                )
            )
        )
        .groupby('industry')
        .sum()
        .assign(emp=lambda df: df.emp.astype('int64'))
    )


def extract_trip_data(path: str | Path) -> pd.DataFrame:
    return (
        pd.read_csv(
            path,
            usecols=[
                'tripID',
                'tourID',
                'stopID',
                'distanceTotal',
                'weightTrip',
                'weightPersonTrip',
            ]
        )
        .pipe(_rename_trip_cols)
        .set_index('trip_id')
    )


def _rename_trip_cols(trips: pd.DataFrame) -> pd.DataFrame:
    mapper = {
        'tripID': 'trip_id',
        'tourID': 'tour_id',
        'stopID': 'stop_id',
        'distanceTotal': 'distance',
        'weightTrip': 'weight_trip',
        'weightPersonTrip': 'weight_person',
    }
    return trips.rename(columns=mapper)


def extract_tour_data(path: str | Path) -> pd.DataFrame:
    return (
        pd.read_csv(
            path,
            usecols=[
                'tourID',
                'actorType',
                'tourMode',
            ]
        )
        .pipe(_rename_tour_cols)
        .pipe(_categorize_tour)
        .set_index('tour_id')
    )


def _rename_tour_cols(tours: pd.DataFrame) -> pd.DataFrame:
    mapper = {
        'tourID': 'tour_id',
        'actorType': 'industry',
        'tourMode': 'mode',
    }
    return tours.rename(columns=mapper)


def _categorize_tour(tours: pd.DataFrame) -> pd.DataFrame:
    return (
        tours
        .assign(
            industry=lambda df: df.industry.astype(
                pd.CategoricalDtype(
                    categories=[
                        'Industry',
                        'Wholesale',
                        'Retail',
                        'Government\\Office',
                        'Service',
                        'Transport',
                        'Fleet Allocator',
                    ]
                )
            )
        )
    )
