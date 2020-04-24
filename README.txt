# Reducing Global CO2 Emissions through Freight Traffic Analytics

### Description

CO2 emissions have been on the rise in the previous decades and pose a severe threat to the environment if no action is taken. One top source of CO2 emission is from maritime freight traffic which requires the delivery of cargo on many different kinds of ships. This package leverages available AIS ship movement data and analytics to demonstrate ways to reduce CO2 emission by aggregating ships at optimal ports. 

Upon running and installing the package, the user will be presented with an interactive dashboard that demonstrates how individuals can leverage a hub-and-spoke model on AIS data which tracks the movement of ships, in order to reduce CO2 emissions. The visualizations include maps of routes, CO2 optimization vs clustering line charts, and multi-dimensional scatterplots. The dashboard comes equipped with controls that shows the many dimensions of the analysis where a user can filter by model cluster size, vessel type, and hub. 

The package is built on top of the open-source Dash platform to build an interactive dashboard to visualize the findings of the team's analysis. Dash is built on-top of the flask web-server backend which is leveraged to query the the results of our analysis and render it dynamically on the dashboard. There was an emphasis on software design for this package so that future users are able to extend the project. The project is architected using the model-view-controller design pattern that many modern applications follow. The visualization, model, and application code are all separated.

For user convenience, we've also included the entire extract-transform-load (ETL) process which details how data is stored, queried, and transformed to build the models that are rendered in the user interface. The data was stored in an AWS instance of Postgres and queried in sql, and analysis was done via a Python Jupyter notebook deployed over AWS utilising sklearn, pandas and numpy.

### Installation

Please ensure your system has the following prerequisites installed:
```
Python 3.6+
```

Create a virtual environment with Python venv (`pip install virtualenv`) and activate the source by doing the following:

```
cd CODE
virtualenv venv

# For Windows
venv\Scripts\activate

# For OSX/Linux
source venv/bin/activate
```

Then install the python application dependencies:
```
pip install -r requirements.txt
```

### Execution

Finally, run the application:
```
python app.py
```

Then visit the live application at http://localhost:8050. For your convenience, we've also made the application available via heroku at https://team-nyc.herokuapp.com/. 

### Demo Video

A demo video of the application can be seen here:
https://www.youtube.com/watch?v=8wcOvY0vawQ
