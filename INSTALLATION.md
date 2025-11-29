# 📦 Installation Guide

Complete installation guide for the ACI Fabric Automation Engine.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
- [Verification](#verification)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🖥️ System Requirements

### Operating System
- **Linux**: Ubuntu 20.04+, CentOS 8+, RHEL 8+, Debian 10+
- **macOS**: 10.15 (Catalina) or newer
- **Windows**: Windows 10/11 with WSL2 (Ubuntu recommended)

### Software Requirements

| Component | Minimum Version | Recommended Version |
|-----------|----------------|---------------------|
| Python | 3.8 | 3.10+ |
| pip | 20.0 | Latest |
| Ansible | 2.12 | 2.15+ |
| Excel | Microsoft Excel 2016+ or LibreOffice 6.0+ | Latest |

### Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk Space | 2 GB | 5+ GB |
| Network | 1 Mbps | 10+ Mbps |

### Network Requirements
- Network connectivity to Cisco APIC controller
- HTTPS (443) access to APIC
- SSH access (optional, for troubleshooting)

## ⚡ Quick Installation

### Manual Quick Install

```bash
# 1. Install Python dependencies
pip install pandas openpyxl

# 2. Install Ansible
pip install ansible

# 3. Install Cisco ACI collection
ansible-galaxy collection install cisco.aci

# 4. Download the automation engine
git clone https://github.com/your-org/aci-automation.git
cd aci-automation/production_ready

# 5. Verify installation
python3 fabric_automation.py --help
```

## 🔧 Detailed Installation

### Step 1: Install Python

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python 3.10
sudo apt install -y python3.10 python3.10-venv python3-pip

# Verify installation
python3 --version  # Should show Python 3.10.x
```

#### CentOS/RHEL
```bash
# Install Python 3.10
sudo dnf install -y python310 python310-pip

# Verify installation
python3.10 --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.10

# Verify installation
python3 --version
```

#### Windows (WSL2)
```bash
# Install WSL2 with Ubuntu
wsl --install -d Ubuntu-22.04

# Inside WSL, install Python
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip
```

### Step 2: Create Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv aci-automation-env

# Activate virtual environment
source aci-automation-env/bin/activate  # Linux/macOS
# OR
aci-automation-env\Scripts\activate.bat  # Windows

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Python Dependencies

#### Install pandas and openpyxl
```bash
# Install required packages
pip install pandas openpyxl

# Verify installation
python3 -c "import pandas; print(f'pandas {pandas.__version__}')"
python3 -c "import openpyxl; print(f'openpyxl {openpyxl.__version__}')"
```

**Expected output:**
```
pandas 2.0.3
openpyxl 3.1.2
```

#### Optional: Install from requirements.txt
```bash
# If requirements.txt is provided
pip install -r requirements.txt
```

**Sample requirements.txt:**
```
pandas>=2.0.0
openpyxl>=3.1.0
ansible>=2.12.0
```

### Step 4: Install Ansible

#### Method 1: Using pip (Recommended)
```bash
# Install Ansible
pip install ansible

# Verify installation
ansible --version
```

**Expected output:**
```
ansible [core 2.15.3]
  config file = None
  configured module search path = [...]
  ansible python module location = ...
  executable location = ...
  python version = 3.10.12
```

#### Method 2: Using system package manager

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y ansible
```

**CentOS/RHEL:**
```bash
sudo dnf install -y ansible
```

**macOS:**
```bash
brew install ansible
```

### Step 5: Install Cisco ACI Collection

```bash
# Install cisco.aci collection
ansible-galaxy collection install cisco.aci

# Verify installation
ansible-galaxy collection list | grep cisco.aci
```

**Expected output:**
```
cisco.aci    2.7.0
```

#### Install Specific Version
```bash
# Install specific version (if needed)
ansible-galaxy collection install cisco.aci:2.7.0
```

#### Offline Installation
```bash
# Download collection
ansible-galaxy collection download cisco.aci --download-path ./collections/

# Install from downloaded file
ansible-galaxy collection install ./collections/cisco-aci-2.7.0.tar.gz
```

### Step 6: Download Automation Engine

#### Option 1: Git Clone (Recommended)
```bash
# Clone repository
git clone https://github.com/your-org/aci-automation.git

# Navigate to production_ready
cd aci-automation/production_ready
```

#### Option 2: Download ZIP
```bash
# Download and extract
wget https://github.com/your-org/aci-automation/archive/main.zip
unzip main.zip
cd aci-automation-main/production_ready
```

#### Option 3: Direct Download
```bash
# Download only production_ready files
wget https://github.com/your-org/aci-automation/raw/main/production_ready/fabric_automation.py
mkdir -p tasks csv
# Download other required files...
```

### Step 7: Setup Excel Template

```bash
# Copy Excel template
cp aci_fabric_config.xlsx my_fabric.xlsx

# Edit with your preferred tool
# - Microsoft Excel
# - LibreOffice Calc
# - Google Sheets (export to .xlsx)
```

## ✅ Verification

### Verify Complete Installation

```bash
# Run verification script
python3 << 'EOF'
import sys
import subprocess

def check_module(module_name):
    try:
        __import__(module_name)
        print(f"✅ {module_name} installed")
        return True
    except ImportError:
        print(f"❌ {module_name} NOT installed")
        return False

def check_command(command):
    try:
        result = subprocess.run([command, '--version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command} installed")
            return True
    except:
        pass
    print(f"❌ {command} NOT installed")
    return False

print("="*60)
print("ACI Fabric Automation Engine - Installation Verification")
print("="*60)

print("\n📦 Python Modules:")
pandas_ok = check_module('pandas')
openpyxl_ok = check_module('openpyxl')

print("\n🔧 Command-line Tools:")
ansible_ok = check_command('ansible')
ansible_playbook_ok = check_command('ansible-playbook')

print("\n📊 Summary:")
all_ok = pandas_ok and openpyxl_ok and ansible_ok and ansible_playbook_ok

if all_ok:
    print("✅ All components installed successfully!")
    print("🚀 Ready to use fabric_automation.py")
else:
    print("❌ Some components missing")
    print("📖 Please review installation steps")

print("="*60)
EOF
```

### Test fabric_automation.py

```bash
# Test with sample Excel file
python3 fabric_automation.py aci_fabric_config.xlsx

# Expected: Successful deployment directory creation
```

### Verify Ansible Collection

```bash
# Test Ansible can find cisco.aci modules
ansible-doc cisco.aci.aci_tenant
```

**Expected:** Documentation for aci_tenant module

### Test APIC Connectivity

```bash
# Create test inventory
cat > test_inventory.yml << 'EOF'
all:
  hosts:
    localhost:
      ansible_connection: local
      aci_hostname: "YOUR_APIC_IP"
      aci_username: "YOUR_USERNAME"
      aci_password: "YOUR_PASSWORD"
      aci_validate_certs: false
EOF

# Test connection (requires valid APIC credentials)
ansible localhost -i test_inventory.yml -m cisco.aci.aci_tenant -a "tenant=TEST_TENANT state=query"
```

**Expected:** JSON output with tenant information or "Tenant not found"

## ⚙️ Configuration

### Configure Python Environment

```bash
# Set Python path (if needed)
export PYTHONPATH=/path/to/aci-automation:$PYTHONPATH

# Add to ~/.bashrc for persistence
echo 'export PYTHONPATH=/path/to/aci-automation:$PYTHONPATH' >> ~/.bashrc
```

### Configure Ansible

Create `~/.ansible.cfg`:

```ini
[defaults]
host_key_checking = False
retry_files_enabled = False
deprecation_warnings = False
stdout_callback = yaml
bin_ansible_callbacks = True
collections_paths = ~/.ansible/collections:/usr/share/ansible/collections

[privilege_escalation]
become = False
```

### Configure Excel Application

#### Microsoft Excel
- Ensure "Developer" tab is enabled for macro support (optional)
- Set default save format to `.xlsx`

#### LibreOffice Calc
```bash
# Install LibreOffice (Ubuntu/Debian)
sudo apt install -y libreoffice-calc

# Configure for Excel compatibility
# Tools → Options → Load/Save → Microsoft Office
# ✅ Enable all Excel format options
```

### Setup Environment Variables

```bash
# Create .env file (optional)
cat > .env << 'EOF'
# APIC Connection (used by scripts)
APIC_HOST=192.168.1.100
APIC_USER=admin
APIC_PASS=YourPassword

# Automation Settings
DEPLOYMENT_DIR=./deployments
LOG_LEVEL=INFO
EOF

# Load environment
source .env
```

## 🐛 Troubleshooting

### Issue 1: Python version too old

**Error:**
```
SyntaxError: f-string: empty expression not allowed
```

**Solution:**
```bash
# Check Python version
python3 --version

# Install Python 3.10+ (see Step 1)
sudo apt install python3.10

# Use specific version
python3.10 fabric_automation.py config.xlsx
```

### Issue 2: pandas import error

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
# Install pandas
pip install pandas

# Or with specific version
pip install pandas==2.0.3

# Verify
python3 -c "import pandas; print(pandas.__version__)"
```

### Issue 3: openpyxl import error

**Error:**
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution:**
```bash
# Install openpyxl
pip install openpyxl

# Verify
python3 -c "import openpyxl; print(openpyxl.__version__)"
```

### Issue 4: Ansible collection not found

**Error:**
```
ERROR! couldn't resolve module/action 'cisco.aci.aci_tenant'
```

**Solution:**
```bash
# Install collection
ansible-galaxy collection install cisco.aci

# Verify installation
ansible-galaxy collection list | grep cisco.aci

# Check collection path
ansible-config dump | grep COLLECTIONS_PATHS
```

### Issue 5: Permission denied

**Error:**
```
Permission denied: 'fabric_automation.py'
```

**Solution:**
```bash
# Make executable
chmod +x fabric_automation.py

# Or run with python3
python3 fabric_automation.py config.xlsx
```

### Issue 6: Excel file format error

**Error:**
```
ValueError: Excel file format cannot be determined
```

**Solution:**
```bash
# Ensure file is .xlsx format
file config.xlsx

# Convert if needed (LibreOffice)
libreoffice --headless --convert-to xlsx config.xls

# Verify
python3 -c "import openpyxl; wb = openpyxl.load_workbook('config.xlsx'); print('OK')"
```

### Issue 7: APIC connection timeout

**Error:**
```
Connection timeout to APIC
```

**Solution:**
```bash
# Test network connectivity
ping YOUR_APIC_IP

# Test HTTPS access
curl -k https://YOUR_APIC_IP

# Check firewall rules
sudo iptables -L | grep 443

# Verify credentials in inventory.yml
```

### Issue 8: SSL certificate error

**Error:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```yaml
# In inventory.yml, set:
aci_validate_certs: false  # For self-signed certificates

# Or install APIC certificate
sudo cp apic-cert.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

## 📚 Post-Installation

### Recommended: Create Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
alias aci-generate='python3 /path/to/production_ready/fabric_automation.py'

# Usage
aci-generate my_fabric.xlsx
```

### Recommended: Setup Logging

```bash
# Create logs directory
mkdir -p ~/aci-automation/logs

# Configure log rotation
cat > ~/aci-automation/logrotate.conf << 'EOF'
~/aci-automation/logs/*.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
EOF
```

### Recommended: Backup Strategy

```bash
# Backup Excel templates
mkdir -p ~/aci-automation/backups
cp *.xlsx ~/aci-automation/backups/backup-$(date +%Y%m%d).xlsx

# Automate backups (cron)
(crontab -l 2>/dev/null; echo "0 0 * * * cp ~/aci-automation/*.xlsx ~/aci-automation/backups/backup-\$(date +\%Y\%m\%d).xlsx") | crontab -
```

## 🎓 Next Steps

After successful installation:

1. **Read Documentation**: Review [README.md](README.md) for usage instructions
2. **Study Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. **Review Template**: Check [EXCEL_TEMPLATE.md](EXCEL_TEMPLATE.md) for Excel structure
4. **Try Examples**: Run example deployments
5. **Deploy Test Environment**: Test on development APIC first

## 📞 Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [README.md](README.md) for common issues
3. Check GitHub Issues for similar problems
4. Create new issue with:
   - Python version (`python3 --version`)
   - Ansible version (`ansible --version`)
   - Error messages (full output)
   - Steps to reproduce

---

**Installation Complete! 🎉**

Ready to automate your ACI fabric deployment!
