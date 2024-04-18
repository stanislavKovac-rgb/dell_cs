from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS, cross_origin  # Import CORS library

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (not recommended for production)

# OR

# For specific origins (recommended for production)
ALLOWED_ORIGINS = '*'

DATABASE_URL="postgresql://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"

@app.route('/get_data', methods=['POST'])
@cross_origin()  # Allows CORS for all origins (adjust for specific origins in production)
def get_data():
    data = request.get_json()
    selected_table = data.get('table')

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Fixed query construction with selected_table:
        query = f"SELECT * FROM {selected_table} LIMIT 100"
        cursor.execute(query)

        rows = cursor.fetchall()

        response_data = []
        for row in rows:
            clean_row = {}
            for i, value in enumerate(row):
                clean_row[f'column_{i}'] = value  # Dynamic key based on index

            # Process nested data if needed (see explanation below)
            # ... (your nested data processing logic here) ...

            response_data.append(clean_row)

        cursor.close()
        conn.close()

        return jsonify(response_data)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)