from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.conf import settings
from django.db import OperationalError, ProgrammingError
import os
from datetime import datetime
from .models import Diagnosis

# Import du prédicteur
try:
    from .ml_models.predictor import get_predictor
    predictor = get_predictor()
except Exception as e:
    print(f"Erreur chargement prédicteur: {e}")
    predictor = None

# ============================================
# PAGES HTML
# ============================================

def home_page(request):
    """Page d'accueil"""
    return render(request, 'home.html', {'title': 'Accueil'})

def upload_page(request):
    """Page d'upload"""
    return render(request, 'upload.html', {'title': 'Upload'})

def api_test_page(request):
    """Page de test simple (sans base.html)"""
    return render(request, 'test.html', {'title': 'Test API'})

def api_test_page_drf(request):
    """Page de test avec base.html"""
    return render(request, 'api_test.html', {'title': 'Test API'})

def test_multiple_page(request):
    """Page de test pour les prédictions multiples"""
    return render(request, 'test_multiple.html', {'title': 'Test Multiple'})

def history_page(request):
    """Page d'historique"""
    try:
        diagnoses = Diagnosis.objects.all()[:50]
    except (OperationalError, ProgrammingError):
        diagnoses = []
        messages.warning(request, "Base de donnees non migree: executez 'python manage.py migrate'.")
    context = {
        'title': 'Historique',
        'diagnoses': diagnoses
    }
    return render(request, 'history.html', context)

# ============================================
# UPLOAD ET PRÉDICTION (AVEC REDIRECTION)
# ============================================

# diagnosis/views.py - Modifiez upload_and_predict

