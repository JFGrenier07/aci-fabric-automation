# 📦 Guide d'Installation

Ce guide fournit des instructions d'installation complètes pour le Moteur d'Automatisation ACI Fabric dans différents environnements.

## 🔧 Exigences Système

### Exigences Minimales
- **Système d'Exploitation** : Linux (Ubuntu 18.04+, RHEL 7+, CentOS 7+), macOS 10.15+, ou Windows 10 avec WSL2
- **Python** : 3.8 ou supérieur
- **Mémoire** : 2GB RAM (4GB+ recommandé pour grandes configurations)
- **Stockage** : 1GB espace disque libre
- **Réseau** : Connectivité directe à l'interface de gestion APIC

### Exigences Recommandées
- **Python** : 3.9+ pour performance optimale
- **Mémoire** : 8GB RAM pour déploiements entreprise
- **CPU** : 4+ cœurs pour exécution parallèle
- **Réseau** : Connexion faible latence à APIC (< 50ms)

## 🐧 Installation Linux

### Ubuntu/Debian

```bash
# Mettre à jour paquets système
sudo apt update && sudo apt upgrade -y

# Installer Python et pip
sudo apt install python3 python3-pip python3-venv git -y

# Vérifier version Python
python3 --version  # Devrait être 3.8+

# Cloner le dépôt
git clone https://github.com/JFGrenier07/aci-fabric-automation.git
cd aci-fabric-automation

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances Python
pip install --upgrade pip
pip install pandas openpyxl ansible

# Installer collection Ansible ACI
ansible-galaxy collection install cisco.aci

# Configurer environnement
cp .env.example .env
```

### RHEL/CentOS/Fedora

```bash
# Installer Python et outils développement
sudo dnf install python3 python3-pip python3-devel git -y
# Pour RHEL/CentOS 7: sudo yum install python3 python3-pip python3-devel git -y

# Cloner et configurer
git clone https://github.com/JFGrenier07/aci-fabric-automation.git
cd aci-fabric-automation

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install pandas openpyxl ansible

# Installer collection ACI
ansible-galaxy collection install cisco.aci

# Configurer environnement
cp .env.example .env
```

## 🍎 Installation macOS

### Utilisation Homebrew (Recommandé)

```bash
# Installer Homebrew si pas déjà installé
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python
brew install python3 git

# Cloner le dépôt
git clone https://github.com/JFGrenier07/aci-fabric-automation.git
cd aci-fabric-automation

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install pandas openpyxl ansible

# Installer collection ACI
ansible-galaxy collection install cisco.aci

# Configurer environnement
cp .env.example .env
```

### Utilisation Installateur Python.org

```bash
# Télécharger et installer Python depuis https://www.python.org/downloads/
# Assurer que "Ajouter Python au PATH" est coché pendant installation

# Ouvrir Terminal et vérifier installation
python3 --version

# Cloner et configurer
git clone https://github.com/JFGrenier07/aci-fabric-automation.git
cd aci-fabric-automation

# Continuer avec configuration environnement virtuel comme ci-dessus
```

## 🪟 Installation Windows

### Utilisation Windows Subsystem pour Linux (WSL2) - Recommandé

```bash
# Installer WSL2 (PowerShell en Administrateur)
wsl --install -d Ubuntu

# Redémarrer ordinateur et ouvrir terminal Ubuntu
# Suivre étapes installation Ubuntu ci-dessus
```

### Utilisation Windows Natif

```powershell
# Installer Python depuis Microsoft Store ou python.org
# Ouvrir PowerShell en Administrateur

# Cloner dépôt
git clone https://github.com/JFGrenier07/aci-fabric-automation.git
cd aci-fabric-automation

# Créer environnement virtuel
python -m venv venv
venv\Scripts\activate

# Installer dépendances
pip install --upgrade pip
pip install pandas openpyxl ansible

# Installer collection ACI
ansible-galaxy collection install cisco.aci

# Configurer environnement
copy .env.example .env
```

## 🐳 Installation Docker

### Utilisation Conteneur Docker

