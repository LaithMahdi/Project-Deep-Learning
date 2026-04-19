# diagnosis/ml_models/predictor.py - Version démo fonctionnelle
import os
import json
import numpy as np
from datetime import datetime

class PulmonaryDiagnosticPredictor:
    """Prédicteur pour le diagnostic pulmonaire - Version démo"""
    
    def __init__(self):
        self.model = None
        self.class_indices = None
        self.class_names = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'pulmonary_diagnostic.h5')
        self.class_indices_path = os.path.join(os.path.dirname(__file__), 'class_indices.json')
        
        # Liste des pathologies pulmonaires
        self.default_classes = [
            'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema',
            'Effusion', 'Emphysema', 'Fibrosis', 'Hernia',
            'Infiltration', 'Mass', 'Nodule', 'Pneumonia', 'Pneumothorax'
        ]
        
        # Essayer de charger les classes
        self.load_classes()
        print("✅ API démarrée en mode démonstration")
        print("⚠️  Les prédictions sont simulées pour les tests")
        
    def load_classes(self):
        """Charge les classes depuis le fichier ou utilise les classes par défaut"""
        if os.path.exists(self.class_indices_path):
            try:
                with open(self.class_indices_path, 'r') as f:
                    self.class_indices = json.load(f)
                self.class_names = {v: k for k, v in self.class_indices.items()}
                print(f"✅ {len(self.class_names)} classes chargées")
                return
            except Exception as e:
                print(f"⚠️ Erreur chargement classes: {e}")
        
        # Utiliser les classes par défaut
        self.class_names = {i: name for i, name in enumerate(self.default_classes)}
        self.class_indices = {name: i for i, name in enumerate(self.default_classes)}
        print(f"✅ {len(self.class_names)} classes par défaut créées")
    
    def predict(self, img_path, confidence_threshold=0.5):
        """Simule une prédiction pour tester l'API"""
        
        # Vérifier que le fichier existe
        if not os.path.exists(img_path):
            return {
                'success': False,
                'error': f"Fichier non trouvé: {img_path}"
            }
        
        # Simuler une prédiction réaliste
        classes = list(self.class_names.values())
        num_classes = len(classes)
        
        # Générer des probabilités aléatoires avec une classe dominante
        np.random.seed(hash(img_path) % 2**32)  # Pour des résultats cohérents
        predictions = np.random.dirichlet(np.ones(num_classes) * 0.3)
        
        # Améliorer pour avoir une classe clairement dominante
        predicted_idx = np.argmax(predictions)
        predicted_pathology = classes[predicted_idx]
        confidence = float(predictions[predicted_idx])
        
        # Ajuster la confiance pour qu'elle soit entre 60% et 95%
        confidence = 0.6 + (confidence * 0.35)
        
        # Créer le dictionnaire des probabilités
        all_probabilities = {
            classes[i]: float(predictions[i]) if i != predicted_idx else confidence
            for i in range(num_classes)
        }
        
        # Normaliser
        total = sum(all_probabilities.values())
        all_probabilities = {k: v/total for k, v in all_probabilities.items()}
        
        # Trier
        sorted_probabilities = dict(
            sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True)
        )
        
        return {
            'success': True,
            'prediction': predicted_pathology,
            'confidence': round(confidence, 4),
            'is_confident': confidence >= confidence_threshold,
            'all_probabilities': sorted_probabilities,
            'top_3': list(sorted_probabilities.items())[:3],
            'mode': 'demo',
            'message': 'Mode démonstration - Prédictions simulées'
        }

# Singleton
_predictor_instance = None

def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = PulmonaryDiagnosticPredictor()
    return _predictor_instance