"""
Haoyuan Deng
DS 3500
HW 1
31 January 2025

"""

import pandas as pd
import sankey as sk

def main():
    #1. Convert the data into a Panda’s dataframe containing three columns: nationality, gender,
    #and the decade the ar?st was born. For example, if they were born between 1940 and
    #1949, you need only store the decade as 1940. Make sure the decade is stored as a float
    #or int, not a string!

    # Load the Artists DataFrame
    artists_df = pd.read_json('artists.json')

    # Create new_artists_df with only three column: 'Nationality', 'Gender', 'Decade'
    new_artists_df = artists_df[['Nationality', 'Gender', 'BeginDate']].copy()
    new_artists_df['Decade'] = (new_artists_df['BeginDate'] // 10) * 10
    new_artists_df = new_artists_df.drop(columns=['BeginDate'])

    # Making sure the decade column values are integer
    new_artists_df['Decade'] = new_artists_df['Decade'].astype('int64')

    # Change lowercase "male" strings to uppercase "Male"
    new_artists_df = new_artists_df.replace({"male": "Male"})

    # 2. Filter any rows where the decade is 0 (presumably unknown) or where there is missing
    #data.

    # Drop the rows with missing data and the Decade value equal to 0
    cleaned_df = new_artists_df.dropna()
    cleaned_df = cleaned_df[cleaned_df['Decade'] != 0]

    # 3. Aggregate the data, counting the number of ar?sts grouped by the combination of
    # nationality, decade, and gender.
    n_d = cleaned_df.groupby(["Nationality", "Decade"]).size().reset_index(name="Artist_Counts")
    n_g = cleaned_df.groupby(["Nationality", "Gender"]).size().reset_index(name="Artist_Counts")
    g_d = cleaned_df.groupby(["Gender", "Decade"]).size().reset_index(name="Artist_Counts")
    cleaned_df = cleaned_df.groupby(["Nationality", "Decade", "Gender"]).size().reset_index(name="Artist_Counts")

    # 4. Filter out rows (Nationality, Gender, Decade combination) whose artist count is below
    # some threshold. You’ll want to experiment with this value to produce a visually
    # appealing visualization. I suggest trying a staring threshold around 20.

    # Filter the DataFrame to keep only rows where the artist count is greater than or equal to the threshold
    n_d = n_d[n_d['Artist_Counts'] >= 60]
    n_g = n_g[n_g['Artist_Counts'] >= 40]
    g_d = g_d[g_d['Artist_Counts'] >= 20]

    # Sankey Visualizations
    # sk.make_sankey(n_d, 'Nationality', 'Decade')
    # sk.make_sankey(n_g, 'Nationality', 'Gender')
    # sk.make_sankey(g_d, 'Gender', 'Decade')

    # 5. Extend the Sankey functionality we developed in class to take an arbitrary list of columns
    # instead of just two specific source/target column parameters.
    sk.make_sankey(cleaned_df, 'Nationality', 'Gender', 'Decade')

if __name__ == "__main__":

    main()
