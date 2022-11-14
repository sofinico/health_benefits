import pandas as pd


def blankspace(n=1):
    for _ in range(n):
        print('\n')


def check(statement: bool, message=''):
    error_message = 'Check not accomplished.' if message == '' else message

    if not statement:
        raise AssertionError(error_message)


def entries(df: pd.DataFrame) -> int:
    return df.shape[0]
