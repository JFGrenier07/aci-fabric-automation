# 📊 Documentation Modèle Excel

Ce document fournit des conseils complets pour créer et maintenir des fichiers de configuration Excel pour le Moteur d'Automatisation ACI Fabric.

## 🎯 Aperçu

Le modèle Excel sert de **source unique de vérité** pour votre configuration fabric ACI. Chaque feuille Excel correspond à un type d'objet ACI spécifique, avec les en-têtes de colonnes définissant les attributs de l'objet.

## 📋 Règles et Conventions Générales

### ✅ Exigences Nommage

**Noms Feuilles** (Sensible à la Casse) :
- Doivent correspondre exactement comme spécifié dans ce document
- Aucun espace, caractère spécial ou variation autorisé
- Exemples : ✅ `vlan_pool` ❌ `vlan_pools`, `VLAN_Pool`

**Noms Objets** :
- Utiliser uniquement caractères alphanumériques et underscores
- Commencer par lettre ou underscore
- Maximum 64 caractères
- Exemples : ✅ `Prod_VLAN_Pool` ❌ `Prod VLAN Pool`, `Prod-VLAN-Pool`

**En-têtes Colonnes** :
- Doivent correspondre exactement comme spécifié
- Sensible à la casse et ordre indépendant
- Colonnes requises manquantes causeront erreurs validation

### 📊 Exigences Format Données

- **Champs Texte** : Texte simple, pas formatage spécial
- **Champs Numériques** : Valeurs entières où spécifié
- **Champs Booléens** : Utiliser `true`/`false` ou `yes`/`no`
- **Champs Optionnels** : Peuvent être laissés vides
- **Pas Formule** : Utiliser valeurs simples seulement, pas formules Excel

## 🏗️ Objets Infrastructure

### Configuration Pool VLAN

**Nom Feuille** : `vlan_pool`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `pool` | String | Nom pool VLAN | `Prod_VLAN_Pool` |
| `description` | String | Description pool | `Pool VLAN Production` |
| `pool_allocation_mode` | String | `static` ou `dynamic` | `static` |

**Exemple** :
```excel
pool,description,pool_allocation_mode
Prod_VLAN_Pool,Pool VLAN Production,static
Dev_VLAN_Pool,Pool VLAN Développement,dynamic
DMZ_VLAN_Pool,Pool VLAN DMZ,static
Mgmt_VLAN_Pool,Pool VLAN gestion,static
```

### Blocs Encapsulation Pool VLAN

**Nom Feuille** : `vlan_pool_encap_block`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `pool` | String | Nom pool VLAN (doit exister) | `Prod_VLAN_Pool` |
| `block_name` | String | Nom bloc encap | `Prod_Block_100-199` |
| `from` | Integer | ID VLAN début | `100` |
| `to` | Integer | ID VLAN fin | `199` |
| `alloc_mode` | String | `static` ou `dynamic` | `static` |

**Exemple** :
```excel
pool,block_name,from,to,alloc_mode,description
Prod_VLAN_Pool,Prod_Block_100-199,100,199,static,Plage VLAN production
Dev_VLAN_Pool,Dev_Block_200-299,200,299,dynamic,Plage VLAN développement
DMZ_VLAN_Pool,DMZ_Block_300-349,300,349,static,Plage VLAN DMZ
```

### Domaines Physiques

**Nom Feuille** : `domain`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `domain` | String | Nom domaine | `Prod_PhysDom` |
| `domain_type` | String | Toujours `phys` pour physique | `phys` |
| `description` | String | Description domaine | `Domaine Physique Production` |

**Exemple** :
```excel
domain,domain_type,description
Prod_PhysDom,phys,Domaine Physique Production
Dev_PhysDom,phys,Domaine Physique Développement
DMZ_PhysDom,phys,Domaine Physique DMZ
```

### Associations Domaine vers Pool VLAN

**Nom Feuille** : `domain_to_vlan_pool`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `domain` | String | Nom domaine (doit exister) | `Prod_PhysDom` |
| `pool` | String | Nom pool VLAN (doit exister) | `Prod_VLAN_Pool` |
| `pool_allocation_mode` | String | `static` ou `dynamic` | `static` |

**Exemple** :
```excel
domain,pool,pool_allocation_mode
Prod_PhysDom,Prod_VLAN_Pool,static
Dev_PhysDom,Dev_VLAN_Pool,dynamic
DMZ_PhysDom,DMZ_VLAN_Pool,static
```

### Profils Entités Attachables (AEP)

**Nom Feuille** : `aep`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `aep` | String | Nom AEP | `Server_AEP` |
| `description` | String | Description AEP | `Profil connectivité serveur` |

**Exemple** :
```excel
aep,description
Server_AEP,Profil connectivité serveur
Storage_AEP,Profil connectivité stockage
Network_AEP,Connectivité équipement réseau
Management_AEP,Connectivité interface gestion
```

