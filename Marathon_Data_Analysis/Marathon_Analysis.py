"""
Haoyuan Deng
DS2500
HW2
Feb 10 2024
"""

import csv
import matplotlib.pyplot as plt
import statistics
import os

def read_csv(filename):
    ''' 
    given the name of a csv file, return its contents as a 2d list,
    including the header.
    '''
    data = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for row in csvfile:
            data.append(row)
    return data

def lst_to_dct(lst):
    ''' 
    given a 2d list, create and return a dictionary.
    keys of the dictionary come from the header (first row)
    , values are corresponding columns, saved as lists
    Ex: [[1, 2, 3], [x, y, z], [a, b, c]]
    should return {1 : [x, a], 2 : [y, b], 3 : [z, c]}
    '''
    dct = {h : [] for h in lst[0]}
    for row in lst[1:]:
        for i in range(len(row)):
            dct[lst[0][i]].append(row[i])
    return dct

def median(orig_lst):
    ''' 
    given a list of numbers, compute and return median 
    '''
    lst = orig_lst.copy()
    lst.sort()
    mid = len(lst) // 2
    if len(lst) % 2 == 1:
        return lst[mid]
    else:
        avg = (lst[mid] + lst[mid - 1]) / 2
        return avg
    
def get_filenames(dirname, ext = ".csv"):
    ''' 
    given the name of a directory (string), return a list
    of paths to all the  ****.ext files in that directory
    '''
    filenames = []
    files = os.listdir(dirname) 
    for file in files:
        if file.endswith(ext):
            filenames.append(dirname + "/" + file)
    return filenames

def clean_numeric(s):
    ''' 
    given a string with extra characters $ or , or %, remove them
    and return the value as a float
    '''
    s = s.replace("$", "")
    s = s.replace("%", "")
    s = s.replace(",", "")
    return float(s)
    
def clean_data(dct):
    ''' 
    given a dictionary that includes currency and
    numbers in the form x,xxx, clean them up and convert
    to int/float
    '''
    for key, value in dct.items():
        for i in range(len(value)):
            if not value[i].replace(" ", "").isalpha():
                value[i] = clean_numeric(value[i])
                        
def choose_file(directory, year):
    '''
    Extract the file that aligns with the given year
    Parameters: directory, year (number)
    Returns: stringc (one of the filenames within the directory)
    '''
    for file in get_filenames(directory):
        if str(year) in file:
            return file

def clean_marathon_data(lst):
    '''
    Parameters: lst (list of filenames)
    Returns: a simplied dictionary of each marathon file data
    '''
    all_dct = {}
    for file in lst:
        data = read_csv(file)
        dct = lst_to_dct(data)
        all_dct = {**all_dct, **dct}
    return all_dct

def dir_dct(filename):
    '''
    Turns the 2d list of data into dictionary where the keys are the first 
    row in the 2d list and the rest of the rows are value vertically.
    Parameters: filename (string)
    Returns: Dictonary
    '''
    return lst_to_dct(read_csv(filename))

def file_sorted_dct(all_files):
    '''
    Arrange the given directory in the ascending year order
    Parameter: all_files (list of filnames)
    Return: dictionary 
    '''
    newdct = {}
    sorted_dct = {}
    for file in all_files:
        for p in range(len(file)):
            # if the [p:P + 4] range are numbers(the year), extract them and 
            # set them as the key of the dictionary
            if (file[p:p + 4]).isdigit():
                newdct[(file[p:p + 4])] = file
    # use the rearrange year key and create the arranged list of the value
    for i in sorted(newdct):
        sorted_dct[i] = newdct[i]
    return sorted_dct

def mean_finish(files, year):
    '''
    Given the data find the mean finish time of the give year file
    Parameter: files(file_lst), year (number)
    Return: time (HH:MM:SS)
    
    '''
    time_lst = []
    seconds_lst = []
    # extract the OfficialTime column data
    for i in dir_dct(file_sorted_dct(files)[str(year)])['OfficialTime']:
    # turn to a 2d list where each row is in the [HH, MM, SS] form of the time
        time_lst.append(i.split(':'))
    # turn all the string number to number
    for row in time_lst:
        hours, minutes, seconds = map(int, row)  
        total_seconds = hours * 3600 + minutes * 60 + seconds
        seconds_lst.append(total_seconds)
    seconds = round(statistics.mean(seconds_lst))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return str(hours) + ':' + str(minutes) + ':' + str(remaining_seconds)
    
def median_age(files, year):
    '''
    Given the data find the median of the age data
    Parameter: files(file_lst), year (number)
    Return: float
    
    '''
    new_age_lst =[]
    for i in dir_dct(file_sorted_dct(files)[str(year)])['AgeOnRaceDay']:
        new_age_lst.append(float(i))
    return statistics.median(new_age_lst)

def most_runner_country(files, year):
    '''
    Given the data corresponding to the given year, find the second most 
    runner country
    Parameter: files(file_lst), year (number)
    Return: string
    
    '''
    new_country_lst =[]
    for i in dir_dct(file_sorted_dct(files)[str(year)])['CountryOfResAbbrev']:
        if i != "USA":
            new_country_lst.append(i)
    return statistics.mode(new_country_lst)

