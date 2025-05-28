from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DATA_SECURITIES = os.getenv('DATA_SECURITIES', '').split('|')

def securities_information(requested_data, data_sec, key_prefix="securities"):
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    json_object = {}
    try:
        for index,data_entry in enumerate(data_sec):
            key = f"{key_prefix}_{index + 1}"
            product_parts = data_entry.split(" - ", 1)
            if len(product_parts) < 2:
                print(f"Warning: Skipping malformed data entry: {data_entry}")
                continue
            
            securities_name = product_parts[0].strip()
            when_issued = product_parts[1].strip()

            cleaning_requested_data = requested_data.strip()
            if cleaning_requested_data == key:
                json_object[key] = {
                    "requested_at" : current_time,
                    "securities" : securities_name, 
                    "issued_day": when_issued
                    }
                json_string = json.dumps(json_object, indent=4)
                return json_string
        return json.dumps({"error": "No matching security found"}, indent=4)
    except Exception as e:
        print (e)
        return json.dumps({"error": str(e)}, indent=4)
    
@app.route('/sear', methods=['GET'])
def get_securities_info():
    requested_data = request.args.get('id')
    if not requested_data:
        return jsonify({"error":"Please provide a 'id' query parameter, e.g., /sear?id=securities_1"}),400
    
    result = securities_information(requested_data, DATA_SECURITIES)

    return app.response_class(
        response=result,
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)
