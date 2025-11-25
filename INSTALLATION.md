# 📦 Installation Guide

This guide provides comprehensive installation instructions for the ACI Fabric Automation Engine across different environments.

## 🔧 System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 18.04+, RHEL 7+, CentOS 7+), macOS 10.15+, or Windows 10 with WSL2
- **Python**: 3.8 or higher
- **Memory**: 2GB RAM (4GB+ recommended for large configurations)
- **Storage**: 1GB free disk space
- **Network**: Direct connectivity to APIC management interface

### Recommended Requirements
- **Python**: 3.9+ for optimal performance
- **Memory**: 8GB RAM for enterprise deployments
- **CPU**: 4+ cores for parallel execution
- **Network**: Low-latency connection to APIC (< 50ms)

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git -y

# Verify Python version
python3 --version  # Should be 3.8+

# Clone the repository
git clone https://github.com/your-org/aci-fabric-automation.git
cd aci-fabric-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install pandas openpyxl ansible

# Install Ansible ACI collection
ansible-galaxy collection install cisco.aci

# Configure environment
cp .env.example .env
```

### RHEL/CentOS/Fedora

```bash
# Install Python and development tools
sudo dnf install python3 python3-pip python3-devel git -y
# For RHEL/CentOS 7: sudo yum install python3 python3-pip python3-devel git -y

# Clone and setup
git clone https://github.com/your-org/aci-fabric-automation.git
cd aci-fabric-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pandas openpyxl ansible

# Install ACI collection
ansible-galaxy collection install cisco.aci

# Configure environment
cp .env.example .env
```

## 🍎 macOS Installation

### Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3 git

# Clone the repository
git clone https://github.com/your-org/aci-fabric-automation.git
cd aci-fabric-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pandas openpyxl ansible

# Install ACI collection
ansible-galaxy collection install cisco.aci

# Configure environment
cp .env.example .env
```

### Using Python.org Installer

```bash
# Download and install Python from https://www.python.org/downloads/
# Ensure "Add Python to PATH" is checked during installation

# Open Terminal and verify installation
python3 --version

# Clone and setup
git clone https://github.com/your-org/aci-fabric-automation.git
cd aci-fabric-automation

# Continue with virtual environment setup as above
```

## 🪟 Windows Installation

### Using Windows Subsystem for Linux (WSL2) - Recommended

```bash
# Install WSL2 (PowerShell as Administrator)
wsl --install -d Ubuntu

# Restart computer and open Ubuntu terminal
# Follow Ubuntu installation steps above
```

### Using Native Windows

```powershell
# Install Python from Microsoft Store or python.org
# Open PowerShell as Administrator

# Clone repository
git clone https://github.com/your-org/aci-fabric-automation.git
cd aci-fabric-automation

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install pandas openpyxl ansible

# Install ACI collection
ansible-galaxy collection install cisco.aci

# Configure environment
copy .env.example .env
```

## 🐳 Docker Installation

### Using Docker Container

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ansible ACI collection
RUN ansible-galaxy collection install cisco.aci

# Copy application code
COPY . .

# Create directories
RUN mkdir -p logs csv

ENTRYPOINT ["python3", "excel_to_csv.py"]
EOF

# Build container
docker build -t aci-automation .

# Run container
docker run -v $(pwd)/config:/app/config \
           -v $(pwd)/logs:/app/logs \
           -v $(pwd)/csv:/app/csv \
           --env-file .env \
           aci-automation config/your_fabric.xlsx
```

### Using Docker Compose

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

## 📋 Requirements File

Create `requirements.txt`:

```txt
# Core dependencies
ansible>=6.0.0
ansible-core>=2.12.0
pandas>=1.3.0
openpyxl>=3.0.0

# Optional performance enhancements
PyYAML>=6.0
Jinja2>=3.0.0
requests>=2.25.0

# Development dependencies (optional)
pytest>=6.0.0
black>=22.0.0
flake8>=4.0.0
```

## ⚙️ Configuration Setup

### 1. Environment Configuration

```bash
# Copy and edit environment file
cp .env.example .env

# Edit with your APIC details
vim .env  # or nano .env on some systems
```

**Required Environment Variables:**

```bash
# APIC Connection
ACI_HOSTNAME=your-apic.company.com
ACI_USERNAME=admin
ACI_PASSWORD=your_secure_password

# SSL Configuration
ACI_VALIDATE_CERTS=false  # Set to true for production

# Deployment Options
GLOBAL_STATE=present
CSV_DIR=csv