### Associations AEP vers Domaine

**Nom Feuille** : `aep_to_domain`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `aep` | String | Nom AEP (doit exister) | `Server_AEP` |
| `domain` | String | Nom domaine (doit exister) | `Prod_PhysDom` |

**Exemple** :
```excel
aep,domain
Server_AEP,Prod_PhysDom
Server_AEP,Dev_PhysDom
Storage_AEP,Prod_PhysDom
Management_AEP,Mgmt_PhysDom
```

## 🔌 Objets Politique Interface

### Politique CDP

**Nom Feuille** : `interface_policy_cdp`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `cdp_policy` | String | Nom politique CDP | `CDP_Enabled` |
| `admin_state` | String | `enabled` ou `disabled` | `enabled` |
| `description` | String | Description politique | `Politique CDP activée` |

**Exemple** :
```excel
cdp_policy,admin_state,description
CDP_Enabled,enabled,Politique CDP activée
CDP_Disabled,disabled,Politique CDP désactivée
```

### Politique Link Level

**Nom Feuille** : `interface_policy_link_level`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `link_level_policy` | String | Nom politique | `1G_Auto` |
| `speed` | String | Vitesse interface | `1G` |
| `auto_negotiation` | String | `on` ou `off` | `on` |
| `description` | String | Description politique | `1 Gigabit auto-négociation` |

**Exemple** :
```excel
link_level_policy,speed,auto_negotiation,description
1G_Auto,1G,on,1 Gigabit auto-négociation
10G_Auto,10G,on,10 Gigabit auto-négociation
100M_Fixed,100M,off,100 Megabit fixe
```

### Politique LLDP

**Nom Feuille** : `interface_policy_lldp`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `lldp_policy` | String | Nom politique LLDP | `LLDP_Enabled` |
| `receive_state` | String | `enabled` ou `disabled` | `enabled` |
| `transmit_state` | String | `enabled` ou `disabled` | `enabled` |
| `description` | String | Description politique | `LLDP activé bidirectionnel` |

**Exemple** :
```excel
lldp_policy,receive_state,transmit_state,description
LLDP_Enabled,enabled,enabled,LLDP activé bidirectionnel
LLDP_RxOnly,enabled,disabled,LLDP réception seulement
LLDP_Disabled,disabled,disabled,LLDP complètement désactivé
```

## 🏢 Objets Tenant

### Tenants

**Nom Feuille** : `tenant`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `tenant` | String | Nom tenant | `Production` |
| `description` | String | Description tenant | `Environnement production` |

**Exemple** :
```excel
tenant,description
Production,Environnement production
Development,Environnement développement
DMZ,Tenant services DMZ
Common,Tenant services partagés
```

### Contextes VRF

**Nom Feuille** : `vrf`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `vrf` | String | Nom VRF | `Prod_VRF` |
| `description` | String | Description VRF | `Contexte VRF production` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `policy_control_preference` | String | `enforced` ou `unenforced` | `enforced` |
| `policy_control_direction` | String | `ingress` ou `egress` | `ingress` |

**Exemple** :
```excel
tenant,vrf,description,policy_control_preference
Production,Prod_VRF,Contexte VRF production,enforced
Development,Dev_VRF,Contexte VRF développement,unenforced
DMZ,DMZ_VRF,Contexte VRF DMZ,enforced
Common,Shared_VRF,VRF services partagés,enforced
```

### Domaines Diffusion

**Nom Feuille** : `bd`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `bd` | String | Nom domaine diffusion | `Web_BD` |
| `vrf` | String | Nom VRF (doit exister) | `Prod_VRF` |
| `description` | String | Description BD | `Domaine diffusion niveau web` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `enable_routing` | String | `yes` ou `no` | `yes` |
| `arp_flooding` | String | `yes` ou `no` | `no` |
| `l2_unknown_unicast` | String | `proxy` ou `flood` | `proxy` |

**Exemple** :
```excel
tenant,bd,vrf,description,enable_routing,arp_flooding
Production,Web_BD,Prod_VRF,Domaine diffusion niveau web,yes,no
Production,App_BD,Prod_VRF,Domaine diffusion niveau application,yes,no
Production,DB_BD,Prod_VRF,Domaine diffusion niveau base données,yes,no
Development,Dev_BD,Dev_VRF,Domaine diffusion développement,yes,yes
```

### Sous-réseaux Domaine Diffusion

**Nom Feuille** : `bd_subnet`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `bd` | String | Nom domaine diffusion (doit exister) | `Web_BD` |
| `subnet` | String | CIDR sous-réseau | `10.1.1.1/24` |
| `description` | String | Description sous-réseau | `Sous-réseau niveau web` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `scope` | String | `private`, `public`, ou `shared` | `private` |
| `subnet_control` | String | `nd_ra`, `no_gw`, `querier_ip` | - |