def total_woman_finished(files, year):
    '''
    Given the data corresponding to the given year, calculate the total number
    of woman finished in the top 1000
    Parameter: files(file_lst), year (number)
    Return: float
    
    '''
    total_woman_lst =[]
    for i in dir_dct(file_sorted_dct(files)[str(year)])['Gender']:
        if i != "M":
            total_woman_lst.append(i)
    return len(total_woman_lst)

def woman_finish_time(filename):
    '''
    Given the filename, produce only the list of all womman's finish time 
    Parameter: filename (string)
    Return: list
    
    '''
    woman_finish_lst =[]
    for p in range(len(dir_dct(filename)['Gender'])):
        if dir_dct(filename)['Gender'][p] != "M":
            woman_finish_lst.append(dir_dct(filename)['OfficialTime'][p])
    return woman_finish_lst

def mean_lst(lst):
    '''
    Given the list of finish time, produce the mean 
    Parameter: filename (string)
    Return: float
     
    '''
    time_lst = []
    total_seconds_lst = []
    for i in lst:
    # turn to a 2d list where each row is in the [HH, MM, SS] form of the time
        time_lst.append(i.split(':'))
    # turn all the string number to number
    for row in time_lst:
        hours, minutes, seconds = map(int, row)  
        total_seconds = hours * 3600 + minutes * 60 + seconds
        total_seconds_lst.append(total_seconds)
    return sum(total_seconds_lst) / len(total_seconds_lst)   

def corr_woman_mean(files):
    '''
    Given the directory of the data file, calculate the correlation of year 
    vs. mean finish times for women
    Parameter: files (file_lst [all the data files])
    Return: float
    
    '''
    woman_finish_lst = []
    year_lst = []
    # goes through all the filenames in the file_sorted_dct
    for year,filename in file_sorted_dct(files).items():
        woman_finish_lst.append(mean_lst(woman_finish_time(filename)))
        year_lst.append(int(year))
    return round(statistics.correlation(woman_finish_lst, year_lst), 4)
                   
def usa_finish_lst(filename):
    '''
    Given the filename, produce only the list of all American runners finish 
    time 
    Parameter: filename (string)
    Return: list
    
    '''
    usa_finish_time_lst =[]
    for p in range(len(dir_dct(filename)['CountryOfResAbbrev'])):
        if dir_dct(filename)['CountryOfResAbbrev'][p] == "USA":
            usa_finish_time_lst.append(dir_dct(filename)['OfficialTime'][p])
    return usa_finish_time_lst

def corr_usa_mean(files):
    '''
    Given the directory of the data file, calculate the correlation of year 
    vs. mean finish times of American runners in the top 1000   
    Parameter: files (file_lst [all the data files])
    Return: float
    
    '''
    usa_lst = []
    year_lst = []
    for year,filename in file_sorted_dct(files).items():
        usa_lst.append(mean_lst(usa_finish_lst(filename)))
        year_lst.append(int(year))
    return round(statistics.correlation(usa_lst, year_lst), 4)

def mean_lst_dct(files):
    '''
    Given a list of files, product a dictionary where the keys are the years
    and the values are the corresponding mean finish time for USA
    Parameter: files (file_lst)
    Return: dictionary
    '''
    mean_usa_finish_dct = {}
    for year,filename in file_sorted_dct(files).items():
        mean_usa_finish_dct[year] = mean_lst(usa_finish_lst(filename))
    return mean_usa_finish_dct  
    
def predict_mean(dct):
    '''
    Given a dictionary of mean finish time from 2010 to 2023, predict the 
    finish time for 2020
    Parameters: dictionary (mean_dct)
    Returns: time (HH:MM:SS)
    '''
    year_lst = []
    mean_lst = []
    numerator_lst = [] 
    denominator_lst = [] 
    # turn the keys and the values from the given dictionary to two list
    for year, value in dct.items():
        year_lst.append(int(year))
        mean_lst.append(value)   
        
    mean_year = statistics.mean(year_lst)
    mean_finish = statistics.mean(mean_lst)
    
    # calculate the linear regression equation and predict the value
    for x, y in zip(year_lst, mean_lst):
        numerator_lst.append((x - mean_year) * (y - mean_finish))
        denominator_lst.append((x - mean_year) ** 2)
        
    slope = sum(numerator_lst) / sum(denominator_lst)
    intercept = mean_finish - slope * mean_year
    predicted_value_2020 = slope * 2020 + intercept
    hours = round(predicted_value_2020) // 3600
    minutes = (round(predicted_value_2020) % 3600) // 60
    remaining_seconds =  round(predicted_value_2020) % 60
    return f'{hours}:{minutes}:{remaining_seconds}'
    
