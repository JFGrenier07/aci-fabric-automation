# 🤝 Contribuer au Moteur d'Automatisation ACI Fabric

Merci de votre intérêt à contribuer ! Ce document fournit des directives et instructions pour contribuer au projet Moteur d'Automatisation ACI Fabric.

## 🎯 Façons de Contribuer

### 🐛 Rapports de Bogues
- Rechercher problèmes existants avant d'en créer nouveaux
- Utiliser le modèle rapport bogue
- Inclure informations système et logs erreur
- Fournir étapes reproduction minimales

### ✨ Demandes Fonctionnalités
- Vérifier si fonctionnalité existe déjà
- Utiliser modèle demande fonctionnalité
- Expliquer cas usage et valeur métier
- Considérer compatibilité rétroactive

### 📝 Documentation
- Améliorer README, guides et commentaires code
- Ajouter exemples et cas usage
- Corriger fautes et explications peu claires
- Traduire documentation

### 💻 Contributions Code
- Corrections bogues et améliorations performance
- Support nouveaux objets ACI
- Infrastructure tests
- Outillage développeur

## 🚀 Commencer

### 1. Configuration Développement

```bash
# Forker le dépôt sur GitHub
# Cloner votre fork
git clone https://github.com/VOTRE_NOM_UTILISATEUR/aci-fabric-automation.git
cd aci-fabric-automation

# Créer environnement développement
python3 -m venv venv
source venv/bin/activate

# Installer dépendances développement
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Installer hooks pre-commit
pre-commit install
```

### 2. Dépendances Développement

Créer `requirements-dev.txt` :
```txt
# Tests
pytest>=7.0.0
pytest-ansible>=3.0.0
pytest-cov>=4.0.0
pytest-mock>=3.0.0

# Qualité code
black>=22.0.0
flake8>=4.0.0
isort>=5.0.0
mypy>=0.910

# Documentation
mkdocs>=1.4.0
mkdocs-material>=8.0.0

# Outils développement
pre-commit>=2.15.0
tox>=3.20.0
```

### 3. Configuration Pre-commit

Créer `.pre-commit-config.yaml` :
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]
```

## 📊 Flux Développement

### 1. Stratégie Branches

```bash
# Créer branche fonctionnalité
git checkout -b feature/fonctionnalite-geniale

# Créer branche correction bogue
git checkout -b bugfix/corriger-probleme-123

# Créer branche documentation
git checkout -b docs/ameliorer-readme
```

### 2. Apporter Modifications

```bash
# Faire vos modifications
vim excel_to_csv.py

# Exécuter tests
pytest tests/

# Exécuter vérifications qualité code
black .
flake8 .
isort .

# Tester vos modifications
python3 excel_to_csv.py config_test.xlsx
ansible-playbook --syntax-check config_test.yml
```

### 3. Directives Commits

**Format Message Commit** :
```
type(portée): description

Explication plus longue si nécessaire

Corrige #123
```

**Types** :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction bogue
- `docs` : Modifications documentation
- `style` : Modifications style code
- `refactor` : Refactoring code
- `test` : Ajout/mise à jour tests
- `chore` : Tâches maintenance

**Exemples** :
```bash
git commit -m "feat(parser): ajouter support IPs secondaires L3Out"
git commit -m "fix(tasks): résoudre problème dépendance tenant"
git commit -m "docs(readme): mettre à jour instructions installation"
```

## 🧪 Directives Tests

### 1. Structure Tests

```
tests/
├── unit/
│   ├── test_parser.py
│   ├── test_validator.py
│   └── test_generator.py
├── integration/
│   ├── test_excel_to_csv.py
│   └── test_ansible_deployment.py
├── fixtures/
│   ├── config_exemple.xlsx
│   └── sortie_attendue.csv
└── conftest.py
```

### 2. Écrire Tests

```python
# tests/unit/test_parser.py
import pytest
from excel_to_csv import ExcelToCSVSimple