**Exemple** :
```excel
tenant,bd,subnet,description,scope
Production,Web_BD,10.1.1.1/24,Sous-réseau niveau web,private
Production,App_BD,10.1.2.1/24,Sous-réseau niveau application,private
Production,DB_BD,10.1.3.1/24,Sous-réseau niveau base données,private
Development,Dev_BD,10.2.1.1/24,Sous-réseau développement,private
```

### Profils Application

**Nom Feuille** : `ap`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `ap` | String | Nom profil application | `WebApp_AP` |
| `description` | String | Description AP | `Profil application web` |

**Exemple** :
```excel
tenant,ap,description
Production,WebApp_AP,Profil application web
Production,ERP_AP,Profil application ERP
Production,Database_AP,Profil application base données
Development,DevApp_AP,Profil application développement
```

### Groupes Endpoints (EPG)

**Nom Feuille** : `epg`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `epg` | String | Nom EPG | `WebServers_EPG` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `ap` | String | Profil application (doit exister) | `WebApp_AP` |
| `bd` | String | Domaine diffusion (doit exister) | `Web_BD` |
| `description` | String | Description EPG | `Groupe endpoints serveurs web` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `preferred_group` | String | `yes` ou `no` | `no` |
| `intra_epg_isolation` | String | `enforced` ou `unenforced` | `unenforced` |

**Exemple** :
```excel
epg,tenant,ap,bd,description,preferred_group
WebServers_EPG,Production,WebApp_AP,Web_BD,Groupe endpoints serveurs web,no
AppServers_EPG,Production,ERP_AP,App_BD,EPG serveurs application,no
DBServers_EPG,Production,Database_AP,DB_BD,EPG serveurs base données,yes
DevWeb_EPG,Development,DevApp_AP,Dev_BD,EPG web développement,no
```

## 🔒 Objets Sécurité

### Filtres

**Nom Feuille** : `filter`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `filter` | String | Nom filtre | `Web_Filter` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `entry` | String | Nom entrée filtre | `HTTP` |
| `ethertype` | String | `ip`, `arp`, etc. | `ip` |
| `ip_protocol` | String | `tcp`, `udp`, `icmp` | `tcp` |
| `dst_port_start` | Integer | Port destination début | `80` |
| `dst_port_end` | Integer | Port destination fin | `80` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `src_port_start` | Integer | Port source début | `unspecified` |
| `src_port_end` | Integer | Port source fin | `unspecified` |
| `stateful` | String | `yes` ou `no` | `yes` |

**Exemple** :
```excel
filter,tenant,entry,ethertype,ip_protocol,dst_port_start,dst_port_end,description
Web_Filter,Production,HTTP,ip,tcp,80,80,Trafic HTTP
Web_Filter,Production,HTTPS,ip,tcp,443,443,Trafic HTTPS
App_Filter,Production,Custom_App,ip,tcp,8080,8080,Application personnalisée
DB_Filter,Production,MySQL,ip,tcp,3306,3306,Base données MySQL
```

### Contrats

**Nom Feuille** : `contract`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `contract` | String | Nom contrat | `Web_Contract` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `description` | String | Description contrat | `Contrat accès serveur web` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `scope` | String | `context`, `global`, `tenant` | `context` |
| `priority` | String | `unspecified`, `level1`, `level2`, `level3` | `unspecified` |

**Exemple** :
```excel
contract,tenant,description,scope
Web_Contract,Production,Contrat accès serveur web,context
App_Contract,Production,Contrat serveur application,context
DB_Contract,Production,Contrat accès base données,context
Common_Contract,Production,Contrat services communs,tenant
```

### Sujets Contrat

**Nom Feuille** : `contract_subject`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `contract` | String | Nom contrat (doit exister) | `Web_Contract` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `subject` | String | Nom sujet | `Web_Subject` |
| `description` | String | Description sujet | `Sujet trafic web` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `reverse_filter` | String | `yes` ou `no` | `yes` |
| `priority` | String | `unspecified`, `level1`, `level2`, `level3` | `unspecified` |

**Exemple** :
```excel
contract,tenant,subject,description,reverse_filter
Web_Contract,Production,Web_Subject,Sujet trafic web,yes
App_Contract,Production,App_Subject,Sujet trafic application,yes
DB_Contract,Production,DB_Subject,Sujet trafic base données,yes
```

### Associations Sujet Contrat vers Filtre

**Nom Feuille** : `contract_subject_to_filter`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `contract` | String | Nom contrat (doit exister) | `Web_Contract` |
| `subject` | String | Nom sujet (doit exister) | `Web_Subject` |
| `filter` | String | Nom filtre (doit exister) | `Web_Filter` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |

