#Coursework Computational Artefact // Data analytics and visualisation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

dataIn = pd.read_csv('cleanedDF.csv')

#Function 1: 
#--------------------------------------------------------------------------------------
#A full dictionary of temperature sorted by Country {'Ireland': [12,13,14], 'United Kingdom': [10,12,13].....}

def function1():
    #Ask user to input countries and years
    listOfCountry = [] #Store the list of countries the user asked for
    while True:
        countryInput = input('Enter the countr(ies) to analyze (0 to exit): ')
        if countryInput == '0':
            break
        listOfCountry.append(countryInput)
    yearRangeFrom = int(input('Enter the year range (from)')) #Ask for a range of year
    yearRangeTo = int(input('Enter the year range (to)'))
    listOfYears = []   #Store the list of years the user asked for                                      
    for year in range(yearRangeFrom, yearRangeTo + 1):
        listOfYears.append(year)
    
    countryMean = {}                                                  #Universal set for storing data
    for country in listOfCountry:                                     #Go through each country
        countryData = dataIn[dataIn['Country'].isin([country])]       #Filter data for the current country
        countryTemps = []
        for year in listOfYears:                                                        #Go through each year within the selected country
            yearData = countryData[pd.to_datetime(countryData['dt']).dt.year == year]   #Only loc selected year within the selected country
            aver = yearData['AverageTemperature'].mean()                                #Average and round the 12 temperatures
            countryTemps.append(round(aver, 2))
        countryMean[country] = countryTemps                                    #Add all country data to Universal set countryMean = {}
    
    plt.figure(figsize=(12, 6))

    for country, temperatures in countryMean.items():
        plt.plot(listOfYears, temperatures, marker='o', linestyle='-', label=country)

    # Graph formatting
    plt.title('Annual Mean Temperature Trends by Country')
    plt.xlabel('Year')
    plt.ylabel('Mean Annual Temperature (°C)')
    plt.legend(title="Countries", loc='upper left')
    plt.grid(True)  # Add grid for better readability
    plt.xticks(listOfYears)  
    min_temp = min([min(temps) for temps in countryMean.values()]) - 1  # Find lowest temperature and subtract 1
    max_temp = max([max(temps) for temps in countryMean.values()]) + 2  # Find highest temperature and add 2
    plt.yticks(range(int(min_temp), int(max_temp), 2))
    # Show the plot
    plt.show()
    

#Function 2 Annual temperature cycle
#---------------------------------------------------------------------------------------
#Display the mean yearly temperature of chosen countries in a year range

def function2(): #Store the list of country the user asked for
    country = input('Enter the countr(ies) to analyze (0 to exit): ')
    year = int(input('Enter the year'))                                               
    dataIn['dt'] = pd.to_datetime(dataIn['dt'])                                 #Making sure data is in datetime format
    countryData = dataIn[dataIn['Country'] == country]                          #Filter data for the current country
    yearData = countryData[pd.to_datetime(countryData['dt']).dt.year == year]   #Filter data for the current year within current country                                   

    monthlyData = yearData.groupby(yearData['dt'].dt.month)['AverageTemperature'].mean()  #Calculae the mean temperature              
    monthlyData = monthlyData.reindex(range(1,13))                                        #Each value 1-12 corresponds to each month
    monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    plt.bar(monthList, monthlyData)
    plt.xlabel('Months')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Monthly Mean Temperature in {country} in {year}')
    plt.grid(True, linestyle='--')
    plt.show()

#Function 3 Fluctuations in mean temperature
#---------------------------------------------------------------------------------------
#Shows the range between the min and max mean temperature of countr(ies) in a year range
def function3():
    listOfCountry = []
    while True:
        countryInput = input('Enter the countr(ies) to analyze (0 to exit): ')
        if countryInput == '0':
            break
        listOfCountry.append(countryInput)
    yearRangeFrom = int(input('Enter the year range (from)'))
    yearRangeTo = int(input('Enter the year range (to)'))
    countryTempsRange = []          #Universal list
    explodeList = []                #A list of 0 or 0.08 representing whether data on pie chart explode or not
    diffList = []                   #List of differences 

    for country in listOfCountry:                                                               #Go through each country
        countryData = dataIn[dataIn['Country'].isin([country])]                                 #Filter data for the current country
        yearDataFrom = countryData[pd.to_datetime(countryData['dt']).dt.year == yearRangeFrom]  #Only loc the selected data equals to yearFrom within current country
        avgTempFrom = yearDataFrom['AverageTemperature'].mean()                                 #Find the mean
        yearDataTo = countryData[pd.to_datetime(countryData['dt']).dt.year == yearRangeTo]      #Only loc the selected data equals to yearTo within current country
        avgTempTo = yearDataTo['AverageTemperature'].mean()                                     #Find the mean
        diff = round((avgTempTo - avgTempFrom),3)                                               #Find the difference
        diffList.append(diff)                #Add to the list of differences
        if diff < 0:                         #If negative, explode, If not, don't explode
            explodeList.append(0.08)
            diff *= -1
        else:
            explodeList.append(0)
        countryTempsRange.append(diff)       #Data appended and ready for visualising
    print(countryTempsRange)
    print(diffList)

    newListOfCountry = []   #Combining listOfCountry and diffList together e.g. ['Ireland', 'United Kingdom'] and [0.025, -0.028] becomes ['Ireland 0.025', 'United Kingdom -0.028']
    counter = 0
    for cou in listOfCountry:
        newListOfCountry.append(f'{cou} {diffList[counter]}')
        counter += 1

    explodeTup = tuple(explodeList)       #For explode values, Matplotlib only takes set data type
    plt.title(f'Difference of Yearly Mean Temperature {yearRangeFrom} to {yearRangeTo}')
    plt.pie(countryTempsRange, labels=newListOfCountry, autopct='%1.1f%%', explode=explodeTup, shadow=True, startangle=90, labeldistance=.9, pctdistance=0.5)
    plt.text(1.2, 0, 'Exploded means negative values', fontsize=8, verticalalignment='center', bbox=dict(facecolor='lightgray', alpha=0.5))
    plt.tight_layout()
    plt.show()

#Function 4 Show list of available countries
#---------------------------------------------------------------------------------------
def function4():
    print(f"Here is a list of all available countries: \n{dataIn['Country'].unique()}")

print('Welcome, this program has 4 functions')
print('Function 1 (Line graph): Find out the monthly mean temperatures of a certain country within a certain year')
print('Function 2 (Bar chart): Find out the yearly mean temperatures of multiple countries within a year range')
print('Function 3 (Pie chart): Find out the the percentage of change of yearly mean temperature of 2 selected years compared to multiple countries')
print('Function 4: Print a list of country available in this dataset')
while True:
    try:
        command = int(input('Please type 1, 2, 3, or 4 for Function 1, 2, 3 or 4: '))
        if command == 1:
            function1()
        elif command == 2:
            function2()
        elif command == 3:
            function3()
        elif command == 4:
            function4()
        else:
            print('Error: Please type in a number between 1-4 inclusive')
    except ValueError:
        print('Error: Please type in a numeric value between 1-4 inclusive')


#Function 5 Recommendation
'''def function5():
    listOfCountry = []
    while True:
        countryInput = input('Enter the countr(ies) to analyze (0 to exit): ')
        if countryInput == '0':
            break
        listOfCountry.append(countryInput)
    yearRangeFrom = int(input('Enter the year range (from)'))
    yearRangeTo = int(input('Enter the year range (to)'))
    countryTempsRange = []          #Universal list'''
#A