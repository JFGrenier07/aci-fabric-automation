# 📊 Excel Template Documentation

This document provides comprehensive guidance for creating and maintaining Excel configuration files for the ACI Fabric Automation Engine.

## 🎯 Overview

The Excel template serves as the **single source of truth** for your ACI fabric configuration. Each Excel sheet corresponds to a specific ACI object type, with column headers defining the object attributes.

## 📋 General Rules and Conventions

### ✅ Naming Requirements

**Sheet Names** (Case-Sensitive):
- Must match exactly as specified in this document
- No spaces, special characters, or variations allowed
- Examples: ✅ `vlan_pool` ❌ `vlan_pools`, `VLAN_Pool`

**Object Names**:
- Use alphanumeric characters and underscores only
- Start with letter or underscore
- Maximum 64 characters
- Examples: ✅ `Prod_VLAN_Pool` ❌ `Prod VLAN Pool`, `Prod-VLAN-Pool`

**Column Headers**:
- Must match exactly as specified
- Case-sensitive and order-independent
- Missing required columns will cause validation errors

### 📊 Data Format Requirements

- **Text Fields**: Plain text, no special formatting
- **Numeric Fields**: Integer values where specified
- **Boolean Fields**: Use `true`/`false` or `yes`/`no`
- **Optional Fields**: Can be left empty
- **No Formula**: Use plain values only, no Excel formulas

## 🏗️ Infrastructure Objects

### VLAN Pool Configuration

**Sheet Name**: `vlan_pool`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `pool` | String | VLAN pool name | `Prod_VLAN_Pool` |
| `description` | String | Pool description | `Production VLAN Pool` |
| `pool_allocation_mode` | String | `static` or `dynamic` | `static` |

**Example**:
```excel
pool,description,pool_allocation_mode
Prod_VLAN_Pool,Production VLAN Pool,static
Dev_VLAN_Pool,Development VLAN Pool,dynamic
DMZ_VLAN_Pool,DMZ VLAN Pool,static
Mgmt_VLAN_Pool,Management VLAN Pool,static
```

### VLAN Pool Encapsulation Blocks

**Sheet Name**: `vlan_pool_encap_block`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `pool` | String | VLAN pool name (must exist) | `Prod_VLAN_Pool` |
| `block_name` | String | Encap block name | `Prod_Block_100-199` |
| `from` | Integer | Starting VLAN ID | `100` |
| `to` | Integer | Ending VLAN ID | `199` |
| `alloc_mode` | String | `static` or `dynamic` | `static` |

**Example**:
```excel
pool,block_name,from,to,alloc_mode,description
Prod_VLAN_Pool,Prod_Block_100-199,100,199,static,Production VLAN range
Dev_VLAN_Pool,Dev_Block_200-299,200,299,dynamic,Development VLAN range
DMZ_VLAN_Pool,DMZ_Block_300-349,300,349,static,DMZ VLAN range
```

### Physical Domains

**Sheet Name**: `domain`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `domain` | String | Domain name | `Prod_PhysDom` |
| `domain_type` | String | Always `phys` for physical | `phys` |
| `description` | String | Domain description | `Production Physical Domain` |

**Example**:
```excel
domain,domain_type,description
Prod_PhysDom,phys,Production Physical Domain
Dev_PhysDom,phys,Development Physical Domain
DMZ_PhysDom,phys,DMZ Physical Domain
```

### Domain to VLAN Pool Associations

**Sheet Name**: `domain_to_vlan_pool`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `domain` | String | Domain name (must exist) | `Prod_PhysDom` |
| `pool` | String | VLAN pool name (must exist) | `Prod_VLAN_Pool` |
| `pool_allocation_mode` | String | `static` or `dynamic` | `static` |

**Example**:
```excel
domain,pool,pool_allocation_mode
Prod_PhysDom,Prod_VLAN_Pool,static
Dev_PhysDom,Dev_VLAN_Pool,dynamic
DMZ_PhysDom,DMZ_VLAN_Pool,static
```

### Attachable Entity Profiles (AEP)

**Sheet Name**: `aep`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `aep` | String | AEP name | `Server_AEP` |
| `description` | String | AEP description | `Server connectivity profile` |

**Example**:
```excel
aep,description
Server_AEP,Server connectivity profile
Storage_AEP,Storage connectivity profile
Network_AEP,Network device connectivity
Management_AEP,Management interface connectivity
```

