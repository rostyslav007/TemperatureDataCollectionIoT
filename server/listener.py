import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the database connection string from the environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')


# Set up the database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/store', methods=['POST'])
def save_data():
    # Get data from the POST request
    data = request.get_json()

    print(data)

    if not data or 'temp' not in data:
        return jsonify({"error": "Invalid format of incoming request"}), 400

    temperature = float(data['temp'])

    # Save the data into PostgreSQL
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the table (make sure you have a table set up for this)
        cur.execute("INSERT INTO history (temp) VALUES (%s)", (temperature, ))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()

        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({"error": "Failed to save data"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Server is running!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
