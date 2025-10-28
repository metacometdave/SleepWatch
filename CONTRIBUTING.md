# Contributing to SleepWatch

Thanks for your interest in contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

Found a bug? Please open an issue with:
- Your macOS version
- Steps to reproduce
- What you expected vs what happened
- Any error messages

### Suggesting Features

Have an idea? Open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Why it would be useful to others

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly** - Run the app and make sure everything works
5. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/SleepWatch.git
cd SleepWatch

# Install dependencies
brew install blueutil
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
python sleepwatch.py
```

## Code Style

- Follow PEP 8 for Python code
- Use clear, descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Before submitting:
- Test on your Mac by running the app
- Try sleep/wake cycles to ensure functionality works
- Check that all menu options work as expected

## Questions?

Feel free to open an issue for any questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