class TestExcelParser:
    def test_has_real_data_with_valid_sheet(self):
        """Tester que feuilles valides sont détectées correctement."""
        parser = ExcelToCSVSimple("tests/fixtures/config_exemple.xlsx")
        assert parser.has_real_data("vlan_pool") is True

    def test_has_real_data_with_empty_sheet(self):
        """Tester que feuilles vides sont rejetées."""
        parser = ExcelToCSVSimple("tests/fixtures/config_exemple.xlsx")
        assert parser.has_real_data("feuille_vide") is False

    @pytest.mark.parametrize("nom_feuille", [
        "Navigation", "Sheet1", "Template", "README"
    ])
    def test_ignore_system_sheets(self, nom_feuille):
        """Tester que feuilles système sont ignorées."""
        parser = ExcelToCSVSimple()
        assert nom_feuille in parser.ignore_sheets
```

### 3. Exécuter Tests

```bash
# Exécuter tous tests
pytest

# Exécuter avec couverture
pytest --cov=excel_to_csv

# Exécuter fichier test spécifique
pytest tests/unit/test_parser.py

# Exécuter avec sortie verbeuse
pytest -v

# Exécuter tests intégration seulement
pytest tests/integration/
```

## 📋 Ajouter Nouveaux Objets ACI

### 1. Création Fichier Tâche

Créer `tasks/nouvel_objet.yml` :
```yaml
---
# Tâches pour gérer les nouveaux_objets avec read_csv
- name: "Lire CSV Nouveaux Objets"
  read_csv:
    path: "{{ csv_dir }}/nouvel_objet.csv"
    delimiter: ','
  register: nouvel_objet_csv
  when: (csv_dir + '/nouvel_objet.csv') is file

- name: "Afficher les Nouveaux Objets détectés"
  debug:
    msg: "Nouveaux Objets à traiter: {{ nouvel_objet_csv.list | map(attribute='nom') | list }}"
  when: nouvel_objet_csv is defined and nouvel_objet_csv.list is defined

- name: "{{ item.nom }} - Créer le Nouvel Objet ACI"
  cisco.aci.aci_nouvel_objet:
    host: "{{ aci_hostname }}"
    username: "{{ aci_username }}"
    password: "{{ aci_password }}"
    validate_certs: "{{ aci_validate_certs | default(false) }}"
    use_ssl: true
    # Paramètres spécifiques objet
    nom: "{{ item.nom }}"
    description: "{{ item.description | default('') }}"
    state: "{{ item.state | default(global_state) }}"
  loop: "{{ nouvel_objet_csv.list }}"
  when:
    - nouvel_objet_csv is defined
    - nouvel_objet_csv.list is defined
    - item.nom is defined
    - item.nom | length > 0
  tags:
    - nouvel_objet
    - aci_nouvel_objet
```

### 2. Mettre à Jour Analyseur

Ajouter à `excel_to_csv.py` :
```python
# Ajouter à liste ordre_modules en position dépendance correcte
ordre_modules = [
    # ... modules existants
    'aci_nouvel_objet',  # Ajouter en ordre approprié
    # ... modules restants
]

# Ajouter au dictionnaire descriptions
descriptions = {
    # ... descriptions existantes
    'nouvel_objet': 'Description Nouvel Objet',
}
```

### 3. Mise à Jour Documentation

Ajouter à `EXCEL_TEMPLATE.fr.md` :
```markdown
### Configuration Nouvel Objet

**Nom Feuille** : `nouvel_objet`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `nom` | String | Nom objet | `Nouvel_Objet_1` |
| `description` | String | Description objet | `Description ici` |
| `champ_requis` | String | Paramètre requis | `valeur` |

**Exemple** :
```excel
nom,description,champ_requis
Nouvel_Objet_1,Premier nouvel objet,valeur1
Nouvel_Objet_2,Deuxième nouvel objet,valeur2
```

### 4. Ajouter Tests

Créer `tests/unit/test_nouvel_objet.py` :
```python
import pytest
from unittest.mock import patch, MagicMock


class TestNouvelObjetTasks:
    @patch('ansible.modules.read_csv')
    def test_nouvel_objet_csv_reading(self, mock_read_csv):
        """Tester lecture CSV pour nouveaux objets."""
        mock_read_csv.return_value = {
            'list': [
                {'nom': 'Objet_Test', 'description': 'Objet test'}
            ]
        }
        # Implémentation test
```

