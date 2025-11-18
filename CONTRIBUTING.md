# Contributing to AWS Incident Co-Pilot

Thank you for your interest in contributing to AWS Incident Co-Pilot! We appreciate your time and effort to help make this project better.

## 🌟 How to Contribute

There are many ways to contribute to this project:

### ⭐ Star the Repository
The simplest way to show support is to star this repository! It helps others discover the project and motivates the maintainers.

### 🐛 Report Bugs
If you find a bug, please [open an issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new) with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, Node.js version)
- Any relevant error messages or logs

### 💡 Suggest Features
Have an idea for a new feature? We'd love to hear it! Please [open an issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new) with:
- A clear description of the feature
- The problem it solves
- How it would benefit users
- Any implementation ideas (optional)

### 📖 Improve Documentation
Documentation improvements are always welcome! You can:
- Fix typos or clarify existing docs
- Add examples or tutorials
- Improve API documentation
- Translate documentation

### 🔧 Submit Code

We welcome code contributions! Follow the guide below to submit your changes.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 20 or higher
- Git
- AWS account (for testing)

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/aws-incident-copilot.git
   cd aws-incident-copilot
   ```

3. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -e ".[dev]"
   ```

4. **Set up Node.js environment**
   ```bash
   npm install
   ```

5. **Configure AWS credentials** (for testing)
   ```bash
   # Set environment variables
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_DEFAULT_REGION=us-east-1
   ```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Use descriptive branch names:
- `feature/add-dynamodb-detector` for new features
- `fix/cloudwatch-timeout` for bug fixes
- `docs/improve-readme` for documentation
- `refactor/cleanup-detectors` for refactoring

### 2. Make Your Changes

Follow our coding standards (see below).

### 3. Test Your Changes

```bash
# Run Python tests
pytest -v --cov=copilot

# Run Python linting
ruff check .
black --check .

# Run Next.js tests
npm run build
npm run lint

# Type checking
npx tsc --noEmit
```

### 4. Commit Your Changes

Write clear, concise commit messages:

```bash
git add .
git commit -m "Add DynamoDB throttling detector"
```

Good commit message examples:
- `Add: DynamoDB throttling detection`
- `Fix: CloudWatch timeout on large metrics`
- `Docs: Update deployment guide for Vercel`
- `Refactor: Simplify incident serialization`

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then:
1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill in the PR template with details
4. Submit the pull request

## 🎯 Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all functions
- Write docstrings for classes and functions
- Keep functions small and focused
- Use meaningful variable names
- Format code with [Black](https://black.readthedocs.io/)
- Lint with [Ruff](https://docs.astral.sh/ruff/)

Example:
```python
def detect_cpu_spike(
    instance_id: str,
    threshold: float = 95.0,
    duration_minutes: int = 10
) -> Optional[Incident]:
    """
    Detect CPU spikes for an EC2 instance.

    Args:
        instance_id: EC2 instance ID
        threshold: CPU percentage threshold (default: 95.0)
        duration_minutes: Minimum duration in minutes (default: 10)

    Returns:
        Incident if detected, None otherwise
    """
    # Implementation here
    pass
```

### TypeScript/JavaScript

- Use TypeScript strict mode
- Provide full type annotations
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful prop names

Example:
```typescript
interface IncidentCardProps {
  incident: Incident;
  onDismiss?: (id: string) => void;
}

export function IncidentCard({ incident, onDismiss }: IncidentCardProps) {
  // Implementation here
}
```

### Testing

- Write tests for all new features
- Maintain >80% code coverage
- Use descriptive test names
- Test edge cases and error conditions

Example:
```python
def test_cpu_spike_detector_high_threshold():
    """Test CPU spike detection with threshold exceeded."""
    detector = CPUSpikeDetector()
    incident = detector.detect(instance_id="i-123", cpu_usage=98.5)
    assert incident is not None
    assert incident.severity == "HIGH"
```

## 🔒 Security Guidelines

- **Never commit credentials** or sensitive data
- Use environment variables for configuration
- All AWS operations must be **read-only**
- Sanitize error messages to avoid data leaks
- Follow the principle of least privilege

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows style guidelines (Black, Ruff, ESLint)
- [ ] All tests pass (`pytest`, `npm run build`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No credentials or sensitive data in code
- [ ] PR description explains the changes

## 🏅 Recognition

All contributors will be:
- Listed in the contributors section
- Credited in release notes
- Appreciated by the community!

## 📞 Questions?

If you have questions about contributing:
- Check existing [issues](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues)
- Open a [new issue](https://github.com/JavierHernandezVantuyl/aws-incident-copilot/issues/new)
- Reach out to maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to AWS Incident Co-Pilot! Your efforts help make AWS infrastructure management easier for everyone. 🚀
