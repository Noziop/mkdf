# MKDF Installation Guide

This guide explains how to install MKDF on your system.

## Prerequisites

To install and use MKDF, you will need:

- A Linux, macOS, or Windows system with WSL
- GCC or Clang
- Make
- pthread library (usually already installed on most systems)

## Installation from Source

### 1. Clone the Repository

```bash
git clone https://github.com/username/mkdf.git
cd mkdf
```

### 2. Compile

```bash
make
```

### 3. Install

For a system-wide installation (requires administrator permissions):

```bash
sudo make install
```

By default, this will install the binary in `/usr/local/bin`.

For a local installation (in your home directory):

```bash
make install PREFIX=~/.local
```

Make sure that `~/.local/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Verifying the Installation

To verify that MKDF has been correctly installed:

```bash
mkdf --version
```

This should display the MKDF version number.

## Installation with Custom Options

You can customize the installation with different Makefile options:

```bash
# Compilation with optimizations
make CFLAGS="-O2 -Wall -Wextra -pthread"

# Installation in a specific directory
make install PREFIX=/opt/mkdf
```

## Uninstallation

To uninstall MKDF:

```bash
# If installed with sudo make install
sudo make uninstall

# If locally installed
make uninstall PREFIX=~/.local
```

## Post-Installation Configuration

After installing MKDF, you can create an optional configuration file in your home directory:

```bash
mkdir -p ~/.config/mkdf
```

You can create a `~/.config/mkdf/config.ini` file with the following content:

```ini
[general]
default_dir=~/projects

[templates]
custom_template_dir=~/.config/mkdf/templates

[web]
port=8080
```

## Troubleshooting Common Issues

### Issue: Command Not Found

If you get a "command not found" error after installation:

1. Check that the installation directory is in your PATH
2. Try restarting your terminal
3. Check the permissions of the binary file

### Issue: Compilation Errors

If you encounter errors during compilation:

1. Make sure you have all the necessary dependencies
2. Check that you're using a recent version of GCC or Clang
3. On some Linux distributions, you might need to install the `build-essential` package

```bash
# On Debian/Ubuntu
sudo apt install build-essential

# On Fedora
sudo dnf install gcc make
```

### Issue: Runtime Errors

If you encounter errors at runtime:

1. Check that you have the necessary permissions on the directories where you're trying to create files
2. Make sure the system has enough disk space
3. In case of pthread-related error, verify that the library is correctly installed

## Updating

To update MKDF to the latest version:

```bash
cd mkdf
git pull
make clean
make
sudo make install  # or make install PREFIX=~/.local for a local installation
```

---

## Navigation

- [Back to Index](index.md)
- Next page: [Command Line Usage](cli_usage.md)
- [Web Interface](web_usage.md)