# 🤝 Contributing to ACI Fabric Automation Engine

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the ACI Fabric Automation Engine project.

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Search existing issues before creating new ones
- Use the bug report template
- Include system information and error logs
- Provide minimal reproduction steps

### ✨ Feature Requests
- Check if the feature already exists
- Use the feature request template
- Explain the use case and business value
- Consider backward compatibility

### 📝 Documentation
- Improve README, guides, and code comments
- Add examples and use cases
- Fix typos and unclear explanations
- Translate documentation

### 💻 Code Contributions
- Bug fixes and performance improvements
- New ACI object support
- Testing infrastructure
- Developer tooling

## 🚀 Getting Started

### 1. Development Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aci-fabric-automation.git
cd aci-fabric-automation

# Create development environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 2. Development Dependencies

Create `requirements-dev.txt`:
```txt
# Testing
pytest>=7.0.0
pytest-ansible>=3.0.0
pytest-cov>=4.0.0
pytest-mock>=3.0.0

# Code quality
black>=22.0.0
flake8>=4.0.0
isort>=5.0.0
mypy>=0.910

# Documentation
mkdocs>=1.4.0
mkdocs-material>=8.0.0

# Development tools
pre-commit>=2.15.0
tox>=3.20.0
```

### 3. Pre-commit Configuration

Create `.pre-commit-config.yaml`:
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

## 📊 Development Workflow

### 1. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Create bugfix branch
git checkout -b bugfix/fix-issue-123

# Create documentation branch
git checkout -b docs/improve-readme
```

### 2. Making Changes

```bash
# Make your changes
vim excel_to_csv_simple.py

# Run tests
pytest tests/

# Run code quality checks
black .
flake8 .
isort .

# Test your changes
python3 excel_to_csv_simple.py test_config.xlsx
ansible-playbook --syntax-check test_config.yml
```

### 3. Commit Guidelines

**Commit Message Format**:
```
type(scope): description

Longer explanation if needed

Fixes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(parser): add support for L3Out secondary IPs"
git commit -m "fix(tasks): resolve tenant dependency issue"
git commit -m "docs(readme): update installation instructions"
```

## 🧪 Testing Guidelines

### 1. Test Structure

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
│   ├── sample_config.xlsx
│   └── expected_output.csv
└── conftest.py
```

### 2. Writing Tests

```python
# tests/unit/test_parser.py
import pytest
from excel_to_csv_simple import ExcelToCSVSimple


class TestExcelParser:
    def test_has_real_data_with_valid_sheet(self):
        """Test that valid sheets are detected correctly."""
        parser = ExcelToCSVSimple("tests/fixtures/sample_config.xlsx")
        assert parser.has_real_data("vlan_pool") is True

    def test_has_real_data_with_empty_sheet(self):
        """Test that empty sheets are rejected."""
        parser = ExcelToCSVSimple("tests/fixtures/sample_config.xlsx")
        assert parser.has_real_data("empty_sheet") is False

    @pytest.mark.parametrize("sheet_name", [
        "Navigation", "Sheet1", "Template", "README"
    ])
    def test_ignore_system_sheets(self, sheet_name):
        """Test that system sheets are ignored."""
        parser = ExcelToCSVSimple()
        assert sheet_name in parser.ignore_sheets
```

### 3. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=excel_to_csv_simple

# Run specific test file
pytest tests/unit/test_parser.py

# Run with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/
```

## 📋 Adding New ACI Objects

### 1. Task File Creation

Create `tasks/new_object.yml`:
```yaml
---
# Tâches pour gérer les new_objects avec read_csv
- name: "Read CSV New Objects"
  read_csv:
    path: "{{ csv_dir }}/new_object.csv"
    delimiter: ','
  register: new_object_csv
  when: (csv_dir + '/new_object.csv') is file

- name: "Afficher les New Objects détectés"
  debug:
    msg: "New Objects à traiter: {{ new_object_csv.list | map(attribute='name') | list }}"
  when: new_object_csv is defined and new_object_csv.list is defined

- name: "{{ item.name }} - Créer le New Object ACI"
  cisco.aci.aci_new_object:
    host: "{{ aci_hostname }}"
    username: "{{ aci_username }}"
    password: "{{ aci_password }}"
    validate_certs: "{{ aci_validate_certs | default(false) }}"
    use_ssl: true
    # Object-specific parameters
    name: "{{ item.name }}"
    description: "{{ item.description | default('') }}"
    state: "{{ item.state | default(global_state) }}"
  loop: "{{ new_object_csv.list }}"
  when:
    - new_object_csv is defined
    - new_object_csv.list is defined
    - item.name is defined
    - item.name | length > 0
  tags:
    - new_object
    - aci_new_object
```

### 2. Update Parser

Add to `excel_to_csv_simple.py`:
```python
# Add to module_order list in correct dependency position
module_order = [
    # ... existing modules
    'aci_new_object',  # Add in appropriate order
    # ... remaining modules
]

# Add to descriptions dictionary
descriptions = {
    # ... existing descriptions
    'new_object': 'New Object description',
}
```

### 3. Documentation Update

Add to `EXCEL_TEMPLATE.md`:
```markdown
### New Object Configuration

**Sheet Name**: `new_object`

**Required Columns**:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `name` | String | Object name | `New_Object_1` |
| `description` | String | Object description | `Description here` |
| `required_field` | String | Required parameter | `value` |

**Example**:
```excel
name,description,required_field
New_Object_1,First new object,value1
New_Object_2,Second new object,value2
```

### 4. Add Tests

Create `tests/unit/test_new_object.py`:
```python
import pytest
from unittest.mock import patch, MagicMock


class TestNewObjectTasks:
    @patch('ansible.modules.read_csv')
    def test_new_object_csv_reading(self, mock_read_csv):
        """Test CSV reading for new objects."""
        mock_read_csv.return_value = {
            'list': [
                {'name': 'Test_Object', 'description': 'Test object'}
            ]
        }
        # Test implementation
```

## 📚 Documentation Standards

### 1. Code Documentation

```python
def create_dynamic_playbook(self, excel_file, detected_modules):
    """Create dynamic Ansible playbook based on detected modules.

    Args:
        excel_file (str): Path to source Excel file
        detected_modules (list): List of detected ACI modules

    Returns:
        str: Path to generated playbook file

    Raises:
        FileNotFoundError: If Excel file doesn't exist
        ValidationError: If modules are invalid

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

### 2. README Updates

- Update supported objects list
- Add examples for new features
- Update installation instructions if needed
- Add troubleshooting for new issues

### 3. Architecture Documentation

- Update `ARCHITECTURE.md` for structural changes
- Document new data flows
- Explain new dependencies

## 🔍 Code Review Process

### 1. Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive data included

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### 3. Review Criteria

**Code Quality**:
- Follows Python PEP 8 standards
- Proper error handling
- Clear variable/function names
- Appropriate comments

**Functionality**:
- Solves the stated problem
- Doesn't break existing features
- Handles edge cases
- Performance considerations

**Documentation**:
- Clear commit messages
- Updated documentation
- Code comments where needed
- Examples provided

## 🏷️ Release Process

### 1. Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 2. Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in appropriate files
- [ ] Git tag created
- [ ] Release notes written

## 💬 Community Guidelines

### 1. Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Respect different perspectives

### 2. Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code review and collaboration

### 3. Getting Help

- Check existing documentation first
- Search GitHub issues
- Ask in GitHub Discussions
- Provide minimal reproduction examples

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributor graphs
- Special mentions for significant contributions

Thank you for contributing to the ACI Fabric Automation Engine! 🎉