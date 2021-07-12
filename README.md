# sqlalchemy-challenge

## Climate Analysis and Exploration

This exercise includes using Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis

* The analysis was started by finding the most recent date in the data set.
* Using this date, the last 12 months of precipitation data was retrieved by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.
* Only the date and prcp values were selected.
* The query results were loaded into a Pandas DataFrame and the index was set to the date column.
* The DataFrame values were sorted by date.
* The results were plotted using the DataFrame plot method.
![](Images/Precipation.png)

### Station Analysis
![](Images/Temperatures.png)


## Climate App
![](Images/Flask_App.png)
