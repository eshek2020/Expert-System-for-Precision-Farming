from flask import Flask, render_template, request, jsonify
from expert_system import PrecisionFarmingExpertSystem

app = Flask(__name__)
expert_system = PrecisionFarmingExpertSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json

    soil_data = {
        'type': data['soil_type'],
        'moisture': float(data['soil_moisture']),
        'nutrients': float(data['soil_nutrients'])
    }

    weather_data = {
        'temperature': float(data['temperature']),
        'humidity': float(data['humidity']),
        'precipitation': float(data.get('precipitation', 0))
    }

    crop_rec = expert_system.get_crop_recommendation(soil_data, weather_data)
    irrigation_rec = expert_system.get_irrigation_schedule(soil_data['moisture'], weather_data)
    fertilizer_rec = expert_system.get_fertilizer_recommendation(soil_data['nutrients'], crop_rec, data.get('growth_stage', 'vegetative'))

    if 'pest_symptoms' in data and data['pest_symptoms']:
        pest_rec = expert_system.get_pest_management(crop_rec, data['pest_symptoms'])
    else:
        pest_rec = "No pest symptoms reported"

    return jsonify({
        'crop_recommendation': crop_rec,
        'irrigation_recommendation': irrigation_rec,
        'fertilizer_recommendation': fertilizer_rec,
        'pest_management': pest_rec
    })

if __name__ == '__main__':
    app.run(debug=True)
