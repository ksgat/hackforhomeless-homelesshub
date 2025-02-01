from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Load the CSV file (make sure facilities.csv is in the same directory)
df = pd.read_csv("facilities.csv")
# Replace NaN values so we can filter reliably
df.fillna("Unavailable", inplace=True)

# Load the cleanedpantrys.csv file
pantry_df = pd.read_csv("cleanedpantrys.csv")
pantry_df.fillna("Unavailable", inplace=True)

@app.route("/")
def index():
    # Serve the static HTML file
    return send_file("index.html")

@app.route("/food")
def food():
    # Serve the food.html file
    return send_file("food.html")
@app.route("/resume")
def resume():
    # Serve the food.html file
    return send_file("resume.html")
@app.route("/health")
def health():
    # Serve the food.html file
    return send_file("health.html")

@app.route("/search", methods=["GET"])
def search_facilities():
    # Get query parameters, e.g., CLOTHING=true, FOOD_GROCERIES=true, etc.
    filters = request.args.to_dict()
    filtered_df = df.copy()

    # For each category that's marked "true", filter out rows where the value is "Unavailable"
    for category, value in filters.items():
        if value.lower() == "true":
            filtered_df = filtered_df[filtered_df[category] != "Unavailable"]

    # Return the filtered data as JSON
    return jsonify(filtered_df.to_dict(orient="records"))

@app.route("/food/search", methods=["GET"])
def search_food_pantries():
    # Get query parameters for food pantries
    filters = request.args.to_dict()
    filtered_df = pantry_df.copy()

    # Filter based on the selected categories
    if "SHOPPING" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Shopping"]
    if "DIRECT_DISTRIBUTION" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Direct Distributions"]
    if "BOTH" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Shopping & Direct Distribution"]

    # Return the filtered data as JSON
    return jsonify(filtered_df.to_dict(orient="records"))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if no PORT is set
    app.run(host='0.0.0.0', port=port)
