# Security Policy

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability in the Caves of Steel project, please report it responsibly by **emailing security details privately** rather than disclosing them publicly in issues or pull requests.

### How to Report

1. **Do not** open a public GitHub issue describing the vulnerability
2. **Do not** create a pull request fixing the vulnerability (this reveals the issue publicly)
3. **Email** a detailed report to the repository maintainer with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### Expected Response Timeline

- **Initial acknowledgment**: Within 48 hours
- **Assessment and fix**: Within 14 days (or timeline for critical issues)
- **Public disclosure**: After patch is available or 90 days, whichever comes first
- **Release**: Security patch released as soon as fix is validated

---

## Security Considerations

### Input Validation

**Current Status**: ✅ Implemented
- Player input is validated and sanitized in `src/commands.py`
- All user-provided names are limited to 30 characters
- Save file paths are restricted to user's documents folder
- All command arguments are parsed and type-checked

**Best Practices**:
- User input is always treated as untrusted
- File operations are restricted to designated save directory
- No arbitrary code execution from player input

### Data Storage

**Current Status**: ✅ Secure
- Save files stored locally in user's home directory (`~/Documents/caves_of_steel/saves/`)
- Saves are JSON format (human-readable, no encoding vulnerabilities)
- Configuration stored locally in `game_config.json`
- No sensitive data encrypted (game progress is not sensitive)
- File permissions follow OS defaults

**Recommendations**:
- Save files should not contain passwords or API keys (none do currently)
- Keep save directory private (user-level permissions)
- Regularly backup save files if important

### Dependency Management

**Current Status**: ✅ Secure - No External Dependencies
- **Zero external dependencies**: Uses only Python standard library
- No package supply chain risks
- No vulnerable transitive dependencies
- All code is first-party

**Maintenance**:
- Requires Python 3.7+ (ensure system Python is up to date)
- No `requirements.txt` packages to audit
- No package manager attacks possible

### Code Quality & Safety

**Current Checks**:
- ✅ Syntax validation: `python3 -m py_compile`
- ✅ Linting: `ruff` configured for code style
- ✅ Code formatting: `black` for consistency
- ✅ Manual code review (before each commit)

**Tools Used**:
```
[tool.ruff]
line-length = 88

[tool.black]
line-length = 88

[tool.flake8]
max-line-length = 88
```

### Exception Handling

**Current Status**: ✅ Implemented
- All file operations wrapped in try-except
- Invalid inputs caught and handled gracefully
- No stack traces exposed to player
- Error messages are user-friendly

**Example**:
```python
try:
    self.game_state.relationships.get_relationship("NPC Name")
except Exception:
    pass  # Graceful fallback
```

### File Operations Security

**Current Status**: ✅ Restricted
- Save files only written to: `~/Documents/caves_of_steel/saves/`
- Load operations verify file exists before reading
- No path traversal attacks possible (paths validated)
- No world-readable save files by default

**Best Practices**:
```python
# Saves restricted to designated directory
save_path = os.path.join(save_dir, f"save_{timestamp}.json")
# No ../../../ traversal possible
```

### Session Security

**Current Status**: ✅ Stateless Design
- Game state stored locally in memory during play
- Save files are snapshots (no session IDs or tokens)
- No authentication required (single-player game)
- No network connections made

### Cryptography

**Current Status**: ℹ️ Not Applicable
- Game is fully offline, single-player
- No encryption needed for game data
- No sensitive user information stored
- No authentication or authorization system

---

## Security Best Practices for Users

### Safe Gameplay

1. **Backup Important Saves**
   - Saves stored in `~/Documents/caves_of_steel/saves/`
   - Periodically copy to backup location
   - Never share save files with untrusted sources

2. **Verify Game Files**
   - Clone only from official GitHub repository
   - Verify commit history: `git log --oneline`
   - Check source code before executing

3. **System Security**
   - Run with latest Python 3.7+ version
   - Keep your OS updated
   - Run malware scanner if downloading from untrusted source

### Environment Setup

```bash
# Secure installation steps
git clone https://github.com/goddardinho/caves_of_steel.git
cd caves_of_steel

# Create isolated Python environment
python3 -m venv venv
source venv/bin/activate

# Run the game
python3 main.py
```

---

## Security Guidelines for Contributors

### Code Review Requirements

Before submitting a pull request:

1. **No hardcoded secrets**
   - No API keys, passwords, or credentials in code
   - Use environment variables if external services added

2. **Input validation**
   - Always validate user-supplied data
   - Sanitize file paths
   - Limit input sizes

3. **Error handling**
   - Use try-except blocks around risky operations
   - Don't expose stack traces to end user
   - Log errors securely (not to player output)

4. **Dependency additions**
   - Justify any new external dependencies
   - Use only well-maintained, reputable packages
   - Pin versions to prevent unexpected updates

### Commit Security

```bash
# Sign commits (recommended but not required)
git config user.signingkey <YOUR_GPG_KEY_ID>
git commit -S -m "Secure commit message"

# Verify commit history
git log --show-signature
```

### Branch Protection

- Main branch (`main`) is protected
- All changes require pull request review
- CI/CD checks must pass before merge

---

## Known Security Limitations

### Accepted Risks

1. **No Encryption**
   - Save files are plain-text JSON
   - Acceptable because game data is non-sensitive

2. **No Update System**
   - Players must manually update from GitHub
   - Standard practice for indie projects

3. **No Telemetry**
   - Game collects no data about player behavior
   - No tracking or analytics
   - Aligns with privacy-first philosophy

### Out of Scope

The following are **not** security concerns for this project:
- Network security (game is offline)
- User authentication (single-player)
- Encryption (no sensitive data)
- Compliance (GDPR, HIPAA, etc.)

---

## Security Checklist for Releases

Before publishing a new release:

- [ ] All code passes `ruff` linting
- [ ] All code passes `black` formatting check
- [ ] All code compiles without syntax errors
- [ ] Demo mode runs without errors
- [ ] No hardcoded secrets in code
- [ ] No new external dependencies introduced
- [ ] No breaking changes to save file format
- [ ] CHANGELOG.md updated with all changes
- [ ] Git tags created and signed (optional)
- [ ] GitHub release notes published

---

## Contact & Support

### Reporting Issues

- **Bug Reports**: Use GitHub Issues (non-security bugs)
- **Security Vulnerabilities**: Email maintainer privately
- **Questions**: GitHub Discussions or Issues

### Maintainer

- **Repository**: https://github.com/goddardinho/caves_of_steel
- **Current Branch**: `0.4.0` (stable)
- **Last Security Review**: November 17, 2025

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-17 | 1.0 | Initial security policy document |

---

## Appendix: Security Tools Configuration

### Ruff Configuration (pyproject.toml)
```toml
[tool.ruff]
line-length = 88
```

### Black Configuration (pyproject.toml)
```toml
[tool.black]
line-length = 88
```

### .gitignore (Sensitive Files Protection)
```
saves/              # User save data
game_config.json    # User configuration
__pycache__/        # Compiled files
*.log              # Log files
.venv/             # Virtual environment
.env               # Environment variables (future-proofing)
```

### Safe Python Practices Used
- Input validation on all user-provided data
- Exception handling for all I/O operations
- No use of `eval()` or `exec()`
- No unpickling untrusted data
- Type hints for clarity

---

**Last Updated**: November 17, 2025  
**Policy Version**: 1.0  
**Status**: Active