# Performance Settings
ANSIBLE_TIMEOUT=300
ANSIBLE_FORKS=5
ANSIBLE_GATHERING=explicit
```

### 2. Ansible Configuration

The included `ansible.cfg` is pre-configured, but you may customize:

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

### 3. Inventory Setup

Edit `inventory.yml` to match your environment:

```yaml
---
all:
  hosts:
    localhost:
      ansible_connection: local
  vars:
    # Use environment variables for security
    aci_hostname: "{{ lookup('env', 'ACI_HOSTNAME') }}"
    aci_username: "{{ lookup('env', 'ACI_USERNAME') }}"
    aci_password: "{{ lookup('env', 'ACI_PASSWORD') }}"
    aci_validate_certs: "{{ lookup('env', 'ACI_VALIDATE_CERTS') | default(false) | bool }}"
```

## ✅ Installation Verification

### 1. Basic Verification

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Verify Python packages
python3 -c "import pandas, openpyxl, ansible; print('All packages imported successfully')"

# Verify Ansible installation
ansible --version

# Verify ACI collection
ansible-galaxy collection list | grep cisco.aci

# Test script syntax
python3 excel_to_csv.py --help
```

### 2. Connectivity Test

```bash
# Test APIC connectivity (ensure .env is configured)
ansible all -i inventory.yml -m ping

# Test ACI module availability
ansible-doc cisco.aci.aci_tenant
```

### 3. End-to-End Test

```bash
# Test with sample Excel file
python3 excel_to_csv.py aci_fabric_config.xlsx

# Verify CSV generation
ls -la csv/

# Test playbook syntax
ansible-playbook --syntax-check aci_fabric_config.yml

# Dry-run test (no changes made)
ansible-playbook -i inventory.yml aci_fabric_config.yml --check
```

## 🔧 Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Error: Python 3.8+ required
# Solution: Install correct Python version
sudo apt install python3.9 python3.9-venv python3.9-pip
python3.9 -m venv venv
```

#### Pandas Installation Errors
```bash
# Error: Microsoft Visual C++ required (Windows)
# Solution: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Error: Failed building wheel for pandas
# Solution: Use conda instead of pip
conda install pandas openpyxl
```

#### Ansible Collection Issues
```bash
# Error: cisco.aci collection not found
# Solution: Reinstall collection
ansible-galaxy collection install cisco.aci --force

# Verify installation path
ansible-galaxy collection list --format json | jq '.cisco.aci'
```

#### Permission Issues (Linux/macOS)
```bash
# Error: Permission denied
# Solution: Fix ownership
sudo chown -R $USER:$USER aci-fabric-automation/
chmod +x excel_to_csv.py
```

### Environment-Specific Issues

#### WSL2 on Windows
```bash
# Issue: Can't access Windows files
# Solution: Use WSL2 filesystem
cd /home/$USER
git clone https://github.com/your-org/aci-fabric-automation.git

# Issue: Ansible too slow
# Solution: Exclude Windows Defender
# Add WSL2 directory to Windows Defender exclusions
```

#### macOS Catalina/Big Sur
```bash
# Issue: SSL certificate errors
# Solution: Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Issue: Command line tools required
xcode-select --install
```

## 🚀 Production Deployment

### Security Hardening

```bash
# Use Ansible Vault for sensitive data
ansible-vault create vault.yml

# Add encrypted variables
ansible-vault edit vault.yml

# Update inventory to use vault
echo "aci_password: !vault |" >> inventory.yml
```

### Performance Optimization

```bash
# Optimize for large deployments
export ANSIBLE_FORKS=10
export ANSIBLE_GATHERING=explicit
export ANSIBLE_HOST_KEY_CHECKING=False

# Use persistent connections
echo "use_persistent_connections = True" >> ansible.cfg
```

### Monitoring Setup

```bash
# Enable structured logging
mkdir -p logs
echo "log_path = logs/ansible.log" >> ansible.cfg
echo "stdout_callback = json" >> ansible.cfg

# Setup log rotation
sudo tee /etc/logrotate.d/aci-automation << 'EOF'
/path/to/aci-automation/logs/*.log {
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

## 📚 Next Steps

After successful installation:

1. **Configure Excel Template**: Follow [Excel Template Guide](EXCEL_TEMPLATE.md)
2. **Run First Deployment**: See [Usage Guide](README.md#usage)
3. **Set Up Monitoring**: Configure logging and alerts
4. **Plan Production Rollout**: Test in lab environment first

## 🆘 Getting Help

If you encounter issues during installation:

1. **Check Requirements**: Ensure all system requirements are met
2. **Review Logs**: Check installation and execution logs
3. **Search Issues**: Look through [GitHub Issues](https://github.com/your-org/aci-fabric-automation/issues)
4. **Ask for Help**: Create a new issue with installation details

**Include in support requests:**
- Operating system and version
- Python version (`python3 --version`)
- Installation method used
- Complete error messages
- Contents of `.env` file (without passwords)