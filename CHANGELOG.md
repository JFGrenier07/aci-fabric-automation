# 📝 Changelog

All notable changes to the ACI Fabric Automation Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Comprehensive documentation suite

## [2.1.0] - 2024-11-24

### Fixed
- **LLDP Warning Resolution**: Fixed 'item' is undefined warning in interface_policy_lldp.yml
  - Removed trailing space from CSV column reference (lldp_policy )
  - Changed task name from dynamic to static to prevent Jinja2 template errors
  - Updated all references from item['lldp_policy '] to item.lldp_policy
- **CDP Boolean Handling**: Fixed admin_state empty string error in interface_policy_cdp.yml
  - Added fallback with omit when admin_state is empty
  - Prevents "unable to convert to bool" errors
- **Route Control State Parameters**: Commented out state parameters in 4 route control task files
  - tasks/match_rule.yml
  - tasks/match_route_destination.yml
  - tasks/route_control_profile.yml
  - tasks/route_control_context.yml
  - Tasks now use default behavior (state=present)
- **Parameter Optimization**: Commented out 106+ unused parameters across 44 task files
  - Ensured all task parameters align with CSV column definitions
  - Prevents "undefined variable" errors during deployment

### Security
- **Credential Management Enhancement**: Modified excel_to_csv_simple.py to generate inventory.yml with placeholders
  - Removed hardcoded credentials from generated deployment directories
  - New placeholders: YOUR_APIC_IP_HERE, YOUR_USERNAME_HERE, YOUR_PASSWORD_HERE
  - Added warning comment for users to fill credentials before deployment
  - Updated inventory.yml generation to always use secure placeholders

### Changed
- **Repository Structure Cleanup**: Removed auto-generated files from version control
  - Removed csv/ directory (created automatically during execution)
  - Removed logs/ directory (created automatically during execution)
  - Removed ansible.cfg (generated automatically by excel_to_csv_simple.py)
  - Removed inventory.yml (generated automatically by excel_to_csv_simple.py)
  - Cleaner repository with only source files tracked
- **Configuration Generation**: All configuration files now generated at runtime
  - ansible.cfg generated with optimized settings
  - inventory.yml generated with secure placeholders
  - CSV files generated from Excel source
  - Dynamic directory creation as needed

### Testing
- Full playbook deployment tested successfully
- Results: ok=217, changed=47, failed=0
- No warnings detected
- All 53 ACI modules working correctly including route control modules

## [2.0.0] - 2024-01-15

### Added
- **Dynamic Playbook Generation**: Automatic creation of optimized Ansible playbooks based on Excel content
- **Intelligent Module Detection**: Automatic discovery of required ACI modules from data
- **Enhanced Security Model**: Environment variable-based credential management
- **Comprehensive Logging**: Structured logging with multiple verbosity levels
- **Production-Ready Configuration**: Pre-configured Ansible settings for enterprise deployment
- **47 ACI Object Types**: Support for complete ACI fabric configuration
- **Dependency Management**: Intelligent ordering of deployment operations
- **State Management**: Full lifecycle support (create, update, delete, query)
- **Validation Engine**: Pre-deployment validation and error checking
- **Template System**: Standardized Excel template with validation rules

### Enhanced
- **Performance Optimization**: Parallel execution and connection reuse
- **Error Handling**: Comprehensive error detection and recovery
- **Documentation**: Complete user guides and API documentation
- **Testing Framework**: Unit and integration test coverage
- **Code Quality**: PEP 8 compliance and type hints

### Technical Improvements
- **Architecture Redesign**: Modular, pipeline-based processing
- **Excel Parser Engine**: Intelligent sheet detection and validation
- **CSV Processing**: Streaming data processing for large datasets
- **Ansible Integration**: Deep integration with cisco.aci collection
- **Configuration Management**: Flexible environment-based configuration

## [1.5.0] - 2023-12-01

### Added
- **L3Out Advanced Features**: Support for floating SVI secondary IPs
- **BGP Protocol Profiles**: Complete BGP peer configuration
- **Interface Policy Enhancements**: Additional interface policy types
- **Switch Profile Management**: Comprehensive switch and interface profiles
- **VPC Protection Groups**: Advanced VPC configuration support

### Fixed
- **Switch Profile Deployment**: Resolved missing include_tasks for switch profiles
- **Dependency Ordering**: Fixed infrastructure deployment sequence
- **CSV Generation**: Improved data validation and error handling
- **Module Detection**: Enhanced accuracy of module requirement detection

### Changed
- **Task Organization**: Restructured task files for better maintainability
- **Error Messages**: More descriptive and actionable error reporting
- **Performance**: Optimized CSV processing for large configurations