```bash
# Créer Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer collection Ansible ACI
RUN ansible-galaxy collection install cisco.aci

# Copier code application
COPY . .

# Créer répertoires
RUN mkdir -p logs csv

ENTRYPOINT ["python3", "excel_to_csv_simple.py"]
EOF

# Construire conteneur
docker build -t aci-automation .

# Exécuter conteneur
docker run -v $(pwd)/config:/app/config \
           -v $(pwd)/logs:/app/logs \
           -v $(pwd)/csv:/app/csv \
           --env-file .env \
           aci-automation config/votre_fabric.xlsx
```

### Utilisation Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  aci-automation:
    build: .
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./csv:/app/csv
    env_file:
      - .env
    environment:
      - PYTHONUNBUFFERED=1
```

## 📋 Fichier Requirements

Créer `requirements.txt` :

```txt
# Dépendances principales
ansible>=6.0.0
ansible-core>=2.12.0
pandas>=1.3.0
openpyxl>=3.0.0

# Améliorations performance optionnelles
PyYAML>=6.0
Jinja2>=3.0.0
requests>=2.25.0

# Dépendances développement (optionnel)
pytest>=6.0.0
black>=22.0.0
flake8>=4.0.0
```

## ⚙️ Configuration Setup

### 1. Configuration Environnement

```bash
# Copier et éditer fichier environnement
cp .env.example .env

# Éditer avec vos détails APIC
vim .env  # ou nano .env sur certains systèmes
```

**Variables Environnement Requises :**

```bash
# Connexion APIC
ACI_HOSTNAME=votre-apic.entreprise.com
ACI_USERNAME=admin
ACI_PASSWORD=votre_mot_de_passe_securise

# Configuration SSL
ACI_VALIDATE_CERTS=false  # Mettre à true pour production

# Options déploiement
GLOBAL_STATE=present
CSV_DIR=csv

# Paramètres performance
ANSIBLE_TIMEOUT=300
ANSIBLE_FORKS=5
ANSIBLE_GATHERING=explicit
```

### 2. Configuration Ansible

Le `ansible.cfg` inclus est pré-configuré, mais vous pouvez personnaliser :

```ini
[defaults]
inventory = inventory.yml
host_key_checking = False
timeout = 30
gathering = explicit
retry_files_enabled = False
stdout_callback = yaml
result_format = yaml
log_path = logs/ansible.log
verbosity = 2

[inventory]
enable_plugins = yaml, ini
```

### 3. Configuration Inventaire

Éditer `inventory.yml` pour correspondre à votre environnement :

```yaml
---
all:
  hosts:
    localhost:
      ansible_connection: local
  vars:
    # Utiliser variables environnement pour sécurité
    aci_hostname: "{{ lookup('env', 'ACI_HOSTNAME') }}"
    aci_username: "{{ lookup('env', 'ACI_USERNAME') }}"
    aci_password: "{{ lookup('env', 'ACI_PASSWORD') }}"
    aci_validate_certs: "{{ lookup('env', 'ACI_VALIDATE_CERTS') | default(false) | bool }}"
```

## ✅ Vérification Installation

### 1. Vérification Basique

```bash
# Activer environnement virtuel
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Vérifier paquets Python
python3 -c "import pandas, openpyxl, ansible; print('Tous paquets importés avec succès')"

# Vérifier installation Ansible
ansible --version

# Vérifier collection ACI
ansible-galaxy collection list | grep cisco.aci

# Tester syntaxe script
python3 excel_to_csv_simple.py --help
```

### 2. Test Connectivité

```bash
# Tester connectivité APIC (assurer .env configuré)
ansible all -i inventory.yml -m ping

# Tester disponibilité module ACI
ansible-doc cisco.aci.aci_tenant
```

### 3. Test End-to-End

```bash
# Tester avec fichier Excel exemple
python3 excel_to_csv_simple.py aci_fabric_config.xlsx

# Vérifier génération CSV
ls -la csv/

# Tester syntaxe playbook
ansible-playbook --syntax-check aci_fabric_config.yml

