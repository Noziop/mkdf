# MKDF Web Interface

This guide explains how to use the MKDF web interface to visually create directory and file structures.

## Starting the Web Interface

To launch the MKDF web interface, use the following command:

```bash
mkdf --web
# or
mkdf -w
```

By default, the web interface is accessible at http://localhost:8080

You can specify a different port using the `--port` or `-p` option:

```bash
mkdf --web --port 3000
# or
mkdf -w -p 3000
```

## Navigating the Web Interface

The MKDF web interface consists of several sections:

### Top Navigation Bar

- **Home**: Return to the main page
- **Documentation**: Links to MKDF documentation
- **Templates**: Access predefined templates
- **About**: Information about the MKDF project

### Main Panel

The main interface is divided into three sections:

1. **Expression Editor**: Area where you can enter your MKDF expression
2. **Structure Preview**: Tree visualization of the structure to be created
3. **Configuration Options**: Additional parameters for generation

## Using the Expression Editor

The expression editor allows you to enter an MKDF expression using the same syntax as the command line version:

1. Enter your expression in the text field
   ```
   project/{src/{models/,views/,controllers/},docs/,tests/}
   ```

2. Click the "Preview" button to visualize the structure that will be created

3. The preview will automatically update and display a tree representation of the structure

## Editing Modes

The web interface offers two editing modes:

### Text Mode

In this mode, you directly enter the MKDF expression as you would on the command line.

### Visual Mode

The visual mode allows you to build your directory and file structure using a drag-and-drop interface:

1. Click on "Visual Mode" to switch to the graphical editor
2. Use the "Add Folder" and "Add File" buttons to create your structure
3. Drag and drop elements to organize your tree
4. The corresponding MKDF expression will be generated automatically

## Interface Themes

MKDF offers different visual themes for the web interface:

1. **Light**: Default theme with white background
2. **Dark**: Dark mode for night use
3. **Girly**: Theme with pastel colors and rounded elements
4. **Minimalist**: Clean interface with minimal elements

To change the theme:

1. Click on the theme icon in the top right corner
2. Select your desired theme from the dropdown menu

## Predefined Templates

The web interface allows you to use the same predefined templates as the command line version:

1. Click on the "Templates" tab in the navigation bar
2. Select a template from the list:
   - Simple
   - Multi
   - Docker
   - FastAPI
   - Vue-Vite
   - Flask
   - React

3. A preview of the template structure will be displayed
4. Click "Use This Template" to apply it

## Customizing Templates

You can customize a template after selecting it:

1. Select a template from the list
2. Click on "Customize"
3. Modify the structure in the visual or text editor
4. Click "Apply Changes"

## Generation Options

The web interface offers several options for generating your structure:

### Generation Location

By default, the structure is generated in the current directory, but you can specify an absolute or relative path:

1. In the "Configuration Options" section, enter the path in the "Location" field
2. You can also click "Browse" to select a location

### Advanced Options

- **Verbose Mode**: Displays details about each operation
- **Simulation Mode**: Shows what would be created without actually doing it
- **Force Creation**: Overwrites existing files/folders
- **Ignore Errors**: Continues creation even if errors occur

## Export and Import

You can save and share your structures:

### Export

1. Create your structure in the editor
2. Click "Export" in the options menu
3. Choose the export format:
   - JSON
   - YAML
   - MKDF Expression
   - Shell Script

### Import

1. Click "Import" in the options menu
2. Select a previously exported file
3. The structure will be loaded into the editor

## Generating the Structure

Once you are satisfied with your structure:

1. Check the preview to make sure it matches your expectations
2. Configure the options as desired
3. Click the "Generate" button to create the structure
4. A notification will indicate whether the generation succeeded or failed

## Web Terminal

The web interface includes an integrated terminal for advanced operations:

1. Click on the "Terminal" tab in the bottom panel
2. You can execute MKDF commands directly
3. The terminal also displays generation logs

## Web API

MKDF also exposes a REST API that you can use to automate the creation of structures:

```
POST /api/generate
{
  "expression": "project/{src/,docs/,tests/}",
  "options": {
    "verbose": true,
    "force": false
  }
}
```

See the API documentation in the "API" section of the main menu for more details.

## Troubleshooting

### Structure is not generated

- Check that you have write permissions on the target location
- Make sure your expression syntax is correct
- Check the logs in the "Terminal" tab

### Web interface does not start

- Check that the specified port is not already in use
- Make sure you have the rights to bind to the port
- Check the startup logs

### Preview does not update

- Verify that your MKDF expression is valid
- Try refreshing the page
- Switch to text mode and then back to visual mode

## Keyboard Shortcuts

The MKDF web interface offers several keyboard shortcuts to speed up your workflow:

- `Ctrl+Enter`: Generate the structure
- `Ctrl+P`: Display preview
- `Ctrl+S`: Export the structure
- `Ctrl+O`: Import a structure
- `Ctrl+/`: Toggle between text mode and visual mode
- `Ctrl+H`: Display keyboard shortcut help

---

## Navigation

- [Back to Index](index.md)
- Related pages:
  - [Command Line Usage](cli_usage.md)
  - [Project Templates](project_templates.md)
- [Developer Guide](developer_guide.md)