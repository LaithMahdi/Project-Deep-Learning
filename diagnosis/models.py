from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

def upload_to_patient(instance, filename):
    """Définit le chemin d'upload pour les radiographies"""
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    new_filename = f"patient_{timestamp}.{ext}"
    return os.path.join('upload', new_filename)

class Diagnosis(models.Model):
    # Informations patient
    patient_name = models.CharField(max_length=200)
    patient_age = models.IntegerField()
    patient_gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')]
    )
    clinical_notes = models.TextField(blank=True, null=True)
    
    # Fichier radiographie
    xray_image = models.ImageField(upload_to=upload_to_patient)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # Résultats de l'IA
    ai_prediction = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    all_probabilities = models.JSONField(default=dict, blank=True)
    
    # Validation médicale
    validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    validation_date = models.DateTimeField(null=True, blank=True)
    final_diagnosis = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name_plural = "Diagnoses"
    
    def __str__(self):
        return f"{self.patient_name} - {self.upload_date.strftime('%d/%m/%Y')}"
    
    def get_top_predictions(self, n=3):
        """Retourne les n meilleures prédictions"""
        if self.all_probabilities:
            sorted_preds = sorted(
                self.all_probabilities.items(), 
                key=lambda x: x[1]['probability'], 
                reverse=True
            )
            return sorted_preds[:n]
        return []