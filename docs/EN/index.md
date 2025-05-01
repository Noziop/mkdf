# MKDF Documentation

Welcome to the documentation of MKDF (MaKeDir&Files), a powerful tool for creating directory and file structures.

## Table of Contents

- [Installation Guide](installation.md) - How to install MKDF on your system
- [Command Line Usage](cli_usage.md) - Complete guide to CLI commands and options
- [Web Interface](web_usage.md) - How to use the MKDF web interface
- [Project Templates](project_templates.md) - Available predefined templates
- [Use Cases](use_cases.md) - Practical examples of usage
- [Developer Guide](developer_guide.md) - Technical documentation for contributors

## What is MKDF?

MKDF is a flexible utility for quickly generating project structures using a concise expansion syntax. It offers:

- An intuitive command-line interface
- A user-friendly web interface
- A powerful brace expansion syntax
- Predefined templates for different project types
- Support for relative and absolute paths

## Getting Started with MKDF

To start using MKDF:

1. Check the [Installation Guide](installation.md) to install the tool
2. Explore the [Command Line Usage](cli_usage.md) or the [Web Interface](web_usage.md) documentation
3. Discover the [Use Cases](use_cases.md) for concrete examples

## Quick Examples

Create a simple structure:
```bash
mkdf 'my-project/{src/,docs/,tests/}'
```

Use a predefined template:
```bash
mkdf -c my-app react
```

Launch the web interface:
```bash
mkdf --web
```