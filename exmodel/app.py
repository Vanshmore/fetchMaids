from flask import Flask, request, jsonify
from fetchMaid import match_maids
app = Flask(__name__)

@app.route('/match-maids/<customer_id>', methods=['POST'])
def match_maids_api(customer_id):
    service_id = request.json.get('serviceId')
    if not service_id:
        return jsonify({"error": "serviceId is required"}), 400

    try:
        matched_maids = match_maids(customer_id, service_id)  # Call your existing function
        return jsonify({"matchedMaids": matched_maids}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
