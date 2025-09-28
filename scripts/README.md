# 🛠️ Scripts Utilitaires

Ce répertoire contient des scripts utilitaires pour la maintenance et l'administration du projet ACI Fabric Automation.

## 📜 Scripts Disponibles

### `cleanup.sh` - Script de Nettoyage

Script automatisé pour nettoyer les fichiers générés et temporaires.

**Usage :**
```bash
# Afficher l'état actuel
./scripts/cleanup.sh

# Nettoyage complet
./scripts/cleanup.sh --all

# Nettoyage sélectif
./scripts/cleanup.sh --csv     # Seulement les CSV
./scripts/cleanup.sh --logs    # Seulement les logs
./scripts/cleanup.sh --temp    # Seulement les fichiers temporaires

# Aide
./scripts/cleanup.sh --help
```

**Fonctionnalités :**
- 🧹 Supprime fichiers CSV générés
- 📋 Nettoie logs Ansible
- 🗑️ Supprime fichiers temporaires système
- 🎭 Efface playbooks générés dynamiquement
- 📊 Affiche statistiques avant/après nettoyage

**Sécurité :**
- Ne supprime jamais les fichiers source
- Préserve la configuration et documentation
- Mode dry-run par défaut (affichage statut)

## 🚀 Utilisation Recommandée

### Avant Commit Git
```bash
# Nettoyer avant commit
./scripts/cleanup.sh --temp
git add .
git commit -m "feat: nouvelle fonctionnalité"
```

### Après Tests
```bash
# Nettoyer après tests
./scripts/cleanup.sh --csv --logs
```

### Maintenance Générale
```bash
# Nettoyage complet hebdomadaire
./scripts/cleanup.sh --all
```

## 🔒 Fichiers Protégés

Le script **ne supprime jamais** :
- Documentation (*.md)
- Configuration (ansible.cfg, inventory.yml, .env*)
- Scripts source (*.py)
- Tâches Ansible (tasks/*.yml)
- Modèles Excel originaux
- Fichiers Git (.git/, .gitignore)

## 📈 Extension

Pour ajouter de nouveaux scripts :

1. Créer le script dans `scripts/`
2. Le rendre exécutable : `chmod +x scripts/monscript.sh`
3. Documenter l'usage dans ce README
4. Ajouter au .gitignore si nécessaire