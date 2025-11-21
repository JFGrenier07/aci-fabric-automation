#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Simple : Excel ACI → CSV
Exporte seulement les onglets avec données dans la première colonne
"""

import pandas as pd
import os
import shutil
from pathlib import Path

class ExcelToCSVSimple:
    def __init__(self, excel_file="aci_complete_standardized_fabric.xlsx", csv_dir="csv"):
        self.excel_file = excel_file
        self.csv_dir = Path(csv_dir)
        
        # Onglets système à ignorer
        self.ignore_sheets = {
            'Navigation',  # Onglet d'index
            'Sheet1', 'Sheet2', 'Sheet3',  # Onglets par défaut
            'Template', 'Example', 'README'  # Onglets de documentation
        }
        
    def clean_csv_directory(self):
        """Nettoyer complètement le répertoire CSV"""
        if self.csv_dir.exists():
            print(f"🧹 Nettoyage du répertoire {self.csv_dir}...")
            shutil.rmtree(self.csv_dir)
        
        self.csv_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Répertoire CSV créé/nettoyé: {self.csv_dir}")
    
    def has_real_data(self, sheet_name):
        """Vérifier si la première colonne contient des données (logique simplifiée)"""
        try:
            df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
            
            # Vérifications de base
            if df.empty:
                return False
            
            first_col = df.iloc[:, 0]
            
            # Cas spécial: une seule ligne de données (sans header séparé)
            if len(first_col) == 1:
                value = first_col.iloc[0]
                if pd.notna(value) and str(value).strip():
                    return True
                return False
            
            # Cas normal: chercher des données après le header (ligne 0)
            for i in range(1, len(first_col)):
                value = first_col.iloc[i]
                if pd.notna(value) and str(value).strip():
                    return True
                    
            return False
            
        except Exception as e:
            print(f"⚠️ Erreur lecture '{sheet_name}': {e}")
            return False
    
    def export_sheet_to_csv(self, sheet_name):
        """Exporter un onglet vers CSV"""
        try:
            # Lire l'onglet
            df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
            
            if df.empty:
                print(f"⚠️ Onglet '{sheet_name}' vide")
                return False
            
            # Nom de fichier CSV
            csv_filename = f"{sheet_name}.csv"
            csv_path = self.csv_dir / csv_filename
            
            # Exporter vers CSV
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            # Module ACI correspondant
            module_name = f"aci_{sheet_name}"
            print(f"✅ {sheet_name:<35} → {csv_filename:<40} ({df.shape[0]}x{df.shape[1]}) → {module_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur export '{sheet_name}': {e}")
            return False
    
    def get_excel_sheets(self):
        """Obtenir la liste des onglets Excel"""
        try:
            excel_file = pd.ExcelFile(self.excel_file)
            return excel_file.sheet_names
        except Exception as e:
            print(f"❌ Erreur lecture Excel: {e}")
            return []
    
    def process_all_sheets(self):
        """Traiter tous les onglets avec données dans la première colonne"""
        print("🚀 EXCEL → CSV : Export Simple")
        print("="*80)
        
        # Nettoyer le répertoire CSV
        self.clean_csv_directory()
        
        # Obtenir tous les onglets
        all_sheets = self.get_excel_sheets()
        if not all_sheets:
            print("❌ Aucun onglet trouvé dans le fichier Excel")
            return
            
        print(f"📋 {len(all_sheets)} onglets trouvés dans Excel")
        
        # Statistiques
        exported_count = 0
        skipped_count = 0
        
        print(f"\n🔍 Analyse et export des onglets avec données...")
        print("-"*80)
        
        for sheet_name in all_sheets:
            # Ignorer certains onglets système
            if sheet_name in self.ignore_sheets:
                print(f"⏭️ {sheet_name:<35} → IGNORÉ (onglet système)")
                skipped_count += 1
                continue
            
            # Vérifier si la première colonne a des données
            if not self.has_real_data(sheet_name):
                print(f"⏭️ {sheet_name:<35} → IGNORÉ (pas de données)")
                skipped_count += 1
                continue
            
            # Exporter vers CSV
            if self.export_sheet_to_csv(sheet_name):
                exported_count += 1
        
        # Résumé
        print("\n" + "="*80)
        print("📊 RÉSUMÉ DE L'EXPORT")
        print("="*80)
        print(f"✅ Onglets exportés: {exported_count}")
        print(f"⏭️ Onglets ignorés: {skipped_count}")
        print(f"📁 Fichiers CSV créés dans: {self.csv_dir}/")
        print(f"📋 Total onglets traités: {len(all_sheets)}")
        
        # Lister les fichiers CSV créés
        csv_files = list(self.csv_dir.glob("*.csv"))
        if csv_files:
            print(f"\n📁 Fichiers CSV générés:")
            for csv_file in sorted(csv_files):
                print(f"   • {csv_file.name}")
        
    def create_detected_modules_list(self):
        """Créer la liste des modules ACI détectés"""
        csv_files = list(self.csv_dir.glob("*.csv"))
        
        detected_modules = []
        for csv_file in csv_files:
            sheet_name = csv_file.stem  # Nom sans extension
            module_name = f"aci_{sheet_name}"
            detected_modules.append(module_name)
        
        # Créer le fichier YAML
        detected_file = "detected_modules_csv.yml"
        with open(detected_file, 'w') as f:
            f.write("# Modules ACI détectés depuis les fichiers CSV\n")
            f.write("# Généré automatiquement par excel_to_csv_simple.py\n")
            f.write("detected_modules:\n")
            for module in sorted(detected_modules):
                f.write(f"- {module}\n")
        
        print(f"✅ Liste des modules créée: {detected_file}")
        return detected_modules

    def create_dynamic_playbook(self, excel_file, detected_modules):
        """Créer un playbook Ansible dynamique basé sur les modules détectés"""
        
        # Extraire le nom du fichier Excel sans extension
        excel_name = Path(excel_file).stem
        playbook_name = f"{excel_name}.yml"
        
        print(f"\n🎯 GÉNÉRATION PLAYBOOK DYNAMIQUE")
        print(f"📋 Excel source: {excel_file}")
        print(f"📝 Playbook cible: {playbook_name}")
        print(f"🔧 Modules à inclure: {len(detected_modules)}")
        
        # Ordre d'exécution des modules (infrastructure → tenant → sécurité)
        module_order = [
            # Infrastructure - Ordre critique
            'aci_vlan_pool',
            'aci_vlan_pool_encap_block', 
            'aci_domain',
            'aci_domain_to_vlan_pool',
            'aci_aep',
            'aci_aep_to_domain',
            'aci_switch_policy_vpc_protection_gr',
            
            # Interface Policies
            'aci_interface_policy_cdp',
            'aci_interface_policy_link_level',
            'aci_interface_policy_lldp',
            'aci_interface_policy_mcp',
            'aci_interface_policy_port_channel',
            'aci_interface_policy_spanning_tree',
            'aci_interface_config',
            'aci_interface_policy_leaf_policy_gr',
            
            # Switch and Interface Profiles - Après interface policies
            'aci_switch_policy_leaf_profile',
            'aci_interface_policy_leaf_profile',
            'aci_switch_leaf_selector',
            'aci_int_sel_to_switch_policy_leaf',
            'aci_access_port_to_int_policy_leaf',
            
            # Tenant - Configuration logique
            'aci_tenant',
            'aci_vrf',
            'aci_bd',
            'aci_bd_subnet',
            'aci_bd_to_l3out',
            'aci_ap',
            'aci_epg',
            'aci_aep_to_epg',
            'aci_epg_to_domain',
            
            # BGP Policies - Avant L3Out
            'aci_bgp_timers_policy',
            'aci_bgp_best_path_policy',
            'aci_bgp_address_family_context_policy',
            
            # Security - Contracts et Filters
            'aci_filter',
            'aci_contract',
            'aci_contract_subject',
            'aci_contract_subject_to_filter',
            'aci_epg_to_contract',
            
            # L3Out Configuration
            'aci_l3out',
            'aci_l3out_logical_node_profile',
            'aci_l3out_logical_node',
            'aci_l3out_logical_interface_profile',
            'aci_l3out_interface',
            'aci_l3out_bgp_protocol_profile',
            'aci_l3out_bgp_peer',
            'aci_l3out_floating_svi',
            'aci_l3out_floating_svi_path',
            'aci_l3out_bgp_peer_floating',
            'aci_l3out_extepg',
            'aci_l3out_extsubnet',
            'aci_l3out_extepg_to_contract',
            'aci_l3out_logical_interface_vpc_member',
            'aci_l3out_floating_svi_secondary_ip',
            'aci_l3out_floating_svi_path_secondary_ip',

            # Route Control - Après L3Out
            'aci_match_rule',
            'aci_match_route_destination',
            'aci_route_control_profile',
            'aci_route_control_context'
        ]
        
        # Filtrer seulement les modules détectés dans l'ordre approprié
        ordered_modules = [m for m in module_order if m in detected_modules]
        
        # Créer le contenu du playbook
        playbook_content = f'''---
- name: "Déploiement ACI depuis {excel_name}.xlsx"
  hosts: localhost
  connection: local
  gather_facts: false
  
  vars:
    csv_dir: "csv"
    # Variable globale pour contrôler l'état des objets ACI
    global_state: "{{{{ deployment_state | default('present') }}}}"

  pre_tasks:
    - name: "🎯 Afficher l'action à effectuer"
      debug:
        msg: 
          - "=== ACI AUTOMATION DYNAMIQUE - {excel_name.upper()} ==="
          - "📁 Répertoire CSV: {{{{ csv_dir }}}}/"
          - "🌐 Fabric ACI: {{{{ aci_hostname }}}}"
          - "⚡ Action: {{% if global_state == 'present' %}}DÉPLOIEMENT{{% else %}}SUPPRESSION{{% endif %}} des objets ACI"
          - "📋 Modules détectés: {len(detected_modules)}"
          - "=================================================="

    - name: "Vérifier la présence du répertoire CSV"
      stat:
        path: "{{{{ csv_dir }}}}"
      register: csv_dir_stat
      failed_when: not csv_dir_stat.stat.exists or not csv_dir_stat.stat.isdir

  tasks:'''

        # Ajouter les tâches pour chaque module détecté
        for module in ordered_modules:
            task_name = module.replace('aci_', '')
            
            # Descriptions spécifiques par catégorie
            descriptions = {
                'vlan_pool': 'VLAN Pools',
                'vlan_pool_encap_block': 'VLAN Encap Blocks (onglet séparé)',
                'domain': 'Physical Domains', 
                'domain_to_vlan_pool': 'associations Domain-VLAN Pool (onglet séparé)',
                'aep': 'AEP (Attachable Entity Profiles)',
                'aep_to_domain': 'associations AEP-Domain (onglet séparé)',
                'switch_policy_vpc_protection_gr': 'VPC Protection Groups',
                'switch_policy_leaf_profile': 'Switch Policy Leaf Profiles',
                'interface_policy_leaf_profile': 'Interface Policy Leaf Profiles',
                'switch_leaf_selector': 'Switch Leaf Selectors',
                'int_sel_to_switch_policy_leaf': 'Interface to Switch Policy Associations',
                'access_port_to_int_policy_leaf': 'Access Port to Interface Policy',
                'interface_policy_cdp': 'policies CDP',
                'interface_policy_link_level': 'policies Link Level',
                'interface_policy_lldp': 'policies LLDP',
                'interface_policy_mcp': 'policies MCP',
                'interface_policy_port_channel': 'policies Port Channel',
                'interface_policy_spanning_tree': 'policies Spanning Tree',
                'interface_policy_leaf_policy_gr': 'Leaf Policy Groups',
                'interface_config': 'Interface Configurations',
                'tenant': 'tenants',
                'vrf': 'VRFs',
                'bd': 'Bridge Domains',
                'bd_subnet': 'BD Subnets',
                'bd_to_l3out': 'associations BD to L3Out',
                'ap': 'Application Profiles',
                'epg': 'Endpoint Groups',
                'aep_to_epg': 'associations AEP-EPG',
                'epg_to_domain': 'associations EPG-Domain',
                'bgp_timers_policy': 'BGP Timers Policies',
                'bgp_best_path_policy': 'BGP Best Path Policies',
                'bgp_address_family_context_policy': 'BGP Address Family Context Policies',
                'filter': 'Filters',
                'contract': 'Contracts',
                'contract_subject': 'Subjects',
                'contract_subject_to_filter': 'associations Subject-Filter',
                'epg_to_contract': 'associations EPG-Contract',
                'l3out': 'L3Out',
                'l3out_logical_node_profile': 'L3Out Logical Node Profiles',
                'l3out_logical_node': 'L3Out Logical Nodes',
                'l3out_logical_interface_profile': 'L3Out Logical Interface Profiles',
                'l3out_interface': 'L3Out Interfaces',
                'l3out_bgp_protocol_profile': 'L3Out BGP Protocol Profiles',
                'l3out_bgp_peer': 'L3Out BGP Peers',
                'l3out_floating_svi': 'L3Out Floating SVI',
                'l3out_floating_svi_path': 'L3Out Floating SVI Path',
                'l3out_bgp_peer_floating': 'L3Out BGP Peer Floating',
                'l3out_extepg': 'L3Out External EPGs',
                'l3out_extsubnet': 'L3Out External Subnets',
                'l3out_extepg_to_contract': 'associations L3Out ExtEPG to Contract',
                'l3out_logical_interface_vpc_member': 'L3Out Logical Interface VPC Members',
                'l3out_floating_svi_secondary_ip': 'L3Out Floating SVI Secondary IPs',
                'l3out_floating_svi_path_secondary_ip': 'L3Out Floating SVI Path Secondary IPs'
            }
            
            description = descriptions.get(task_name, task_name)
            
            playbook_content += f'''
    - name: "Inclure les tâches pour les {description}"
      include_tasks: tasks/{task_name}.yml
      tags:
        - {task_name}
        - {module}'''

        # Ajouter les post_tasks
        playbook_content += f'''

  post_tasks:
    - name: "Résumé du déploiement {excel_name}"
      debug:
        msg: 
          - "Déploiement ACI depuis {excel_name}.xlsx terminé"
          - "Modules traités: {detected_modules}"
          - "Nombre total de modules: {len(detected_modules)}"
          - "Source: Fichiers CSV dans {{{{ csv_dir }}}}/"
'''

        # Écrire le fichier playbook
        with open(playbook_name, 'w', encoding='utf-8') as f:
            f.write(playbook_content)
        
        print(f"✅ Playbook dynamique créé: {playbook_name}")
        print(f"📋 Modules inclus dans l'ordre: {ordered_modules}")
        
        return playbook_name

def main():
    """Fonction principale"""
    import sys
    
    print("🎯 Excel ACI → CSV Simple Export")
    print("="*60)
    
    # Vérifier les paramètres - OBLIGATOIRE pour la sécurité
    if len(sys.argv) < 2:
        print("❌ ERREUR: Fichier Excel obligatoire pour éviter les déploiements accidentels")
        print("💡 Usage: python3 excel_to_csv_simple.py fichier.xlsx")
        print("🔒 Sécurité: Aucun fichier par défaut pour éviter les catastrophes")
        return
        
    excel_file = sys.argv[1]
    print(f"📁 Fichier Excel spécifié: {excel_file}")
    
    # Vérifier que le fichier Excel existe
    if not os.path.exists(excel_file):
        print(f"❌ Fichier Excel non trouvé: {excel_file}")
        print("💡 Usage: python3 excel_to_csv_simple.py fichier.xlsx")
        print("🔍 Vérifiez que le fichier existe dans le répertoire courant")
        return
    
    print(f"✅ Fichier Excel trouvé: {excel_file}")
    
    # Initialiser l'exporteur
    exporter = ExcelToCSVSimple(excel_file, "csv")
    
    # Traiter tous les onglets
    exporter.process_all_sheets()
    
    # Créer la liste des modules détectés
    detected_modules = exporter.create_detected_modules_list()
    
    # Créer le playbook dynamique
    playbook_name = exporter.create_dynamic_playbook(excel_file, detected_modules)
    
    print(f"\n🎯 Export terminé! {len(detected_modules)} modules ACI détectés.")
    print(f"🚀 Playbook dynamique créé: {playbook_name}")
    print("💡 Prêt pour le déploiement Ansible ultra-propre (0 SKIPPED)!")

if __name__ == "__main__":
    main()