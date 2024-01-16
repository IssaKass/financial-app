from flask import Blueprint, jsonify, request

export_bp = Blueprint("export", __name__, url_prefix="/export")


@export_bp.route("/csv", methods=["POST"])
def generate_csv():
    try:
        # Get JSON data from the request
        json_data = request.get_json()

        # Validate if JSON data is present
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate if required fields are present in the JSON data
        if "data" not in json_data or not isinstance(json_data["data"], list):
            return (
                jsonify({"error": "Invalid JSON format. 'data' should be a list."}),
                400,
            )

        # Extract data from JSON data
        data = json_data["data"]

        # Create a CSV string from the JSON data
        csv_content = ""
        if data:
            csv_content += ",".join(data[0].keys()) + "\n"
            for row in data:
                csv_content += ",".join(map(str, row.values())) + "\n"

        # Return the CSV content in the response
        return jsonify({"csv_content": csv_content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