def plt1(dct):
    '''
    Produce a linear regression modeling the relationship between year 
    and mean finish times of American runners in the top 1000
    Parameters: dictionary (mean_dct)
    Returns: plot
    '''
    years = []
    means = []
    numerator_lst = [] 
    denominator_lst = [] 
    regression_y = []
    # turn the keys and the values from the given dictionary to two list
    for year, value in dct.items():
        years.append(int(year))
        means.append(value)  
        
    mean_year = statistics.mean(years)
    mean_finish = statistics.mean(means)
    # calculate the linear regression line
    for x, y in zip(years, means):
        numerator_lst.append((x - mean_year) * (y - mean_finish))
        denominator_lst.append((x - mean_year) ** 2)
        
    slope = sum(numerator_lst) / sum(denominator_lst)
    intercept = mean_finish - slope * mean_year
    # find out the y-value for each year based on the regression line
    for i in years:
        regression_y.append(slope* i + intercept)
    # plot the data and the linear regression line
    plt.scatter(years, means, label='Actual data')
    plt.plot(years, regression_y, color='red', label='Linear regression')
    plt.xlabel('Year')
    plt.ylabel('Mean Finish Time (Seconds)')
    plt.title('Linear Regression Model of USA Mean Finish Times')      
    plt.legend()
    plt.grid(True)
    plt.show()          
             
def normalize(lst):
    '''
    Produce the normalized list of data
    Parameters: lst (list of numbers)
    Return: list
    '''
    norm_lst = []
    for i in lst:
        norm_lst.append((i - min(lst)) / (max(lst) - min(lst)))
    return norm_lst

def time_seconds(lst):
    '''
    Given the list of finish time in time format, change it to list of seconds
    Parameter: lst (list of time)
    Return: list
    '''
    time_lst = []
    total_seconds_lst = []
    # turn to a 2d list where each row is in the [HH, MM, SS] form of the time
    for i in lst:
        time_lst.append(i.split(':'))
    # turn all the string number to number
    for row in time_lst:
        hours, minutes, seconds = map(int, row)  
        total_seconds = hours * 3600 + minutes * 60 + seconds
        total_seconds_lst.append(total_seconds) 
    return  total_seconds_lst
    
def plot2(dct):  
    '''
    Produce the plot for median age and average finish times, over time.
    Parameters: dictionary (perfect_dct)
    Returns: plot
    '''
    years_lst = []
    sorted_file_lst = []
    median_age_lst = []
    finish_lst = []
    # the keys and values to two list
    for year, filename in dct.items():
        years_lst.append(year)
        sorted_file_lst.append(filename)
    # create list of median age and average finish time from the list of 
    # ordered data and normalize them into the corresponding y-axis variable
    for year in years_lst:
        median_age_lst.append(median_age(sorted_file_lst, year))
        finish_lst.append(mean_finish(sorted_file_lst, year))
        mean_seconds_lst = time_seconds(finish_lst)
    # y-axis for normalization list of media age for all years
    norm_median_y = normalize(median_age_lst)
    norm_mean_finish_y = normalize(mean_seconds_lst)
    # plot the median age and mean finish time over time with normalized data
    plt.plot(years_lst, norm_median_y, color='red', label='median age')
    plt.plot(years_lst, norm_mean_finish_y, color='blue', label='mean finish')
    plt.xlabel('Year')
    plt.ylabel('Mean Finish Time / Median age (Normalized)')
    plt.title('Median Age and Mean Finish Times Over Time. ')      
    plt.legend()
    plt.grid(True)
    plt.show()   
 

def main():
# Variables:
    DIRECTORY = "marathon_data"
    
    # List of filenames
    file_lst = get_filenames(DIRECTORY)
    
    # An orderd dictionary where keys are years and values are corresponding
    # filename
    perfect_dct = file_sorted_dct(file_lst)
    
    # Dictionary of mean finish time of USA runners for all years
    mean_dct = mean_lst_dct(file_lst) 
    
# Q1.1: What was the mean finish time of the top 1000 runners in 2013? 
    print(mean_finish(file_lst, 2013))
       
# Q1.2: What is the median age of the top 1000 runners in 2010?
    print(median_age(file_lst, 2010))
        
# Q1.3: Apart from the US, which country had the most runners in 2023? 
    print(most_runner_country(file_lst, 2023))
       
# Q1.4: How many women finished in the top 1000 in 2021?
    #print(total_woman_finished(file_lst, 2021))
   
# Q2.1: What is the correlation (r-value) of year vs. mean finish times for 
#       women?
    #print(corr_woman_mean(file_lst))

# Q2.2: What is the correlation (r-value) of year vs. the mean finish time of 
#       American runners in the top 1000? 
   # print(corr_usa_mean(file_lst))
    
# Q2.3: If the 2020 race had actually happened, what would you predict to be 
#       the mean finish time of Americans in the top 1000?
    #print(predict_mean(mean_dct))
    #
# Q3: Upload your first plot here: a linear regression modeling the 
#     relationship between year and mean finish times of American runners 
#     in the top 1000.
   # plt1(mean_dct)
    
# Q4: Upload your second plot here: median age and average finish times, 
#     over time.
    #plot2(perfect_dct)
    
main()