### AEP to Domain Associations

**Sheet Name**: `aep_to_domain`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `aep` | String | AEP name (must exist) | `Server_AEP` |
| `domain` | String | Domain name (must exist) | `Prod_PhysDom` |

**Example**:
```excel
aep,domain
Server_AEP,Prod_PhysDom
Server_AEP,Dev_PhysDom
Storage_AEP,Prod_PhysDom
Management_AEP,Mgmt_PhysDom
```

## 🔌 Interface Policy Objects

### CDP Policy

**Sheet Name**: `interface_policy_cdp`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `cdp_policy` | String | CDP policy name | `CDP_Enabled` |
| `admin_state` | String | `enabled` or `disabled` | `enabled` |
| `description` | String | Policy description | `CDP enabled policy` |

**Example**:
```excel
cdp_policy,admin_state,description
CDP_Enabled,enabled,CDP enabled policy
CDP_Disabled,disabled,CDP disabled policy
```

### Link Level Policy

**Sheet Name**: `interface_policy_link_level`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `link_level_policy` | String | Policy name | `1G_Auto` |
| `speed` | String | Interface speed | `1G` |
| `auto_negotiation` | String | `on` or `off` | `on` |
| `description` | String | Policy description | `1 Gigabit auto-negotiation` |

**Example**:
```excel
link_level_policy,speed,auto_negotiation,description
1G_Auto,1G,on,1 Gigabit auto-negotiation
10G_Auto,10G,on,10 Gigabit auto-negotiation
100M_Fixed,100M,off,100 Megabit fixed
```

### LLDP Policy

**Sheet Name**: `interface_policy_lldp`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `lldp_policy` | String | LLDP policy name | `LLDP_Enabled` |
| `receive_state` | String | `enabled` or `disabled` | `enabled` |
| `transmit_state` | String | `enabled` or `disabled` | `enabled` |
| `description` | String | Policy description | `LLDP enabled both ways` |

**Example**:
```excel
lldp_policy,receive_state,transmit_state,description
LLDP_Enabled,enabled,enabled,LLDP enabled both ways
LLDP_RxOnly,enabled,disabled,LLDP receive only
LLDP_Disabled,disabled,disabled,LLDP completely disabled
```

## 🏢 Tenant Objects

### Tenants

**Sheet Name**: `tenant`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tenant` | String | Tenant name | `Production` |
| `description` | String | Tenant description | `Production environment` |

**Example**:
```excel
tenant,description
Production,Production environment
Development,Development environment
DMZ,DMZ services tenant
Common,Shared services tenant
```

### VRF Contexts

**Sheet Name**: `vrf`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tenant` | String | Tenant name (must exist) | `Production` |
| `vrf` | String | VRF name | `Prod_VRF` |
| `description` | String | VRF description | `Production VRF context` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `policy_control_preference` | String | `enforced` or `unenforced` | `enforced` |
| `policy_control_direction` | String | `ingress` or `egress` | `ingress` |

**Example**:
```excel
tenant,vrf,description,policy_control_preference
Production,Prod_VRF,Production VRF context,enforced
Development,Dev_VRF,Development VRF context,unenforced
DMZ,DMZ_VRF,DMZ VRF context,enforced
Common,Shared_VRF,Shared services VRF,enforced
```

### Bridge Domains

**Sheet Name**: `bd`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tenant` | String | Tenant name (must exist) | `Production` |
| `bd` | String | Bridge domain name | `Web_BD` |
| `vrf` | String | VRF name (must exist) | `Prod_VRF` |
| `description` | String | BD description | `Web tier bridge domain` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `enable_routing` | String | `yes` or `no` | `yes` |
| `arp_flooding` | String | `yes` or `no` | `no` |
| `l2_unknown_unicast` | String | `proxy` or `flood` | `proxy` |

**Example**:
```excel
tenant,bd,vrf,description,enable_routing,arp_flooding
Production,Web_BD,Prod_VRF,Web tier bridge domain,yes,no
Production,App_BD,Prod_VRF,Application tier bridge domain,yes,no
Production,DB_BD,Prod_VRF,Database tier bridge domain,yes,no
Development,Dev_BD,Dev_VRF,Development bridge domain,yes,yes
```

### Bridge Domain Subnets

**Sheet Name**: `bd_subnet`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tenant` | String | Tenant name (must exist) | `Production` |
| `bd` | String | Bridge domain name (must exist) | `Web_BD` |
| `subnet` | String | Subnet CIDR | `10.1.1.1/24` |
| `description` | String | Subnet description | `Web tier subnet` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `scope` | String | `private`, `public`, or `shared` | `private` |
| `subnet_control` | String | `nd_ra`, `no_gw`, `querier_ip` | - |

