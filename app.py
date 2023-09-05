from flask import Flask, jsonify, request
import pandas as pd
import functools

app = Flask(__name__)

# Load data from CSV file and perform initial data manipulation
data_file = "hero_profile.csv"
data_df = pd.read_csv(
    data_file,
    usecols=[
        "CharacterName",
        "Name",
        "Alias",
        "Alignment",
        "IsGoodGuy",
        "IsTeam",
        "TeamAffiliation",
        "Intelligence",
        "Strength",
        "Speed",
        "Durability",
        "Power",
        "Combat",
        "X",
        "IsSuperior",
        "Rating",
        "X-Factor",
    ],
)

# Aggregation logic
aggregated_data = data_df.groupby(["Alignment", "IsGoodGuy"])[
    ["Intelligence", "Strength", "Speed", "Durability", "Power", "Combat"]
].mean()


# LRU cache for get_data function
@functools.lru_cache(maxsize=128)
def get_data(alignment_filter=None):
    if alignment_filter:
        filtered_data = aggregated_data.reset_index()
        filtered_data = filtered_data[filtered_data["Alignment"] == alignment_filter]
        result = filtered_data.to_dict(orient="records")
    else:
        result = aggregated_data.reset_index().to_dict(orient="records")
    return result


# Flask route to get manipulated and aggregated data with URL filtering
@app.route("/get_data", methods=["GET"])
def get_data_route():
    alignment_filter = request.args.get("Alignment")
    return jsonify(get_data(alignment_filter))


if __name__ == "__main__":
    app.run(debug=True)
