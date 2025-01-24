# Django Vue3 Project

Ce projet contient une **application Django** configurée pour fonctionner avec un **frontend Vue3**. Voici un guide pour configurer, démarrer et développer l'application.

## Structure du Projet

L'arborescence du projet est la suivante :


## Prérequis

Avant de commencer, assure-toi d'avoir les outils suivants installés sur ton ordinateur :

- **Python 3.x** et **pip**
- **Node.js** et **npm**
- **Vue CLI** (optionnel, mais recommandé pour faciliter la gestion de Vue3)
- **Django 3.x+** et **Django REST Framework** (pour l'API)
- **Vue3** pour le frontend

## Installation

### 1. Cloner le projet

Clone le projet depuis le repository Git :

```bash
git clone https://github.com/ton_utilisateur/django_vue_project.git
cd django_vue_project
```

Crée un environnement virtuel Python à l'aide de venv:

Sur Windows :
```bash
.\env\Scripts\activate
```

Sur macOS/Linux :
```bash
source env/bin/activate
```

Installe les dépendances Python :
```bash
pip install -r backend/requirements.txt
```
Fais les migrations de la BDD puis lance le serveur:
```bash
python3 manage.py migrate
python3 manage.py startserver
```

Va dans le dossier frontend et installe les dépendances:
```bash
cd frontend
npm install
```
puis
```bash
npm run serve
```
