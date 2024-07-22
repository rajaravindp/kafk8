from kafka import KafkaConsumer, KafkaProducer
import json
import pandas as pd

# Init Kafka consumer and producer
consumer = KafkaConsumer(
    'user-login',
    bootstrap_servers=['kafka-service:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['kafka-service:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def process_data(data):
    # Convert timestamp to human-readable format
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms').strftime('%Y-%m-%d %H:%M:%S')
    
    # Flag to indiciate data = processed
    data['processed'] = True

    # insights = {
    #     'total_users': data['user_id'].nunique(),
    #     'total_logins': data.shape[0],
    #     'avg_logins_per_hour': data['timestamp'].dt.hour.value_counts().mean(),
    # }

    # data['insights'] = insights

    return data

# Process data
for message in consumer:
    try:
        data = message.value
        # Execute Data Processing
        processed_data = process_data(data)
        
        # Send processed data to a new topic
        producer.send('processed-data', value=processed_data)
        
        # Print processed data. Print insights every 50 messages
        print(f"Processed data: {processed_data}")
        # if message.offset % 50 == 0:
        #     print(f"Insights: {processed_data['insights']}")
        
    except Exception as e:
        print(f"Error processing message: {e}")

# Close the Kafka consumer and producer
consumer.close()
producer.close()

