# Changelog

All notable changes to Minedetector will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.1] - 2026-01-27

### Bug Fixes
- Fix game over state properly disabling clicks without applying grayscale filter
- Correct import sorting in main.py
- Update PyInstaller version to 6.18.0 for successful builds
- Fix README.md typo (Minesweeper → Minedetector)

### CI/CD Improvements
- Install Qt system dependencies for headless testing (libegl1, libgl1, etc.)
- Update deprecated GitHub Actions (cache@v3 → v4, upload-artifact@v3 → v4)
- Set QT_QPA_PLATFORM=offscreen for headless Qt testing
- Remove strict coverage requirement to allow UI tests to skip in CI

### Testing & QA
- Add pre-commit hooks for code quality (black, isort, flake8, mypy)
- Fix failing tests and establish QA infrastructure
- Add conftest.py for pytest configuration
- Mark display-dependent tests to skip in headless CI environments
- Add 153 comprehensive unit tests with 100% core coverage

### Code Quality
- Run black and isort on entire codebase
- Remove unused imports and variables
- Fix f-strings without placeholders
- Fix line length issues in docstrings
- Add type annotations where missing

### Documentation
- Add release notes for v0.1.0
- Add Windows 95 authenticity plan documentation

## [v0.1.0] - 2026-01-26

### Initial Release
- Beginner, Intermediate, and Expert difficulty levels
- First-click safety (never click a mine on first attempt)
- Flood fill algorithm for blank cell revelation
- Chording (double-click to reveal adjacent cells when flags match)
- Flagging with right-click
- Timer and mine counter
- Game over detection (win/lose states)
- Windows 95 authentic styling