**Exemple** :
```excel
contract,subject,filter,tenant
Web_Contract,Web_Subject,Web_Filter,Production
App_Contract,App_Subject,App_Filter,Production
DB_Contract,DB_Subject,DB_Filter,Production
```

### Associations EPG vers Contrat

**Nom Feuille** : `epg_to_contract`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `epg` | String | Nom EPG (doit exister) | `WebServers_EPG` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `ap` | String | Profil application (doit exister) | `WebApp_AP` |
| `contract` | String | Nom contrat (doit exister) | `Web_Contract` |
| `contract_type` | String | `provider` ou `consumer` | `provider` |

**Exemple** :
```excel
epg,tenant,ap,contract,contract_type
WebServers_EPG,Production,WebApp_AP,Web_Contract,provider
AppServers_EPG,Production,ERP_AP,Web_Contract,consumer
AppServers_EPG,Production,ERP_AP,DB_Contract,consumer
DBServers_EPG,Production,Database_AP,DB_Contract,provider
```

## 🌐 Objets L3Out

### Configuration L3Out

**Nom Feuille** : `l3out`

**Colonnes Requises** :
| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `l3out` | String | Nom L3Out | `Internet_L3Out` |
| `tenant` | String | Nom tenant (doit exister) | `Production` |
| `vrf` | String | Nom VRF (doit exister) | `Prod_VRF` |
| `domain` | String | Nom domaine L3 | `L3_Domain` |
| `description` | String | Description L3Out | `Connectivité Internet` |

**Colonnes Optionnelles** :
| Colonne | Type | Description | Défaut |
|---------|------|-------------|--------|
| `route_control` | String | Contrôle route | - |
| `dscp` | String | Marquage DSCP | `unspecified` |

**Exemple** :
```excel
l3out,tenant,vrf,domain,description
Internet_L3Out,Production,Prod_VRF,L3_Domain,Connectivité Internet
Partner_L3Out,Production,Prod_VRF,L3_Domain,Connectivité réseau partenaire
MPLS_L3Out,Production,Prod_VRF,L3_Domain,Connectivité WAN MPLS
```

## 📝 Règles Validation

### Intégrité Données
- **Clés Étrangères** : Objets référencés doivent exister dans leurs feuilles respectives
- **Noms Uniques** : Noms objets doivent être uniques dans leur portée
- **Champs Requis** : Toutes colonnes requises doivent avoir valeurs
- **Types Données** : Valeurs doivent correspondre aux types données attendus

### Contraintes ACI
- **Nommage** : Suivre conventions nommage ACI (pas espaces, caractères spéciaux)
- **Dépendances** : Respecter hiérarchie objets ACI (Tenant → VRF → BD → EPG)
- **Limites** : Rester dans limites plateforme ACI (ex. 4000 VLANs par pool)

### Format Excel
- **Type Fichier** : Utiliser format .xlsx seulement
- **Noms Feuilles** : Correspondance exacte sensible à la casse requise
- **Pas Formules** : Utiliser valeurs texte simple seulement
- **Pas Formatage** : Éviter formatage cellule spécial

## 🔍 Dépannage

### Erreurs Courantes

#### Nom Feuille Incorrect
```
Erreur : Feuille 'vlans' non trouvée
Solution : Utiliser nom exact 'vlan_pool'
```

#### Colonnes Requises Manquantes
```
Erreur : Colonne requise 'tenant' manquante dans feuille 'vrf'
Solution : Ajouter en-tête colonne 'tenant'
```

#### Références Invalides
```
Erreur : VRF 'MonVRF' non trouvé pour BD 'MonBD'
Solution : Assurer VRF existe dans feuille 'vrf'
```

#### Erreurs Type Données
```
Erreur : Valeur entier invalide 'abc' dans colonne 'from'
Solution : Utiliser valeurs numériques pour IDs VLAN
```

### Meilleures Pratiques

1. **Commencer Simple** : Débuter avec objets de base (tenant, VRF, BD)
2. **Valider Tôt** : Tester petites configurations d'abord
3. **Utiliser Nommage Cohérent** : Établir conventions nommage
4. **Documenter Dépendances** : Comprendre relations objets
5. **Contrôle Version** : Garder fichiers Excel sous contrôle version
6. **Tester Incrémentalement** : Ajouter objets graduellement

## 📚 Références

- **Modèle Objet ACI** : [Cisco ACI Management Information Model](https://developer.cisco.com/docs/apic-mim-ref/)
- **Collection Ansible ACI** : [Documentation cisco.aci](https://docs.ansible.com/ansible/latest/collections/cisco/aci/)
- **Meilleures Pratiques ACI** : [Guide Conception Cisco ACI](https://www.cisco.com/c/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/white-paper-c11-737909.html)