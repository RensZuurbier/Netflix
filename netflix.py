import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Adjust datafram show settings to see all tables
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

#Get dataframe
df = pd.read_csv('netflix_data/CONTENT_INTERACTION/ViewingActivity.csv')


###################### CLEAN THE DATA ######################
# Clean up some columns
skip_columns = ['Attributes', 'Bookmark', 'Latest Bookmark', 'Supplemental Video Type']
cleaned_df = df.drop(columns=skip_columns)

# Convert Start time to DateTime object
cleaned_df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)

# Update timezone from UTC to Local
# change the Start Time column into the dataframe's index
cleaned_df = cleaned_df.set_index('Start Time')
cleaned_df.index = cleaned_df.index.tz_convert('Europe/Amsterdam')
cleaned_df = cleaned_df.reset_index()

# Update Duration from object to time
cleaned_df['Duration'] = pd.to_timedelta(cleaned_df['Duration'])

# Remove all Titles which contains "Trailer" && remove all duration < 02:00
cleaned_df = cleaned_df[~cleaned_df['Title'].str.contains('Trailer', case=False)]
cleaned_df = cleaned_df[cleaned_df['Duration'] > '0 Days 00:02:00']

# Add columns 'Year', 'Month', 'Weekday' and 'Hour'  to Dataframe
cleaned_df['Year'] = cleaned_df['Start Time'].dt.year
cleaned_df['Month'] = cleaned_df['Start Time'].dt.month
cleaned_df['Weekday'] = cleaned_df['Start Time'].dt.weekday
cleaned_df['Hour'] = cleaned_df['Start Time'].dt.hour

# Clean up "Season" / Episodes names and stuff like that
cleaned_df['Title'] = cleaned_df['Title'].str.split(':').str[0]

# Export cleaned_df to .csv for PowerBi
cleaned_df.to_csv('cleaned_netflix.csv', index=False)
###################### CLEAN THE DATA ######################

exit()

##### Get Data of specific Profile Name #####
def df_profile(df, profile_name):
    return df[df['Profile Name'] == profile_name]
################################################################

# Get separate dataframe for Bono and Rentah
df_dinho = df_profile(cleaned_df, 'Bono')
df_rentah = df_profile(cleaned_df, 'Rentah')


##### Function get filtered data of specific TV-show (String) #####
def df_tvshow(df, tvshow_name):
    # Clean up the Titles / Season nrs. and episode names and stuff
    # df = df.copy()
    # df['Title'] = df['Title'].str.split(':').str[0]
    return df[df['Title'].str.contains(tvshow_name, case=False)]
################################################################

rentah_suits = df_tvshow(df_rentah, 'Suits')
bono_suits = df_tvshow(df_dinho, 'Suits')




#### --------> Plot by Weekday <-------- ####
def plot_days(df, title):
    df.plot(kind='bar')
    plt.xlabel('Day')
    plt.ylabel('Count')
    plt.title(title)
    plt.show()
############################################

rentah_days = df_rentah['Weekday'].value_counts().sort_index()
dinho_days = df_dinho['Weekday'].value_counts().sort_index()

plot_days(rentah_days, "Days watching Rentah")
plot_days(dinho_days, "Days watching Dinho")


#### --------> Plot by Hour <-------- ####
def plot_hours(df, title):
    df.plot(kind='bar')
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.title(title)
    plt.show()
############################################

rentah_hours = df_rentah['Hour'].value_counts().sort_index()
dinho_hours = df_dinho['Hour'].value_counts().sort_index()

plot_hours(rentah_hours, "Hours watching Rentah")
plot_hours(dinho_hours, "Hours watching Dinho")



#### --------> Plot by Month <-------- ####
def plot_months(df, title):
    df.plot(kind='bar')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title(title)
    plt.show()
############################################

rentah_months = df_rentah['Month'].value_counts().sort_index()
dinho_months = df_dinho['Month'].value_counts().sort_index()

plot_months(rentah_months, "Netflix by Month Rentah")
plot_months(dinho_months, "Netflix by Month Dinho")


#### ---->> Get top X of Watched Titles per Year <<---- ####
#1 Filter based on given year
#2 Get the totals of duration per Title
#3 Generate a top X ranking of Titles watched that year
def top_duration_year(df, year, rank):
    df = df[df['Year'] == year] #1
    duration_per_title = df.groupby('Title')['Duration'].sum() #2
    return duration_per_title.nlargest(rank).sort_values(ascending=True) #3


top_3_2024 = top_duration_year(df_rentah, 2024, 3)
top_3_2023 = top_duration_year(df_rentah, 2023, 3)
top_3_2022 = top_duration_year(df_rentah, 2022, 3)
top_3_2021 = top_duration_year(df_rentah, 2021, 3)

top_3_2024_dinho = top_duration_year(df_dinho, 2024, 3)
top_3_2023_dinho = top_duration_year(df_dinho, 2023, 3)
top_3_2022_dinho = top_duration_year(df_dinho, 2022, 3)
top_3_2021_dinho = top_duration_year(df_dinho, 2021, 3)

## Plot top titles function ##
def plot_top_titles(df, title):
    df.plot(kind='bar', figsize=(12, 12))
    plt.xlabel('Title')
    plt.ylabel('Duration')
    plt.title(title)
    plt.show()

plot_top_titles(top_3_2024, 'Top 3 2024 Rentah')
plot_top_titles(top_3_2023, 'Top 3 2023 Rentah')
plot_top_titles(top_3_2022, 'Top 3 2022 Rentah')
plot_top_titles(top_3_2021, 'Top 3 2021 Rentah')

plot_top_titles(top_3_2024_dinho, 'Top 3 2024 Dinho')
plot_top_titles(top_3_2023_dinho, 'Top 3 2023 Dinho')
plot_top_titles(top_3_2022_dinho, 'Top 3 2022 Dinho')
plot_top_titles(top_3_2021_dinho, 'Top 3 2021 Dinho')


unique_devices_rentah = df_rentah['Device Type'].unique()

# for i in unique_devices_rentah:
#     print(i)

unique_devices_dinho = df_dinho['Device Type'].unique()

# for i in unique_devices_dinho:
#     print(i)

unique_titles = cleaned_df['Title'].unique()

# print('Dinho watched', len(df_dinho['Title'].unique()), 'unique titles, Fockking addict!!')
# print('Rentah watched', len(df_rentah['Title'].unique()), 'unique titles, Fockking addict!!')

unique_countries_rentah = df_rentah['Country'].unique()
unique_countries_dinho = df_dinho['Country'].unique()

# print('Contries Dinho')
# for i in unique_countries_dinho:
#     print(i)
#
# print('Countries Rentah')
# for i in unique_countries_rentah:
#     print(i)