**Example**:
```excel
tenant,bd,subnet,description,scope
Production,Web_BD,10.1.1.1/24,Web tier subnet,private
Production,App_BD,10.1.2.1/24,Application tier subnet,private
Production,DB_BD,10.1.3.1/24,Database tier subnet,private
Development,Dev_BD,10.2.1.1/24,Development subnet,private
```

### Application Profiles

**Sheet Name**: `ap`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tenant` | String | Tenant name (must exist) | `Production` |
| `ap` | String | Application profile name | `WebApp_AP` |
| `description` | String | AP description | `Web application profile` |

**Example**:
```excel
tenant,ap,description
Production,WebApp_AP,Web application profile
Production,ERP_AP,ERP application profile
Production,Database_AP,Database application profile
Development,DevApp_AP,Development application profile
```

### Endpoint Groups (EPGs)

**Sheet Name**: `epg`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `epg` | String | EPG name | `WebServers_EPG` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `ap` | String | Application profile (must exist) | `WebApp_AP` |
| `bd` | String | Bridge domain (must exist) | `Web_BD` |
| `description` | String | EPG description | `Web servers endpoint group` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `preferred_group` | String | `yes` or `no` | `no` |
| `intra_epg_isolation` | String | `enforced` or `unenforced` | `unenforced` |

**Example**:
```excel
epg,tenant,ap,bd,description,preferred_group
WebServers_EPG,Production,WebApp_AP,Web_BD,Web servers endpoint group,no
AppServers_EPG,Production,ERP_AP,App_BD,Application servers EPG,no
DBServers_EPG,Production,Database_AP,DB_BD,Database servers EPG,yes
DevWeb_EPG,Development,DevApp_AP,Dev_BD,Development web EPG,no
```

## 🔒 Security Objects

### Filters

**Sheet Name**: `filter`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `filter` | String | Filter name | `Web_Filter` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `entry` | String | Filter entry name | `HTTP` |
| `ethertype` | String | `ip`, `arp`, etc. | `ip` |
| `ip_protocol` | String | `tcp`, `udp`, `icmp` | `tcp` |
| `dst_port_start` | Integer | Destination port start | `80` |
| `dst_port_end` | Integer | Destination port end | `80` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `src_port_start` | Integer | Source port start | `unspecified` |
| `src_port_end` | Integer | Source port end | `unspecified` |
| `stateful` | String | `yes` or `no` | `yes` |

**Example**:
```excel
filter,tenant,entry,ethertype,ip_protocol,dst_port_start,dst_port_end,description
Web_Filter,Production,HTTP,ip,tcp,80,80,HTTP traffic
Web_Filter,Production,HTTPS,ip,tcp,443,443,HTTPS traffic
App_Filter,Production,Custom_App,ip,tcp,8080,8080,Custom application
DB_Filter,Production,MySQL,ip,tcp,3306,3306,MySQL database
```

### Contracts

**Sheet Name**: `contract`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `contract` | String | Contract name | `Web_Contract` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `description` | String | Contract description | `Web server access contract` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `scope` | String | `context`, `global`, `tenant` | `context` |
| `priority` | String | `unspecified`, `level1`, `level2`, `level3` | `unspecified` |

**Example**:
```excel
contract,tenant,description,scope
Web_Contract,Production,Web server access contract,context
App_Contract,Production,Application server contract,context
DB_Contract,Production,Database access contract,context
Common_Contract,Production,Common services contract,tenant
```

### Contract Subjects

**Sheet Name**: `contract_subject`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `contract` | String | Contract name (must exist) | `Web_Contract` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `subject` | String | Subject name | `Web_Subject` |
| `description` | String | Subject description | `Web traffic subject` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `reverse_filter` | String | `yes` or `no` | `yes` |
| `priority` | String | `unspecified`, `level1`, `level2`, `level3` | `unspecified` |

**Example**:
```excel
contract,tenant,subject,description,reverse_filter
Web_Contract,Production,Web_Subject,Web traffic subject,yes
App_Contract,Production,App_Subject,Application traffic subject,yes
DB_Contract,Production,DB_Subject,Database traffic subject,yes
```

### Contract Subject to Filter Associations

**Sheet Name**: `contract_subject_to_filter`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `contract` | String | Contract name (must exist) | `Web_Contract` |
| `subject` | String | Subject name (must exist) | `Web_Subject` |
| `filter` | String | Filter name (must exist) | `Web_Filter` |
| `tenant` | String | Tenant name (must exist) | `Production` |

**Example**:
```excel
contract,subject,filter,tenant
Web_Contract,Web_Subject,Web_Filter,Production
App_Contract,App_Subject,App_Filter,Production
DB_Contract,DB_Subject,DB_Filter,Production
```

### EPG to Contract Associations

**Sheet Name**: `epg_to_contract`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `epg` | String | EPG name (must exist) | `WebServers_EPG` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `ap` | String | Application profile (must exist) | `WebApp_AP` |
| `contract` | String | Contract name (must exist) | `Web_Contract` |
| `contract_type` | String | `provider` or `consumer` | `provider` |

**Example**:
```excel
epg,tenant,ap,contract,contract_type
WebServers_EPG,Production,WebApp_AP,Web_Contract,provider
AppServers_EPG,Production,ERP_AP,Web_Contract,consumer
AppServers_EPG,Production,ERP_AP,DB_Contract,consumer
DBServers_EPG,Production,Database_AP,DB_Contract,provider
```

## 🌐 L3Out Objects

### L3Out Configuration

**Sheet Name**: `l3out`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `l3out` | String | L3Out name | `Internet_L3Out` |
| `tenant` | String | Tenant name (must exist) | `Production` |
| `vrf` | String | VRF name (must exist) | `Prod_VRF` |
| `domain` | String | L3 domain name | `L3_Domain` |
| `description` | String | L3Out description | `Internet connectivity` |

**Optional Columns**:
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `route_control` | String | Route control enforcement | - |
| `dscp` | String | DSCP marking | `unspecified` |

**Example**:
```excel
l3out,tenant,vrf,domain,description
Internet_L3Out,Production,Prod_VRF,L3_Domain,Internet connectivity
Partner_L3Out,Production,Prod_VRF,L3_Domain,Partner network connectivity
MPLS_L3Out,Production,Prod_VRF,L3_Domain,MPLS WAN connectivity
```

## 📝 Validation Rules

### Data Integrity
- **Foreign Keys**: Referenced objects must exist in their respective sheets
- **Unique Names**: Object names must be unique within their scope
- **Required Fields**: All required columns must have values
- **Data Types**: Values must match expected data types

### ACI Constraints
- **Naming**: Follow ACI naming conventions (no spaces, special characters)
- **Dependencies**: Respect ACI object hierarchy (Tenant → VRF → BD → EPG)
- **Limits**: Stay within ACI platform limits (e.g., 4000 VLANs per pool)

### Excel Format
- **File Type**: Use .xlsx format only
- **Sheet Names**: Exact case-sensitive matching required
- **No Formulas**: Use plain text values only
- **No Formatting**: Avoid special cell formatting

## 🔍 Troubleshooting

### Common Errors

#### Sheet Name Mismatch
```
Error: Sheet 'vlans' not found
Solution: Use exact name 'vlan_pool'
```

#### Missing Required Columns
```
Error: Required column 'tenant' missing in sheet 'vrf'
Solution: Add 'tenant' column header
```

#### Invalid References
```
Error: VRF 'MyVRF' not found for BD 'MyBD'
Solution: Ensure VRF exists in 'vrf' sheet
```

#### Data Type Errors
```
Error: Invalid integer value 'abc' in column 'from'
Solution: Use numeric values for VLAN IDs
```

### Best Practices

1. **Start Simple**: Begin with basic objects (tenant, VRF, BD)
2. **Validate Early**: Test small configurations first
3. **Use Consistent Naming**: Establish naming conventions
4. **Document Dependencies**: Understand object relationships
5. **Version Control**: Keep Excel files in version control
6. **Test Incrementally**: Add objects gradually

## 📚 References

- **ACI Object Model**: [Cisco ACI Management Information Model](https://developer.cisco.com/docs/apic-mim-ref/)
- **Ansible ACI Collection**: [cisco.aci Documentation](https://docs.ansible.com/ansible/latest/collections/cisco/aci/)
- **ACI Best Practices**: [Cisco ACI Design Guide](https://www.cisco.com/c/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/white-paper-c11-737909.html)