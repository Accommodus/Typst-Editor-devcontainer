# Typst Editor Devcontainer

## Features

* **Base Image**: Debian Bookworm
  
* Pre-installed Tools:
  * [Pandoc](https://pandoc.org/): Universal document converter
  * [LaTeX](https://www.latex-project.org/): Typesetting system with `chktex` for style checking
  * [Typst](https://typst.app/): Markup-based typesetting for technical documents
  * [Rust](): : {for compile typst modules}
  * [wasm32-unknown-unknown](): {for compile typst modules}
    
* VSCode Extensions:
  * From Features:  
   * Tinymist Typst by Myriad Dreamin
   * CodeLLDB by Vadim Chugunov
   * Even Better TOML by tamasfe
   * rust-analyzer by The Rust Programming Language

  * Manually Specified
   * Typst Companion by Caleb Figgers
   * Typst Math by Julien THILLARD
   * Typst Sync by OrangeX4
   * Code Spell Checker by Street Side Software

* Preconfigured Settings:
  * The editing enviornment has been configured to be good for both developing source code and drafting text.

## Installation

The structure of this repository is designed to be most effectively used as a submodule or as a subdirectory within a larger repository or project.

### If This Is Your Only Dev Container

Add this Dev Container directly as your `.devcontainer` folder:

1. Navigate to your project’s root directory.
  
1. Add the Dev Container as a submodule:
   ```bash
   git submodule add \$TYPST_DEVCON_URL .devcontainer
   ```
   
1. Initialize and update the submodule:
   ```bash
   git submodule update --init --recursive
   ```

### If You Want Multiple Dev Containers

If you want to use more than one Dev Container in your project (for example, one for running code and this one for writing the associated paper):

1. Navigate to your project’s root directory.
   
1. `cd` into your project’s `.devcontainer` directory
   ```bash
   cd .devcontainer
   ```

1. Add the Dev Container as a submodule within this subdirectory:
   ```bash
   git submodule add \$TYPST_DEVCON_URL
   ```
   
1. Initialize and update the submodule:
   ```bash
   git submodule update --init --recursive
   ```
   
1. When reopening the project in a remote container, select the desired Dev Container configuration from the list.

## Usage
1. Open your project folder in Visual Studio Code.
2. Ensure the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) is installed.
3. Press `F1` or `Shift+Ctrl+P` to open the Command Palette and select `Dev Containers: Reopen in Container`.
4. VS Code will build and start the Dev Container. Once ready, you can begin working with Typst.
