# PulmonaryAI - Django Deep Learning Diagnostic Platform

PulmonaryAI est une application Django pour l'analyse de radiographies thoraciques avec un modele deep learning (TensorFlow). Le projet fournit:

- une interface web professionnelle pour uploader une image et lire les resultats,
- des endpoints API REST pour integrer la prediction dans d'autres applications,
- une presentation des classes probables et des scores de confiance.

## Fonctionnalites

- Upload d'image pulmonaire (JPG, JPEG, PNG)
- Prediction IA avec classe principale et probabilites
- Historique des analyses (structure deja prevue)
- API REST pour prediction simple et multiple
- Interface Tailwind CSS (via CDN) modernisee et responsive

## Stack Technique

- Backend: Django 4.2
- IA: TensorFlow / Keras
- API: Django REST Framework
- Traitement image: Pillow, NumPy
- UI: Tailwind CSS (CDN)
- Base de donnees: SQLite

## Structure Principale

```
django_deepLearning/
|- pulmonary_api/          # Configuration Django (settings, urls, wsgi, asgi)
|- diagnosis/              # App principale (views, urls, templates, modeles IA)
|  |- ml_models/           # Modele .h5, mapping classes, logique de prediction
|  |- templates/           # Interface web Tailwind
|- media/                  # Fichiers temporaires uploades (runtime)
|- db.sqlite3              # Base SQLite
|- requirements.txt
|- manage.py
```

## Installation

1. Cloner le projet

```bash
git clone <votre-repo>
cd django_deepLearning
```

2. Creer un environnement virtuel

```bash
python -m venv .venv
```

3. Activer l'environnement virtuel

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Windows (CMD):

```bat
.venv\Scripts\activate.bat
```

Windows (Git Bash):

```bash
source .venv/Scripts/activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

4. Installer les dependances

```bash
pip install -r requirements.txt
```

Si vous voyez `Defaulting to user installation`, vous n'etes pas dans le venv.
Sur Windows, utilisez directement le Python du venv:

```bash
.venv/Scripts/python -m pip install --upgrade pip
.venv/Scripts/python -m pip install -r requirements.txt
```

5. Appliquer les migrations

```bash
python manage.py migrate
```

6. Lancer le serveur

```bash
python manage.py runserver
```

## Script Automatique

Un script shell est disponible pour automatiser tout le setup:

- creation du venv
- activation du venv
- installation des dependances
- makemigrations + migrate
- lancement du serveur

Utilisation:

```bash
bash script.sh
```

Remarque:

- Sur Windows, ce script est concu pour Git Bash.
- L'activation faite dans le script est valable dans le processus du script. Le serveur est lance dans ce meme processus.

## Acces Application

- Interface analyse: http://127.0.0.1:8000/diagnosis/
- API Lab (test visuel): http://127.0.0.1:8000/diagnosis/api-test/
- Admin Django: http://127.0.0.1:8000/admin/

## Endpoints API

### 1. Prediction simple

- URL: `POST /diagnosis/api/predict/`
- Form-data:
  - `image` (fichier image)

Exemple cURL:

```bash
curl -X POST http://127.0.0.1:8000/diagnosis/api/predict/ \
	-F "image=@chest_xray.jpg"
```

### 2. Prediction multiple

- URL: `POST /diagnosis/api/predict-multiple/`
- Form-data:
  - `images` (plusieurs fichiers, max 10)

### 3. Informations modele

- URL: `GET /diagnosis/api/model-info/`

### 4. Dernier resultat session

- URL: `GET /diagnosis/api/result/<prediction_id>/`

## Interface Tailwind

Le projet utilise Tailwind CSS via CDN dans le template de base. Aucune etape Node.js n'est necessaire.

- Integration: script CDN dans `diagnosis/templates/base.html`
- Pages redesign:
  - upload,
  - resultats,
  - historique,
  - API Lab,
  - page legacy test API.

Si vous souhaitez une integration Tailwind compilee (CLI/PostCSS), vous pouvez ajouter un pipeline Node plus tard, mais ce n'est pas obligatoire pour ce projet.

## Notes Importantes

- Le modele IA est charge depuis `diagnosis/ml_models/pulmonary_diagnostic.h5`.
- Les images uploades sont sauvegardees temporairement dans `media/temp` puis supprimees apres prediction.
- En mode developpement, `DEBUG=True` et SQLite sont utilises.
- Si vous utilisez une version recente de Python (ex: 3.13), utilisez les versions du `requirements.txt` mises a jour (TensorFlow 2.20+).

## Depannage Installation

Si `pip install -r requirements.txt` echoue avec un message de type:

`No matching distribution found for tensorflow==...`

faites ces verifications:

```bash
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verification rapide (Windows Git Bash):

```bash
which python
python -c "import sys; print(sys.executable)"
```

Le chemin doit pointer vers `.venv/Scripts/python`.

## Commandes Utiles

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Ameliorations Recommandees

- Brancher `history_page` sur les donnees reelles du modele `Diagnosis`
- Ajouter des tests unitaires pour les endpoints API
- Ajouter gestion d'authentification pour espaces medecins
- Ajouter journalisation et monitoring des predictions