@csrf_exempt
@require_http_methods(["POST"])
def upload_and_predict(request):
    """
    Vue pour l'upload et la prédiction avec redirection vers la page de résultats
    """
    
    if request.method == 'POST':
        # Récupérer les informations patient
        patient_name = request.POST.get('patient_name', 'Patient Test')
        patient_age = request.POST.get('patient_age', '45')
        patient_gender = request.POST.get('patient_gender', '')
        exam_date = request.POST.get('exam_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Vérifier si une image a été uploadée
        if 'image' not in request.FILES:
            messages.error(request, 'Veuillez sélectionner une image')
            return redirect('diagnosis:upload_page')
        
        image_file = request.FILES['image']
        
        # Vérifier le type de fichier
        if not image_file.content_type.startswith('image/'):
            messages.error(request, 'Le fichier doit être une image (JPG, PNG, JPEG)')
            return redirect('diagnosis:upload_page')
        
        # Créer le dossier temp
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Sauvegarder l'image temporairement
        file_name = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
        file_path = default_storage.save(
            os.path.join('temp', file_name),
            ContentFile(image_file.read())
        )
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        try:
            # Faire la prédiction
            if predictor is None:
                messages.error(request, 'Service de prédiction non disponible')
                return redirect('diagnosis:upload_page')
            
            result = predictor.predict(full_path)
            
            # Nettoyer le fichier temporaire
            if os.path.exists(full_path):
                os.remove(full_path)
            
            if result.get('success', False):
                image_file.seek(0)
                raw_confidence = result.get('confidence') or 0
                confidence_percent = float(raw_confidence) * 100 if raw_confidence <= 1 else float(raw_confidence)

                diagnosis = None
                try:
                    diagnosis = Diagnosis.objects.create(
                        patient_name=patient_name,
                        patient_age=int(patient_age) if str(patient_age).isdigit() else 0,
                        patient_gender=patient_gender if patient_gender in ['M', 'F', 'O'] else 'M',
                        clinical_notes='',
                        xray_image=image_file,
                        ai_prediction=result.get('prediction', ''),
                        confidence=confidence_percent,
                        all_probabilities=result.get('all_probabilities') or {}
                    )
                except (OperationalError, ProgrammingError):
                    messages.warning(request, "Analyse effectuee, mais non enregistree. Lancez 'python manage.py migrate'.")

                # Stocker les résultats dans la session avec les infos patient
                request.session['last_prediction'] = {
                    'diagnosis_id': diagnosis.id if diagnosis else None,
                    'patient_name': patient_name,
                    'patient_age': patient_age,
                    'patient_gender': patient_gender,
                    'exam_date': exam_date,
                    'prediction': result.get('prediction'),
                    'confidence': confidence_percent,
                    'is_confident': result.get('is_confident'),
                    'all_probabilities': result.get('all_probabilities'),
                    'top_3': result.get('top_3'),
                    'file_name': image_file.name,
                    'timestamp': datetime.now().isoformat(),
                    'release_date': diagnosis.upload_date.isoformat() if diagnosis else datetime.now().isoformat()
                }
                
                messages.success(request, f'Analyse terminée ! Diagnostic: {result.get("prediction")}')
                return redirect('diagnosis:result_page')
            else:
                messages.error(request, f'Erreur lors de la prédiction: {result.get("error", "Erreur inconnue")}')
                return redirect('diagnosis:upload_page')
                
        except Exception as e:
            if os.path.exists(full_path):
                os.remove(full_path)
            
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('diagnosis:upload_page')
    
    return redirect('diagnosis:upload_page')
# ============================================
# API ENDPOINTS (REST)
# ============================================

@csrf_exempt
@require_http_methods(["POST"])
def predict_diagnosis(request):
    """
    Endpoint API REST pour prédire le diagnostic d'une image
    Retourne un JSON
    """
    
    if predictor is None:
        return JsonResponse({
            'success': False,
            'error': 'Service de prédiction non disponible'
        }, status=503)
    
    if 'image' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': 'Aucune image fournie'
        }, status=400)
    
    image_file = request.FILES['image']
    
    # Vérifier le type de fichier
    if not image_file.content_type.startswith('image/'):
        return JsonResponse({
            'success': False,
            'error': 'Le fichier doit être une image'
        }, status=400)
    
    # Créer le dossier temp
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Sauvegarder l'image temporairement
    file_name = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
    file_path = default_storage.save(
        os.path.join('temp', file_name),
        ContentFile(image_file.read())
    )
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    try:
        # Faire la prédiction
        result = predictor.predict(full_path)
        result['file_name'] = image_file.name
        result['timestamp'] = datetime.now().isoformat()
        
        # Nettoyer le fichier temporaire
        if os.path.exists(full_path):
            os.remove(full_path)
        
        return JsonResponse(result)
        
    except Exception as e:
        # Nettoyer en cas d'erreur
        if os.path.exists(full_path):
            os.remove(full_path)
        
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def predict_multiple(request):
    """
    Endpoint API REST pour prédire plusieurs images à la fois
    Maximum 10 images par requête
    """
    
    if predictor is None:
        return JsonResponse({
            'success': False,
            'error': 'Service de prédiction non disponible'
        }, status=503)
    
    if 'images' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': 'Aucune image fournie. Utilisez le champ "images" avec plusieurs fichiers.'
        }, status=400)
    
    images = request.FILES.getlist('images')
    
    # Limiter à 10 images maximum
    if len(images) > 10:
        return JsonResponse({
            'success': False,
            'error': 'Maximum 10 images par requête'
        }, status=400)
    
    # Créer le dossier temp
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    results = []
    
    for idx, image_file in enumerate(images):
        # Vérifier le type de fichier
        if not image_file.content_type.startswith('image/'):
            results.append({
                'success': False,
                'file_name': image_file.name,
                'error': 'Le fichier doit être une image',
                'index': idx
            })
            continue
        
        # Sauvegarder l'image temporairement
        file_name = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{image_file.name}"
        file_path = default_storage.save(
            os.path.join('temp', file_name),
            ContentFile(image_file.read())
        )
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        try:
            # Faire la prédiction
            result = predictor.predict(full_path)
            result['file_name'] = image_file.name
            result['index'] = idx
            result['timestamp'] = datetime.now().isoformat()
            results.append(result)
            
        except Exception as e:
            results.append({
                'success': False,
                'file_name': image_file.name,
                'error': str(e),
                'index': idx
            })
        
        # Nettoyer le fichier temporaire
        if os.path.exists(full_path):
            os.remove(full_path)
    
    # Compter les succès et échecs
    success_count = sum(1 for r in results if r.get('success', False))
    error_count = len(results) - success_count
    
    return JsonResponse({
        'success': True,
        'total': len(results),
        'success_count': success_count,
        'error_count': error_count,
        'results': results
    }, status=200)

