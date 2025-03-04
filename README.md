# Flask Weather API

This Flask application serves as an API for retrieving climate data from an SQLite database containing weather observations in Hawaii.

## Installation

1. Clone the repository and navigate to the project folder.
2. Ensure that the `hawaii.sqlite` database is located inside the `Resources/` folder.

## Running the Application

To start the Flask app, run:
```bash
python app.py
```
This will start the development server on `http://127.0.0.1:5000/`.

## Available API Routes

### Home Page
`/`
- Lists all available API routes.

### Precipitation Data
`/api/v1.0/precipitation`
- Returns JSON data for precipitation records over the last 12 months.

### Weather Stations
`/api/v1.0/stations`
- Returns a JSON list of weather stations.

### Temperature Observations
`/api/v1.0/tobs`
- Returns temperature observations for the most active station over the last year.

### Temperature Statistics
#### Start Date Only
`/api/v1.0/<start>`
- Returns minimum, average, and maximum temperature from the given `start` date onwards.

#### Start and End Date
`/api/v1.0/<start>/<end>`
- Returns minimum, average, and maximum temperature for the date range between `start` and `end` (inclusive).

**Note:** Dates should be provided in `YYYY-MM-DD` format.

## Example Usage
### Fetching Temperature Stats from 2017-01-01 Onwards:
```
http://127.0.0.1:5000/api/v1.0/2017-01-01
```

### Fetching Temperature Stats Between 2017-01-01 and 2017-12-31:
```
http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-12-31
```

## References
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xmlLinks