## 📚 Standards Documentation

### 1. Documentation Code

```python
def create_dynamic_playbook(self, fichier_excel, modules_detectes):
    """Créer playbook Ansible dynamique basé sur modules détectés.

    Args:
        fichier_excel (str): Chemin vers fichier Excel source
        modules_detectes (list): Liste modules ACI détectés

    Returns:
        str: Chemin vers fichier playbook généré

    Raises:
        FileNotFoundError: Si fichier Excel n'existe pas
        ValidationError: Si modules sont invalides

    Example:
        >>> parser = ExcelToCSVSimple()
        >>> playbook = parser.create_dynamic_playbook(
        ...     "config.xlsx",
        ...     ["aci_tenant", "aci_vrf"]
        ... )
        >>> print(playbook)
        'config.yml'
    """
```

### 2. Mises à Jour README

- Mettre à jour liste objets supportés
- Ajouter exemples pour nouvelles fonctionnalités
- Mettre à jour instructions installation si nécessaire
- Ajouter dépannage pour nouveaux problèmes

### 3. Documentation Architecture

- Mettre à jour `ARCHITECTURE.fr.md` pour changements structurels
- Documenter nouveaux flux données
- Expliquer nouvelles dépendances

## 🔍 Processus Revue Code

### 1. Avant Soumission

- [ ] Tous tests passent
- [ ] Code suit directives style
- [ ] Documentation mise à jour
- [ ] Messages commit clairs
- [ ] Aucune donnée sensible incluse

### 2. Modèle Pull Request

```markdown
## Description
Brève description modifications

## Type Changement
- [ ] Correction bogue
- [ ] Nouvelle fonctionnalité
- [ ] Mise à jour documentation
- [ ] Amélioration performance

## Tests
- [ ] Tests unitaires ajoutés/mis à jour
- [ ] Tests intégration passent
- [ ] Tests manuels complétés

## Liste Vérification
- [ ] Code suit directives style
- [ ] Auto-revue complétée
- [ ] Documentation mise à jour
- [ ] Aucun changement cassant
```

### 3. Critères Revue

**Qualité Code** :
- Suit standards Python PEP 8
- Gestion erreur appropriée
- Noms variables/fonctions clairs
- Commentaires appropriés

**Fonctionnalité** :
- Résout problème énoncé
- Ne casse pas fonctionnalités existantes
- Gère cas limites
- Considérations performance

**Documentation** :
- Messages commit clairs
- Documentation mise à jour
- Commentaires code où nécessaire
- Exemples fournis

## 🏷️ Processus Releases

### 1. Numérotation Versions

Nous suivons [Versioning Sémantique](https://semver.org/) :
- **MAJEUR** : Changements cassants
- **MINEUR** : Nouvelles fonctionnalités (compatible rétroactivement)
- **PATCH** : Corrections bogues (compatible rétroactivement)

### 2. Liste Vérification Release

- [ ] Tous tests passent
- [ ] Documentation mise à jour
- [ ] CHANGELOG.fr.md mis à jour
- [ ] Version incrémentée dans fichiers appropriés
- [ ] Tag Git créé
- [ ] Notes release écrites

## 💬 Directives Communauté

### 1. Code Conduite

- Être respectueux et inclusif
- Se concentrer sur feedback constructif
- Aider nouveaux arrivants apprendre
- Respecter perspectives différentes

### 2. Canaux Communication

- **GitHub Issues** : Rapports bogues et demandes fonctionnalités
- **GitHub Discussions** : Questions générales et idées
- **Pull Requests** : Revue code et collaboration

### 3. Obtenir Aide

- Vérifier documentation existante d'abord
- Rechercher GitHub issues
- Demander dans GitHub Discussions
- Fournir exemples reproduction minimaux

## 🙏 Reconnaissance

Contributeurs seront reconnus dans :
- Fichier CONTRIBUTORS.md
- Notes release
- Graphiques contributeurs GitHub
- Mentions spéciales pour contributions significatives

Merci de contribuer au Moteur d'Automatisation ACI Fabric ! 🎉