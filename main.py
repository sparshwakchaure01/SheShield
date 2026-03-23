import requests
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure logging
the logging.basicConfig(level=logging.INFO)

# Replace with your actual ORS API Key
ORS_API_KEY = "YOUR_ORS_API_KEY"

# Color mapping based on risk
COLOR_MAPPING = {
    'low': 'green',
    'medium': 'yellow',
    'high': 'red'
}

@app.route('/api/routes', methods=['GET'])
def get_routes():
    try:
        # Extract parameters from request
        start_point = request.args.get('start')
        end_point = request.args.get('end')

        # Try ORS first
        ors_response = requests.get(f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_API_KEY}&start={start_point}&end={end_point}')
        ors_response.raise_for_status()

        # Process ORS response
        routes = ors_response.json()['routes']
        return jsonify(routes)

    except requests.exceptions.RequestException as e:
        logging.error(f'Error calling ORS API: {e}')
        return jsonify({'error': 'ORS API call failed'}), 500

    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)