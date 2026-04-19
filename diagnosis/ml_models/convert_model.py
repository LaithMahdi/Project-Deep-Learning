# convert_model.py
import tensorflow as tf
from tensorflow import keras

# Charger l'ancien modèle
try:
    model = keras.models.load_model('models/pulmonary_diagnostic.h5')
    print("✅ Modèle chargé")
    
    # Sauvegarder au nouveau format
    model.save('models/pulmonary_diagnostic_new.h5', save_format='h5')
    print("✅ Modèle converti et sauvegardé")
    
    # Tester le nouveau modèle
    test_model = keras.models.load_model('models/pulmonary_diagnostic_new.h5')
    print("✅ Nouveau modèle testé avec succès")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("Utilisez la version démo à la place")