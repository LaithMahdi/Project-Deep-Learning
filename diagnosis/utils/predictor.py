"""
Predictor pour diagnostic pulmonaire
Version minimaliste sans dépendances externes
"""
import os
import random

class PulmonaryPredictor:
    def __init__(self):
        self.class_names = [
            'COVID-19', 'Pneumonia', 'Tuberculosis', 'Edema', 
            'Lung_Opacity', 'Normal', 'Fibrosis'
        ]
        print("✅ PulmonaryPredictor initialisé (mode démonstration)")
    
    def predict(self, image_path):
        """Simule une prédiction"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image non trouvée: {image_path}")
            
            # Simuler des probabilités
            predictions = {}
            
            base_probs = {
                'Normal': 45,
                'Pneumonia': 15,
                'COVID-19': 12,
                'Lung_Opacity': 8,
                'Tuberculosis': 5,
                'Edema': 4,
                'Fibrosis': 3
            }
            
            for class_name in self.class_names:
                base = base_probs.get(class_name, 5)
                variation = random.uniform(-2, 2)
                prob = max(0.1, base + variation)
                predictions[class_name] = {
                    'probability': prob,
                    'percentage': f"{prob:.1f}%"
                }
            
            # Normaliser
            total = sum(p['probability'] for p in predictions.values())
            for class_name in predictions:
                predictions[class_name]['probability'] = (predictions[class_name]['probability'] / total) * 100
                predictions[class_name]['percentage'] = f"{predictions[class_name]['probability']:.1f}%"
            
            # Trier
            sorted_results = dict(sorted(
                predictions.items(), 
                key=lambda x: x[1]['probability'], 
                reverse=True
            ))
            
            top_prediction = list(sorted_results.keys())[0]
            confidence = sorted_results[top_prediction]['probability']
            
            return {
                'top_prediction': top_prediction,
                'confidence': confidence,
                'all_predictions': sorted_results,
                'raw_predictions': []
            }
            
        except Exception as e:
            print(f"Erreur: {e}")
            raise
    
    def get_recommendations(self, pathology):
        """Retourne des recommandations"""
        recommendations = {
            'COVID-19': {
                'severity': 'ÉLEVÉE',
                'actions': ['Isolement immédiat', 'Test PCR recommandé'],
                'follow_up': '24-48h'
            },
            'Pneumonia': {
                'severity': 'MODÉRÉE',
                'actions': ['Antibiothérapie', 'Radio de contrôle dans 7-10j'],
                'follow_up': '7 jours'
            },
            'Normal': {
                'severity': 'FAIBLE',
                'actions': ['Pas d\'action urgente', 'Suivi standard'],
                'follow_up': 'Si symptômes'
            }
        }
        
        default_reco = {
            'severity': 'À ÉVALUER',
            'actions': ['Consultation spécialisée recommandée'],
            'follow_up': 'À déterminer'
        }
        
        return recommendations.get(pathology, default_reco)


# Instance globale
predictor = PulmonaryPredictor()
print("✅ Predictor prêt (mode minimaliste)")