from flask import Flask, jsonify, request
import pytz
from datetime import datetime
import os

app = Flask(__name__)

# Dictionary to store registered time zones and their names
registered_timezones = {
    'utc': 'UTC',
    'us/central': 'US/Central',
    'europe/london': 'Europe/London',
    # Add more time zones as needed
}


@app.route('/current_time', methods=['GET'])
def get_current_time():
    try:
        # Get the requested time zone from the query parameter
        timezone_param = request.args.get('timezone')

        if not timezone_param:
            return jsonify({'error': 'Missing timezone query parameter'}), 400

        # Check if the requested time zone is registered
        if timezone_param not in registered_timezones:
            return jsonify({'error': 'Invalid timezone'}), 400

        # Get the current time in the requested time zone
        current_time = datetime.now(pytz.timezone(timezone_param)).strftime('%Y-%m-%d %H:%M:%S')

        # Prepare the response JSON object
        response_data = {
            'timezone': registered_timezones[timezone_param],
            'current_time': current_time
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=True)
