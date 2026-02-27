import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
import joblib
import os

class PrecisionFarmingExpertSystem:
    def __init__(self):
        # Database connection (update username:password if needed)
        self.engine = create_engine('mysql+pymysql://root:@localhost/precision_farming')

        # Encoders for categorical data
        self.soil_encoder = LabelEncoder()
        self.crop_encoder = LabelEncoder()

        # Model path
        self.model_path = "models/crop_model.pkl"

        # Load or train model
        self.crop_model = None
        self.load_or_train_model()

    def load_or_train_model(self):
        """Load saved model if available, otherwise train a new one"""
        if os.path.exists(self.model_path):
            self.crop_model = joblib.load(self.model_path)
            self.soil_encoder = joblib.load("models/soil_encoder.pkl")
            self.crop_encoder = joblib.load("models/crop_encoder.pkl")
            print("✅ Loaded trained model")
        else:
            print("⚡ Training new model...")
            self.train_model()

    def train_model(self):
        """Train the crop recommendation model"""
        query = "SELECT * FROM farming_data"
        df = pd.read_sql(query, self.engine)

        if df.empty:
            raise ValueError("❌ farming_data table is empty! Insert sample rows first.")

        # Encode categorical values
        df['soil_type'] = self.soil_encoder.fit_transform(df['soil_type'])
        df['crop_type'] = self.crop_encoder.fit_transform(df['crop_type'])

        # Features & labels
        X = df[['soil_type', 'soil_moisture', 'soil_nutrients', 'temperature', 'humidity']]
        y = df['crop_type']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.crop_model = DecisionTreeClassifier()
        self.crop_model.fit(X_train, y_train)

        acc = accuracy_score(y_test, self.crop_model.predict(X_test))
        print(f"✅ Model trained with accuracy: {acc:.2f}")

        # Save model + encoders
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.crop_model, self.model_path)
        joblib.dump(self.soil_encoder, "models/soil_encoder.pkl")
        joblib.dump(self.crop_encoder, "models/crop_encoder.pkl")

    def get_crop_recommendation(self, soil_data, weather_data):
        """Predict the best crop"""
        input_data = {
            'soil_type': self.soil_encoder.transform([soil_data['type']])[0],
            'soil_moisture': soil_data['moisture'],
            'soil_nutrients': soil_data['nutrients'],
            'temperature': weather_data['temperature'],
            'humidity': weather_data['humidity']
        }

        df = pd.DataFrame([input_data])
        prediction = self.crop_model.predict(df)
        return self.crop_encoder.inverse_transform(prediction)[0]

    def get_irrigation_schedule(self, soil_moisture, weather_forecast):
        """Simple irrigation rules"""
        if soil_moisture < 30:
            return "Immediate irrigation needed"
        elif soil_moisture < 50 and weather_forecast.get('precipitation', 0) < 5:
            return "Irrigate within 24 hours"
        else:
            return "No irrigation needed currently"

    def get_fertilizer_recommendation(self, soil_nutrients, crop_type, growth_stage):
        """Simple fertilizer rules"""
        recommendations = {
            'low': {
                'wheat': 'NPK 20-20-20 at 50kg/acre',
                'rice': 'Urea at 40kg/acre',
                'corn': 'NPK 17-17-17 at 60kg/acre'
            },
            'medium': {
                'wheat': 'NPK 15-15-15 at 40kg/acre',
                'rice': 'NPK 20-10-10 at 35kg/acre',
                'corn': 'NPK 20-10-10 at 50kg/acre'
            },
            'high': {
                'wheat': 'No fertilizer needed',
                'rice': 'No fertilizer needed',
                'corn': 'No fertilizer needed'
            }
        }

        nutrient_level = 'low' if soil_nutrients < 30 else 'high' if soil_nutrients > 70 else 'medium'
        return recommendations[nutrient_level].get(crop_type, "Consult expert")

    def get_pest_management(self, crop_type, symptoms):
        """Simple pest rules"""
        pest_db = {
            'wheat': {
                'yellow leaves': "Rust infection. Apply fungicide.",
                'holes in leaves': "Armyworm infestation. Apply pesticide."
            },
            'rice': {
                'yellow leaves': "Possible nitrogen deficiency or bacterial blight.",
                'white spots': "Rice blast disease. Apply fungicide."
            }
        }
        return pest_db.get(crop_type, {}).get(symptoms, "No specific recommendation.")


if __name__ == "__main__":
    expert = PrecisionFarmingExpertSystem()

    # Example input
    soil_data = {'type': 'loamy', 'moisture': 45, 'nutrients': 55}
    weather_data = {'temperature': 28, 'humidity': 65, 'precipitation': 0}

    crop_rec = expert.get_crop_recommendation(soil_data, weather_data)
    irrigation_rec = expert.get_irrigation_schedule(soil_data['moisture'], weather_data)
    fertilizer_rec = expert.get_fertilizer_recommendation(soil_data['nutrients'], crop_rec, 'vegetative')
    pest_rec = expert.get_pest_management(crop_rec, 'yellow leaves')

    print(f"🌱 Recommended Crop: {crop_rec}")
    print(f"💧 Irrigation: {irrigation_rec}")
    print(f"🌿 Fertilizer: {fertilizer_rec}")
    print(f"🐛 Pest Management: {pest_rec}")