@require_http_methods(["GET"])
def get_model_info(request):
    """
    Endpoint API REST pour obtenir des informations sur le modèle
    """
    if predictor:
        return JsonResponse({
            'model_loaded': predictor.model is not None,
            'num_classes': len(predictor.class_names) if predictor.class_names else 13,
            'classes': list(predictor.class_names.values()) if predictor.class_names else [],
            'mode': getattr(predictor, 'mode', 'demo'),
            'status': 'active'
        })
    else:
        return JsonResponse({
            'model_loaded': False,
            'error': 'Prédicteur non disponible',
            'status': 'inactive'
        })
def result_page(request, pk=None):
    """Page de résultats"""
    if pk is not None:
        try:
            diagnosis = Diagnosis.objects.filter(pk=pk).first()
        except (OperationalError, ProgrammingError):
            diagnosis = None
        if diagnosis:
            context = {
                'title': 'Résultats',
                'patient_name': diagnosis.patient_name,
                'patient_age': diagnosis.patient_age,
                'patient_gender': diagnosis.patient_gender,
                'exam_date': diagnosis.upload_date.strftime('%Y-%m-%d'),
                'prediction': diagnosis.ai_prediction,
                'confidence': diagnosis.confidence,
                'all_probabilities': diagnosis.all_probabilities,
                'top_3': [],
                'is_confident': True,
                'file_name': os.path.basename(diagnosis.xray_image.name),
                'timestamp': diagnosis.upload_date.isoformat(),
                'release_date': diagnosis.upload_date,
                'released_by': 'Laith Mahdi and Dalel Loussaief'
            }
            return render(request, 'result.html', context)

    # Récupérer les données de la session
    last_prediction = request.session.get('last_prediction', {})

    confidence_value = last_prediction.get('confidence', 95.0)
    confidence_percent = float(confidence_value) * 100 if float(confidence_value) <= 1 else float(confidence_value)
    
    context = {
        'title': 'Résultats',
        'patient_name': last_prediction.get('patient_name', 'Patient Test'),
        'patient_age': last_prediction.get('patient_age', '45'),
        'patient_gender': last_prediction.get('patient_gender', ''),
        'exam_date': last_prediction.get('exam_date', datetime.now().strftime('%d/%m/%Y')),
        'prediction': last_prediction.get('prediction', 'Normal'),
        'confidence': confidence_percent,
        'all_probabilities': last_prediction.get('all_probabilities', {}),
        'top_3': last_prediction.get('top_3', []),
        'is_confident': last_prediction.get('is_confident', True),
        'file_name': last_prediction.get('file_name', ''),
        'timestamp': last_prediction.get('timestamp', ''),
        'release_date': last_prediction.get('release_date', ''),
        'released_by': 'Laith Mahdi and Dalel Loussaief'
    }
    return render(request, 'result.html', context)
@require_http_methods(["GET"])
def get_prediction_result(request, prediction_id):
    """
    Récupérer un résultat de prédiction par ID (stocké en session)
    """
    last_prediction = request.session.get('last_prediction')
    
    if last_prediction:
        return JsonResponse({
            'success': True,
            'prediction': last_prediction
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Aucune prédiction trouvée'
        }, status=404)