# Test dry-run (aucun changement effectué)
ansible-playbook -i inventory.yml aci_fabric_config.yml --check
```

## 🔧 Dépannage Installation

### Problèmes Courants

#### Problèmes Version Python
```bash
# Erreur : Python 3.8+ requis
# Solution : Installer version Python correcte
sudo apt install python3.9 python3.9-venv python3.9-pip
python3.9 -m venv venv
```

#### Erreurs Installation Pandas
```bash
# Erreur : Microsoft Visual C++ requis (Windows)
# Solution : Installer Visual C++ Build Tools
# Télécharger depuis : https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Erreur : Échec construction wheel pour pandas
# Solution : Utiliser conda au lieu de pip
conda install pandas openpyxl
```

#### Problèmes Collection Ansible
```bash
# Erreur : collection cisco.aci non trouvée
# Solution : Réinstaller collection
ansible-galaxy collection install cisco.aci --force

# Vérifier chemin installation
ansible-galaxy collection list --format json | jq '.cisco.aci'
```

#### Problèmes Permissions (Linux/macOS)
```bash
# Erreur : Permission refusée
# Solution : Corriger propriété
sudo chown -R $USER:$USER aci-fabric-automation/
chmod +x excel_to_csv_simple.py
```

### Problèmes Spécifiques Environnement

#### WSL2 sur Windows
```bash
# Problème : Ne peut accéder fichiers Windows
# Solution : Utiliser système fichiers WSL2
cd /home/$USER
git clone https://github.com/JFGrenier07/aci-fabric-automation.git

# Problème : Ansible trop lent
# Solution : Exclure répertoire WSL2 de Windows Defender
# Ajouter répertoire WSL2 aux exclusions Windows Defender
```

#### macOS Catalina/Big Sur
```bash
# Problème : Erreurs certificat SSL
# Solution : Mettre à jour certificats
/Applications/Python\ 3.x/Install\ Certificates.command

# Problème : Outils ligne commande requis
xcode-select --install
```

## 🚀 Déploiement Production

### Durcissement Sécurité

```bash
# Utiliser Ansible Vault pour données sensibles
ansible-vault create vault.yml

# Ajouter variables chiffrées
ansible-vault edit vault.yml

# Mettre à jour inventaire pour utiliser vault
echo "aci_password: !vault |" >> inventory.yml
```

### Optimisation Performance

```bash
# Optimiser pour gros déploiements
export ANSIBLE_FORKS=10
export ANSIBLE_GATHERING=explicit
export ANSIBLE_HOST_KEY_CHECKING=False

# Utiliser connexions persistantes
echo "use_persistent_connections = True" >> ansible.cfg
```

### Configuration Monitoring

```bash
# Activer journalisation structurée
mkdir -p logs
echo "log_path = logs/ansible.log" >> ansible.cfg
echo "stdout_callback = json" >> ansible.cfg

# Configurer rotation logs
sudo tee /etc/logrotate.d/aci-automation << 'EOF'
/chemin/vers/aci-automation/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
```

## 📚 Prochaines Étapes

Après installation réussie :

1. **Configurer Modèle Excel** : Suivre [Guide Modèle Excel](EXCEL_TEMPLATE.fr.md)
2. **Exécuter Premier Déploiement** : Voir [Guide Utilisation](README.fr.md#utilisation)
3. **Configurer Monitoring** : Configurer journalisation et alertes
4. **Planifier Déploiement Production** : Tester d'abord en environnement lab

## 🆘 Obtenir Aide

Si vous rencontrez problèmes pendant installation :

1. **Vérifier Exigences** : Assurer toutes exigences système remplies
2. **Revoir Logs** : Vérifier logs installation et exécution
3. **Chercher Issues** : Parcourir [GitHub Issues](https://github.com/JFGrenier07/aci-fabric-automation/issues)
4. **Demander Aide** : Créer nouvelle issue avec détails installation

**Inclure dans demandes support :**
- Système d'exploitation et version
- Version Python (`python3 --version`)
- Méthode installation utilisée
- Messages erreur complets
- Contenu fichier `.env` (sans mots de passe)