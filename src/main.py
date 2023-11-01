from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import psycopg2


class Main:
    def __init__(self, host, token, tickets, t_max, t_min, database):
        """Initialize with environment variables and provided values."""
        self._hub_connection = None
        self.HOST = host
        self.TOKEN = token
        self.TICKETS = 3
        self.T_MAX = t_max
        self.T_MIN = t_min
        self.DATABASE = database

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS."""
        self.set_sensorhub()

    def start(self):
        """Start Oxygen CS."""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(
            lambda: print("||| Connection opened.", flush=True)
        )
        self._hub_connection.on_close(
            lambda: print("||| Connection closed.", flush=True)
        )
        self._hub_connection.on_error(
            lambda data: print(
                f"||| An exception was thrown closed: {data.error}", flush=True
            )
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature, date)
        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature, date):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
            self.send_event_to_database(date, "TurnOnAc", temperature)
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")
            self.send_event_to_database(date, "TurnOnHeater", temperature)
        else:
            self.send_event_to_database_temp(date, temperature)

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def send_event_to_database(self, timestamp, event, temperature):
        """Save sensor data into the database."""
        try:
            # Set up the PostgreSQL connection
            connection = psycopg2.connect(
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                database=self.DATABASE,
            )

            # save temp
            self.send_event_to_database_temp(timestamp, temperature)

            # Create a cursor
            cursor = connection.cursor()

            # Define the PostgreSQL INSERT statement
            postgres_insert_query = (
                "INSERT INTO sensor_data_event (timestamp, event) VALUES (%s, %s)"
            )

            # Insert data into the PostgreSQL table
            record_to_insert = (timestamp, event)
            cursor.execute(postgres_insert_query, record_to_insert)

            # Commit the changes to the database
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into sensor_data_event table")
        except requests.exceptions.RequestException as e:
            print(e, flush=True)
            pass
        except Exception as e:
            print(e, flush=True)
            pass

    def send_event_to_database_temp(self, timestamp, temperature):
        """Save sensor data into the database."""
        try:
            # Set up the PostgreSQL connection
            connection = psycopg2.connect(
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                database=self.DATABASE,
            )

            # Create a cursor
            cursor = connection.cursor()

            # Define the PostgreSQL INSERT statement
            postgres_insert_query = (
                "INSERT INTO sensor_data_temp (timestamp, temperature) VALUES (%s, %s)"
            )

            # Insert data into the PostgreSQL table
            record_to_insert = (timestamp, temperature)
            cursor.execute(postgres_insert_query, record_to_insert)

            # Commit the changes to the database
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into sensor_data table_temp")
        except Exception as e:
            print(e, flush=True)
            pass


if __name__ == "__main__":
    main = Main(
        host="https://hvac-simulator-a23-y2kpq.ondigitalocean.app",
        token="WeVCNw8DOZ",
        tickets=2,
        t_max=30,
        t_min=18,
        database="log680",
    )
    main.start()
