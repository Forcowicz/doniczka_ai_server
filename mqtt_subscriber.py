import os
from paho.mqtt import client as mqtt_client

from doniczka_ai_server.controllers import (
    EventLogEntryController,
    TelemetryController,
)
from doniczka_ai_server.database.postgres_client import PostgresClient
from doniczka_ai_server.initializers import initialize_controllers, initialize_database
from doniczka_ai_server.schemas.EventLogEntrySchemas import EventLogEntryCreate
from doniczka_ai_server.schemas.TelemetrySchemas import TelemetryCreate


def on_telemetry_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    try:
        telemetry_data = TelemetryCreate.model_validate_json(msg.payload.decode())
    except Exception as e:
        print(f"Failed to parse telemetry data: {e}")
        return

    # Controller
    controller = TelemetryController.get_instance()
    controller.store_telemetry(telemetry_data)
    print("Telemetry data stored successfully.")


def on_event_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    try:
        event_data = EventLogEntryCreate.model_validate_json(msg.payload.decode())
    except Exception as e:
        print(f"Failed to parse event log data: {e}")
        return

    # Controller
    controller = EventLogEntryController.get_instance()
    controller.store(event_data)
    print("Event log data stored successfully.")


def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
            subscribe("devices/1/telemetry", client, on_telemetry_message)
            subscribe("devices/1/events", client, on_event_message)
        else:
            print(f"Failed to connect, return code {reason_code}")

    client = mqtt_client.Client(
        client_id="remote_server",
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
        protocol=mqtt_client.MQTTv5,
    )

    client.on_connect = on_connect
    if os.environ["APP_ENV"] == "production":

        client.username_pw_set(
            os.environ["MQTT_USERNAME"],
            os.environ["MQTT_PASSWORD"],
        )
        client.connect(
            os.environ["MQTT_BROKER_HOST"],
            int(os.environ.get("MQTT_BROKER_PORT", "8883")),
        )
    else:
        client.connect(
            os.getenv("MQTT_BROKER_HOST"), int(os.getenv("MQTT_BROKER_PORT"))
        )
    return client


def subscribe(topic: str, client: mqtt_client.Client, callback=None):
    if callback is None:
        if topic == "devices/telemetry":
            callback = on_telemetry_message
        elif topic == "devices/1/events":
            callback = on_event_message

    client.subscribe(topic)
    if callback is not None:
        client.message_callback_add(topic, callback)


def run():
    postgres_client = PostgresClient.get_instance()

    initialize_database(postgres_client)
    initialize_controllers(postgres_client)

    client = connect_mqtt()
    client.loop_forever()


if __name__ == "__main__":
    run()
