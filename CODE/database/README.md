# Postgres Database

The Postgres instance is setup using AWS Free Tier (https://aws.amazon.com/rds/?did=ft_card&trk=ft_card). The ais table is created directly using pgAdmin and the schema is available in tableShema.sql.

The dataset is downloaded from https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2017/index.html. We downloaded AIS data for every zone for all of December and unzipped the data and put it in the data directory. We run ingest_data.ipynb to remove the "T" in the BaseDateTime column and insert a Zone column into the dataset. This is performed so that the "BaseDateTime" column has the data type "timestamp without time zone" and we can easily filter by zones, because the original dataset doesn't have a zone column. The final dataset is outputted into the output directory. Afterwards, the data is directly uploaded to the ais table using pgAdmin.

### Prerequisites

The prerequisites below can all be easily installed using the https://docs.anaconda.com/anaconda/install/ suite.

```
Python 3.7 +
Pandas 1.0.3 +
Jupyter Notebook
```

Otherwise, Python can be installed using https://www.python.org/downloads/release/python-382/. Afterwards the below commands can be used to install the necessary libraries.

```
pip install pandas
pip install jupyter
```