## [1.4.0] - 2023-11-15

### Added
- **Security Enhancements**: Contract and filter management
- **EPG Associations**: Comprehensive EPG to contract bindings
- **Bridge Domain Subnets**: Advanced subnet configuration
- **Application Profiles**: Complete application profile management
- **Enhanced Validation**: Pre-deployment configuration validation

### Improved
- **Excel Template**: Clearer documentation and examples
- **Error Handling**: Better error messages and recovery
- **Logging**: Enhanced debugging and audit capabilities

## [1.3.0] - 2023-10-30

### Added
- **Tenant Management**: Complete tenant lifecycle management
- **VRF Contexts**: Advanced VRF configuration with policies
- **Bridge Domains**: Full bridge domain configuration
- **Endpoint Groups**: EPG management with advanced features
- **Interface Policies**: Comprehensive interface policy support

### Enhanced
- **Data Validation**: Improved Excel data validation
- **CSV Processing**: Better handling of complex data structures
- **Ansible Tasks**: Optimized task execution and error handling

## [1.2.0] - 2023-10-15

### Added
- **Physical Domain Support**: Complete physical domain configuration
- **AEP Management**: Attachable Entity Profile configuration
- **VLAN Pool Associations**: Domain to VLAN pool bindings
- **Infrastructure Automation**: Complete infrastructure setup

### Fixed
- **Sheet Detection**: Improved Excel sheet analysis
- **Data Processing**: Better handling of empty cells and missing data
- **Module Ordering**: Corrected dependency-based execution order

## [1.1.0] - 2023-09-30

### Added
- **VLAN Pool Management**: Complete VLAN pool and encapsulation block support
- **Dynamic Sheet Detection**: Automatic Excel sheet analysis
- **CSV Export Engine**: Intelligent data transformation
- **Module Detection System**: Automatic ACI module identification

### Improved
- **Excel Parser**: Enhanced data extraction and validation
- **Error Reporting**: More detailed error messages and logging
- **Code Organization**: Better modular structure

## [1.0.0] - 2023-09-15

### Added
- **Initial Release**: Basic Excel to CSV conversion
- **Ansible Integration**: Basic Ansible playbook execution
- **ACI Module Support**: Support for core ACI objects
- **Configuration Management**: Basic configuration handling

### Features
- Excel to CSV conversion
- Basic ACI object deployment
- Simple Ansible playbook execution
- Configuration validation

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

## Migration Guides

### Upgrading from 1.x to 2.0

**Breaking Changes**:
1. **Configuration Format**: Environment variables now required
2. **Sheet Names**: Stricter sheet name validation
3. **Playbook Structure**: New dynamic playbook format

**Migration Steps**:
```bash
# 1. Create environment configuration
cp .env.example .env
# Edit .env with your APIC credentials

# 2. Update Excel templates
# Ensure sheet names match exactly (case-sensitive)

# 3. Test new dynamic playbooks
python3 excel_to_csv_simple.py your_config.xlsx
ansible-playbook --syntax-check your_config.yml
```

### Upgrading from 1.5 to 2.0

**New Features**:
- Dynamic playbook generation (automatic)
- Enhanced security model (environment variables)
- Improved error handling (automatic)

**Optional Optimizations**:
```bash
# Enable enhanced logging
echo "verbosity = 2" >> ansible.cfg

# Use parallel execution
export ANSIBLE_FORKS=10
```

## Support Matrix

| Version | Python | Ansible | ACI Support | Status |
|---------|--------|---------|-------------|--------|
| 2.0.x   | 3.8+   | 6.0+    | 4.x, 5.x, 6.x | Active |
| 1.5.x   | 3.7+   | 5.0+    | 4.x, 5.x    | Security Only |
| 1.4.x   | 3.7+   | 4.0+    | 4.x, 5.x    | End of Life |
| 1.x     | 3.6+   | 4.0+    | 4.x         | End of Life |

## Roadmap

### Version 2.1 (Q2 2024)
- **Cloud ACI Support**: Azure and AWS ACI integration
- **Enhanced Templates**: Interactive Excel templates with validation
- **REST API Interface**: RESTful API for programmatic access
- **Monitoring Dashboard**: Real-time deployment monitoring

### Version 2.2 (Q3 2024)
- **Multi-Site Support**: Cross-site fabric management
- **Policy Templates**: Pre-built policy templates library
- **Advanced Validation**: AI-powered configuration validation
- **Performance Analytics**: Deployment performance insights

### Version 3.0 (Q4 2024)
- **GUI Interface**: Web-based configuration interface
- **Workflow Engine**: Advanced deployment workflows
- **Integration APIs**: Third-party system integration
- **Enterprise Features**: Advanced security and compliance

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.