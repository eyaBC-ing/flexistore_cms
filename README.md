# FlexiStore CMS

FlexiStore CMS est un mini système de gestion de contenu (CMS) basé sur Django. Il permet aux utilisateurs de créer dynamiquement des pages web à partir de composants personnalisés (boutons, titres, produits, formulaires, etc.), **sans écrire de code**.

---

## Fonctionnalités

- Création de composants dynamiques via un modèle JSON Schema
- Rendu des composants via templates HTML personnalisables
- Aperçu en temps réel avec HTMX
- API REST & GraphQL sécurisées avec JWT
- Système de cache côté serveur
- Interface utilisateur moderne avec Tailwind CSS

---

## Technologies utilisées

- Django / Django REST Framework
- Strawberry GraphQL
- Tailwind CSS
- HTMX
- PostgreSQL (ou SQLite pour dev)
- Celery (pour le rendu différé/précompilé des composants)

---

## Installation

git clone https://github.com/eyaBC-ing/flexistore-cms.git
cd flexistore-cms
python -m venv venv_py311
source venv/bin/activate  # ou `venv\Scripts\activate` sur Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
