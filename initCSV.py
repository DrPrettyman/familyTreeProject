import pandas as pd
import csv


def create_csv_files(people_csv_path, unions_csv_path):
    with open(people_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['full_name', 'date_of_birth', 'sex', 'code'])

    with open(unions_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['members', 'date_of_union', 'children', 'separation', 'code'])


def add_person(people_csv_path, full_name, dob, sex, code=''):
    if code == '':
        _names = full_name.split()
        code = _names[0] + _names[-1][0]
    with open(people_csv_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow([full_name, dob, sex, code])


def add_union(unions_csv_path, members, date_of_union, children, code, separation=0):
    with open(unions_csv_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow([members, date_of_union, children, separation, code])


def add_prettycrew(people_csv_path, unions_csv_path):
    # Add Unions:
    add_union(unions_csv_path, 'Joshua Amber', '2010-07-22', 'Ruben Atticus', 'JoshuaAndAmber')
    add_union(unions_csv_path, 'Elizabeth Graham', '1992', 'Joshua Amelia Samuel Alfie', 'G&E')
    add_union(unions_csv_path, 'Amelia Adrian', '', 'Talulah', 'AmeliaAndAdrian')
    add_union(unions_csv_path, 'Adrian', '', 'TaylorB', 'JustAdrian')
    add_union(unions_csv_path, 'Samuel HannahSmith', '', '', 'SamuelAndHannah')

    # Add details:
    add_person(people_csv_path, 'Ruben Arthur Prettyman', '2012-12-19', 'm', 'Ruben')
    add_person(people_csv_path, 'Atticus Pablo Prettyman', '2015-09-19', 'm', 'Atticus')
    add_person(people_csv_path, 'Joshua John Prettyman', '1990-10-03', 'm', 'Joshua')
    add_person(people_csv_path, 'Amber Isis Prettyman', '1990-11-23', 'f', 'Amber')
    add_person(people_csv_path, 'Graham John Prettyman', '1962-07-04', 'm', 'Graham')
    add_person(people_csv_path, 'Elizabeth Anne Prettyman', '1969-08-24', 'f', 'Elizabeth')
    add_person(people_csv_path, 'Amelia Rose Prettyman', '1993-07-08', 'f', 'Amelia')
    add_person(people_csv_path, 'Adrian Bryn', '1988-07-10', 'm', 'Adrian')
    add_person(people_csv_path, 'Talulah Celia Bryn', '2018-11-11', 'f', 'Talulah')
    add_person(people_csv_path, 'Taylor Bryn', '', 'm', 'TaylorB')
    add_person(people_csv_path, 'Samuel Thomas Prettyman', '1994-11-01', 'm', 'Samuel')
    add_person(people_csv_path, 'Hannah Smith', '', 'f', 'HannahSmith')
    add_person(people_csv_path, 'Alfie Bartholemew Prettyman', '1997-10-25', 'm', 'Alfie')


def read_csv_files(people_csv_path, unions_csv_path):
    """
    Reads csv files to pandas dataframes
    :return:

    """
    people_df = pd.read_csv(people_csv_path, delimiter=';', index_col='code', parse_dates=['date_of_birth'])
    unions_df = pd.read_csv(unions_csv_path, delimiter=';', index_col=False, parse_dates=['date_of_union'])
    unions_df['children'] = unions_df['children'].apply(lambda names: names.split(' ') if type(names) == str else [])
    unions_df['members'] = unions_df['members'].apply(lambda names: names.split(' ') if type(names) == str else [])
    return people_df, unions_df


def init_prettycrew():
    people_csv_path_prettycrew = 'ft_people.csv'
    unions_csv_path_prettycrew = 'ft_unions.csv'

    print('Writing empty csv files @ '
          '\n\t - {} '
          '\n\t - {}'.format(people_csv_path_prettycrew, unions_csv_path_prettycrew))
    create_csv_files(people_csv_path_prettycrew, unions_csv_path_prettycrew)

    print('Adding Prettycrew data to files...')
    add_prettycrew(people_csv_path_prettycrew, unions_csv_path_prettycrew)

    print('Reading csv files to pandas DataFrames...')
    people_df, unions_df = read_csv_files(people_csv_path_prettycrew, unions_csv_path_prettycrew)

    print('Printing DataFrames...')
    print('\nPeople:')
    print(people_df)
    print('\nUnions:')
    print(unions_df)
    print('Joshua DOB: ', people_df.date_of_birth['Joshua'])


if __name__ == '__main__':
    init_prettycrew()
