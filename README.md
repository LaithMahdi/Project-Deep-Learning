# PulmonaryAI - Plateforme Clinique d'Aide au Diagnostic Pulmonaire

**PulmonaryAI** est une plateforme web d'analyse de radiographies thoraciques reposant sur le deep learning (TensorFlow). Concue pour l'environnement clinique, elle fournit:

✅ **Interface web intuitive** pour uploader des radiographies et consulter les resultats  
✅ **Inference IA rapide** via modele CNN pre-entraine, avec probabilites multi-classes  
✅ **API REST documentee** pour integration dans d'autres systemes ou applications mobile  
✅ **Enregistrement automatique** de chaque analyse avec metadonnees patient et tracabilite  
✅ **Historique et comparaisons** pour suivi longitudinal des cas  
✅ **Deployable via Docker** pour environnement de production

## Fonctionnalites

- Upload d'image pulmonaire (JPG, JPEG, PNG)
- Prediction IA avec classe principale et probabilites
- Historique des analyses (structure deja prevue)
- API REST pour prediction simple et multiple
- Interface Tailwind CSS (via CDN) modernisee et responsive

## Stack Technique

| Composant            | Technologie                      |
| -------------------- | -------------------------------- |
| **Backend**          | Django 5.1.5                     |
| **IA**               | TensorFlow 2.20 / Keras          |
| **API**              | Django REST Framework 3.15       |
| **Traitement image** | Pillow, NumPy, scikit-learn      |
| **UI**               | Tailwind CSS (CDN)               |
| **Base de donnees**  | SQLite (dev) / PostgreSQL (prod) |
| **Containerisation** | Docker & Docker Compose          |
| **Python**           | 3.11+                            |

## Structure Principale

```
django_deepLearning/
|- pulmonary_api/          # Configuration Django (settings, urls, wsgi, asgi)
|- diagnosis/              # App principale (views, urls, templates, modeles IA)
|  |- ml_models/           # Modele .h5, mapping classes, logique de prediction
|  |- templates/           # Interface web Tailwind
|- media/                  # Fichiers temporaires uploades (runtime)
|- db.sqlite3              # Base SQLite
|- Dockerfile              # Configuration Docker
|- docker-compose.yml      # Orchestration Docker Compose
|- requirements.txt
|- manage.py
```

## Installation Rapide (Docker)

**Prerequis**: Docker et Docker Compose installes.

```bash
git clone https://github.com/LaithMahdi/Project-Deep-Learning
cd Project-Deep-Learning
docker-compose up --build
```

Acces: http://localhost:8000/diagnosis/

## Installation

1. Cloner le projet

```bash
git clone https://github.com/LaithMahdi/Project-Deep-Learning
cd Project-Deep-Learning
```

2. Creer un environnement virtuel

```bash
python -m venv .venv
```

3. Activer l'environnement virtuel

Windows (CMD):

```bat
.venv\Scripts\activate.bat
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

Un script shell est disponible pour automatiser l'installation locale:

```bash
bash script.sh
```

**Note**: Ce script fonctionne sous Git Bash (Windows) et bash native (Linux/Mac).

## Acces Application

| URL                                          | Description                      |
| -------------------------------------------- | -------------------------------- |
| http://127.0.0.1:8000/diagnosis/             | Accueil et page d'analyse        |
| http://127.0.0.1:8000/diagnosis/upload-page/ | Interface d'upload               |
| http://127.0.0.1:8000/diagnosis/history/     | Historique des analyses          |
| http://127.0.0.1:8000/diagnosis/api-test/    | Laboratoire API (test visuel)    |
| http://127.0.0.1:8000/admin/                 | Admin Django (si superuser cree) |

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

- [ ] Migration vers PostgreSQL pour production
- [ ] Gestion d'authentification et autorisations (JWT/OAuth2)
- [ ] Tests unitaires et d'integration complets
- [ ] Logging structuree et monitoring (Sentry, ELK)
- [ ] CI/CD pipeline (GitHub Actions, GitLab CI)
- [ ] Documentation API Swagger/OpenAPI
- [ ] Support multi-modeles IA
- [ ] Interface admin amelioree pour validation medicale

## Deployment en Production

### Avec Docker

1. **Creer un fichier `.env.prod`**:

```env
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=postgresql://user:password@db:5432/pulmonaryai
SECRET_KEY=your-secure-random-key
```

2. **Utiliser Gunicorn au lieu du serveur de dev**:

```dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "pulmonary_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

3. **Configurer un reverse proxy (Nginx, Apache)**

4. **Securiser les communications (HTTPS/SSL)**

5. **Mettre en place un backup strategy pour media/ et db**

### Sans Docker (VPS/Serveur)

1. Cloner le repo sur le serveur
2. Configurer virtualenv et installer dependances
3. Configurer variables d'environnement (`DEBUG=False`, `SECRET_KEY`, etc.)
4. Utiliser Gunicorn + Systemd pour persistance du service
5. Configurer Nginx comme reverse proxy
6. Configurer SSL avec Let's Encrypt

## Support & Contribution

Pour toute question, bug report, ou contribution:

1. Ouvrir une issue sur le repository
2. Soumettre une pull request avec description claire
3. Respecter les conventions de code et tests

## License

Ce projet est fourni a titre informatif pour usage educationnel et clinique-research.
La responsabilite du resultat medical reste celle du praticien clinicien.
