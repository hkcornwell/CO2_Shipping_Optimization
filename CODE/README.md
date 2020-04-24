# Reducing Global CO2 Emissions through Freight Traffic Analytics (Dash)

Team NYC's project is a dashboard that provides informative analytics on maritime traffic and CO2 emissions.

## Project Structure
The project loosely follows a model-view-controller structure with extra directories that show data ingestion and model creation. 

#### Notebooks (notebooks/)
Before any UI/UX or backend was created, analysis was conducted via jupyter notebooks. This analysis is available for viewing under the notebooks/ directory which shows all the necessary code for the ETL process. The ETL process entails querying the data from postgres, transforming the data and building the models, and lastly storing it in an application-digestable format.

#### Database (database/)
This directory contains our ingest process of the massive AIS dataset into postgres. Further documentation is available in the README in that directory.

#### Views (views/)
"Views" are plotly components that usually take a dataframe as an input and process them to store into a plotly figure. These plotly figures were originated from notebook analysis.

#### Model (model/)
The model is where data logic and ORM logic is stored to query the necessary data. This can be either through a pickle, json, or postgres connection. In this case, we queried our data structures from the data/ directory which are plain CSVs. This was done for user-convenience.

#### Data (data/)
This directory contains all the necessary model outputs and reference tables that the UI uses for continuous queries and re-rendering of the UI. Do not touch anything here.

#### Controller (app.py)
The controller would be the application logic that weaves together functions from the views and the models. Logic here should not be too complex, and anything that can be written as a function or something larger should be tossed into the util/ directory.

#### Utility (util/)
The utility directory contains miscellenous functions that are reused throughout the application and refactored out for our convenience.

#### Static Assets (assets/)
The assets directory is used by dash and contains static content such a CSS and javascript code. Most of the code here comes out-of-the-box with initial dash applications best practice and we've rewritten a bit of it to cater to our design choices.

## Installation & Running

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
virtualenv venv

# Windows
venv\Scripts\activate
# Or Linux
source venv/bin/activate
```

Clone the git repo, then install the requirements with pip
```
pip install -r requirements.txt
```

Run the app
```
python app.py
```

## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots
