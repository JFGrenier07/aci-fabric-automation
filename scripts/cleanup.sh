#!/bin/bash
# Script de nettoyage pour le projet ACI Fabric Automation
# Usage: ./scripts/cleanup.sh [--all|--csv|--logs|--temp]

set -e

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher l'aide
show_help() {
    echo -e "${BLUE}Script de nettoyage ACI Fabric Automation${NC}"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --all     Nettoyer tous les fichiers générés"
    echo "  --csv     Nettoyer seulement les fichiers CSV"
    echo "  --logs    Nettoyer seulement les logs"
    echo "  --temp    Nettoyer les fichiers temporaires"
    echo "  --help    Afficher cette aide"
    echo ""
    echo "Sans option, affiche l'état actuel des fichiers"
}

# Fonction pour nettoyer les CSV
cleanup_csv() {
    echo -e "${YELLOW}🧹 Nettoyage des fichiers CSV...${NC}"
    if [ -d "csv" ]; then
        find csv/ -name "*.csv" -type f -delete 2>/dev/null || true
        echo -e "${GREEN}✅ Fichiers CSV supprimés${NC}"
    else
        echo -e "${BLUE}ℹ️  Répertoire csv/ n'existe pas${NC}"
    fi

    # Supprimer le fichier modules détectés s'il existe
    if [ -f "detected_modules_csv.yml" ]; then
        rm -f detected_modules_csv.yml
        echo -e "${GREEN}✅ detected_modules_csv.yml supprimé${NC}"
    fi

    # Supprimer playbooks générés dynamiquement
    find . -maxdepth 1 -name "*_fabric_config.yml" -type f -delete 2>/dev/null || true
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Playbooks dynamiques supprimés${NC}"
    fi
}

# Fonction pour nettoyer les logs
cleanup_logs() {
    echo -e "${YELLOW}🧹 Nettoyage des logs...${NC}"
    if [ -d "logs" ]; then
        find logs/ -name "*.log" -type f -delete 2>/dev/null || true
        echo -e "${GREEN}✅ Fichiers logs supprimés${NC}"
    else
        echo -e "${BLUE}ℹ️  Répertoire logs/ n'existe pas${NC}"
    fi
}

# Fonction pour nettoyer fichiers temporaires
cleanup_temp() {
    echo -e "${YELLOW}🧹 Nettoyage des fichiers temporaires...${NC}"

    # Fichiers temporaires Python
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -type f -delete 2>/dev/null || true
    find . -name "*.pyo" -type f -delete 2>/dev/null || true
    find . -name "*.pyd" -type f -delete 2>/dev/null || true

    # Fichiers temporaires système
    find . -name ".DS_Store" -type f -delete 2>/dev/null || true
    find . -name "Thumbs.db" -type f -delete 2>/dev/null || true
    find . -name "*.tmp" -type f -delete 2>/dev/null || true
    find . -name "*.temp" -type f -delete 2>/dev/null || true
    find . -name "*~" -type f -delete 2>/dev/null || true

    # Fichiers lock Excel
    find . -name ".~lock.*" -type f -delete 2>/dev/null || true
    find . -name "~$*.xlsx" -type f -delete 2>/dev/null || true

    # Fichiers backup
    find . -name "*.bak" -type f -delete 2>/dev/null || true
    find . -name "*.backup" -type f -delete 2>/dev/null || true
    find . -name "*_backup_*" -type f -delete 2>/dev/null || true

    # Fichiers Ansible temporaires
    find . -name "*.retry" -type f -delete 2>/dev/null || true

    echo -e "${GREEN}✅ Fichiers temporaires supprimés${NC}"
}

# Fonction pour afficher l'état
show_status() {
    echo -e "${BLUE}📊 État actuel du projet:${NC}"
    echo ""

    # Compter fichiers CSV
    csv_count=$(find csv/ -name "*.csv" -type f 2>/dev/null | wc -l)
    echo -e "📁 Fichiers CSV: ${csv_count}"

    # Compter fichiers logs
    log_count=$(find logs/ -name "*.log" -type f 2>/dev/null | wc -l)
    echo -e "📋 Fichiers logs: ${log_count}"

    # Vérifier playbooks générés
    playbook_count=$(find . -maxdepth 1 -name "*_fabric_config.yml" -type f 2>/dev/null | wc -l)
    echo -e "🎭 Playbooks générés: ${playbook_count}"

    # Vérifier fichiers temporaires
    temp_count=$(find . \( -name "*.tmp" -o -name "*.temp" -o -name "*~" -o -name "*.pyc" \) -type f 2>/dev/null | wc -l)
    echo -e "🗑️  Fichiers temporaires: ${temp_count}"

    # Vérifier detected_modules_csv.yml
    if [ -f "detected_modules_csv.yml" ]; then
        echo -e "🔍 detected_modules_csv.yml: ${GREEN}Présent${NC}"
    else
        echo -e "🔍 detected_modules_csv.yml: ${YELLOW}Absent${NC}"
    fi

    echo ""
    echo -e "${BLUE}💡 Utilisez $0 --help pour voir les options de nettoyage${NC}"
}

# Script principal
case "${1:-}" in
    --all)
        echo -e "${BLUE}🚀 Nettoyage complet...${NC}"
        cleanup_csv
        cleanup_logs
        cleanup_temp
        echo -e "${GREEN}✨ Nettoyage complet terminé!${NC}"
        ;;
    --csv)
        cleanup_csv
        ;;
    --logs)
        cleanup_logs
        ;;
    --temp)
        cleanup_temp
        ;;
    --help|-h)
        show_help
        ;;
    "")
        show_status
        ;;
    *)
        echo -e "${RED}❌ Option inconnue: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac