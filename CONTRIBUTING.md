# Contributing to Double Pendulum Art

We love your input! We want to make contributing to Double Pendulum Art as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any Contributions You Make Will Be Under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report Bugs Using GitHub's [Issue Tracker](https://github.com/mohidkhan/double-pendulum-art/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/mohidkhan/double-pendulum-art/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mohidkhan/double-pendulum-art.git
   cd double-pendulum-art
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests to make sure everything works:
   ```bash
   python tests/test_physics.py
   ```

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Before submitting a PR, please run:

```bash
black .
flake8 .
mypy pendulum_art/
```

### Code Style Guidelines

- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and small when possible
- Use type hints where appropriate
- Follow PEP 8 style guide

## Testing

- Write tests for new functionality
- Ensure existing tests still pass
- Aim for good test coverage of physics and core functionality

## Submitting Changes

1. **Create a descriptive branch name**: `feature/add-new-palette` or `bugfix/fix-physics-crash`
2. **Make your changes**: Keep commits focused and atomic
3. **Write good commit messages**: Use present tense ("Add feature" not "Added feature")
4. **Test your changes**: Run tests and manual testing
5. **Update documentation**: If you changed behavior, update README or docstrings
6. **Submit a pull request**: Include a clear description of what you changed and why

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] I have run the existing tests
- [ ] I have added new tests for my changes
- [ ] I have tested the changes manually

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] My changes generate no new warnings
```

## Ideas for Contributions

### Easy/Beginner
- Add new color palettes
- Improve error messages
- Add keyboard shortcuts
- Create new preset configurations
- Improve documentation

### Medium
- Add sound/music generation based on pendulum motion
- Implement different pendulum types (triple pendulum, elastic pendulum)
- Add animation export (GIF/MP4)
- Create a web interface
- Add physics parameter controls (gravity, damping, etc.)


## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing!

