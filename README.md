
#  Stock API

This is a Flask-based RESTful API for managing and analyzing stock data. It supports:

- Creating, reading, updating, and deleting stock metadata
- Loading and storing historical price data from CSV files
- Analyzing the most profitable trading periods
- Calculating total achievable profit from multiple trades
- Dockerized environment for easy deployment

## Run with Docker

### Prerequisites

- Docker installed (Linux: `sudo apt install docker.io`)
- Docker Compose (optional, for easier local development)

### 1. Build Docker image

```bash
docker build -t stock-api .
```

### 2. Run the container

```bash
docker run -p 5000:5000 stock-api
```

### (Optional) Using docker-compose

```bash
docker-compose up --build
```

## Project Structure

* `app/`:
  * `__init__.py`
  * `routes.py`
  * `models.py`
  * `logic.py`
* `data/` - CSV files with historical prices
* `tests/`:
  * `test_logic.py` - Unit tests
* `loader.py` - Script to load CSV data into DB
* `app.py` - Entry point
* `Dockerfile`
* `docker-compose.yml`
* `requirements.txt`
* `README.md`


## API Endpoints

### 1. `POST /stocks`
Create a new stock entry.

```json
{
  "name": "Apple",
  "symbol": "AAPL",
  "founded": "1980-12-12"
}
```

### `GET /stocks`
Get all stock entries.

### 2. `GET /stocks/<symbol>`
Get a stock by its symbol.

### 3. `PUT /stocks/<symbol>`
Update stock details.

### 4. `DELETE /stocks/<symbol>`
Delete a stock.

### 5. `POST /stocks/profit`
Returns most profitable buy/sell dates and total profit for a stock. Additionally it returns company that are more profitable in that time period.

#### Request body:

```json
{
  "symbol": "AAPL",
  "start_date": "2020-06-01",
  "end_date": "2020-06-10"
}
```

#### Response:

```json
{
  "previous": {  },
  "selected": {  },
  "next": {  },
  "more_profitable_stocks": [ ]
}
```

## Postman Testing

1. Open [Postman](https://www.postman.com/)
2. Use URL: `http://localhost:5000`
3. Create a request for each endpoint (see above)
4. Use `raw JSON` body for `POST` and `PUT`

## Unit Testing

Run tests using:

```bash
PYTHONPATH=. pytest
```

Tests located in `tests/test_logic.py`.
