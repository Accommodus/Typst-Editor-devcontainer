# Typst Editor Dev Container

**This editor is configured to look best with a font that is not pre-installed; see [Font Installation](#Font-Install) for details.**

This devcontainer provides a ready-to-use environment for editing and scripting Typst documents. It also supports development of Rust-based Typst modules. It comes pre-installed with Typst, Rust (including the wasm32-unknown-unknown target), Pandoc, and a set of extensions for both code and prose workflows. System-wide installation of all Google Fonts and the Monaspace family ensures consistent, high-quality typography for all documents, eliminating the need to manually add fonts.

## Installation

### If This Is Your Only Dev Container

Add this Dev Container directly as your `.devcontainer` folder:

1. Navigate to your project’s root directory.

1. Create the config file with the following content:

   ```bash
   echo '{ "image": "ghcr.io/accommodus/typst-editor-devcontainer:latest" }' > .devcontainer.json
   ```

### If You Want Multiple Dev Containers

If your project needs more than one Dev Container (for example, one for code and one for writing papers), you can organize each configuration in its own subdirectory:

1. Navigate to your project’s root directory.

1. Create the `.devcontainer/typst_editor/devcontainer.json` file with the following content::

   ```bash
   mkdir -p .devcontainer/typst_editor/ && echo '{ "image": "ghcr.io/accommodus/typst-editor-devcontainer:latest" }' > .devcontainer/typst_editor/devcontainer.json
   ```
   
1. When reopening the project, select the desired Dev Container configuration from the list.

<a id="Font-Install"></a>
### If You Want to Use Monaspace Xenon in Your Editor
Instructions based on your operating system. [See this.](https://github.com/githubnext/monaspace?tab=readme-ov-file#desktop-installation)

## Usage

1. Open the project in VS Code
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Press `F1` or `Shift+Ctrl+P` to open the Command Palette and select `Dev Containers: Reopen in Container`.
4. You are ready to use Typst.

## Features

* Base Image: Debian Bookworm

* Pre-installed Tools:

  * [Pandoc](https://pandoc.org/): Universal document converter
  * [Git](https://git-scm.com/): Version control system
  * [Typst](https://typst.app/): Markup-based typesetting for technical documents
  * [Rust](https://www.rust-lang.org/): Language used to compile Typst modules
  * [wasm32-unknown-unknown](https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html): WebAssembly compilation target for Typst modules

* Fonts Installed in Container:

  * All Google Fonts: [broad typographic choice](https://github.com/google/fonts)
  * GitHub Monaspace Family: [(Neon, Argon, Xenon, Radon, Krypton) — modern variable monospace with advanced “texture healing”](https://github.com/githubnext/monaspace)


## Preconfigured Settings

The editor settings are tailored to create an ideal environment for both scripting and drafting documents in Typst.

* Uses the **Monaspace Xenon** font if installed (with ligatures and weight 500) for a modern, consistent look across code and prose.
* Font size set to 16 px for comfortable, accessible reading and editing.
* Automatic formatting on save ensures consistent code style.
* Editor wraps lines for easier reading and editing of long paragraphs or code.

## VS Code Extensions

* From features

  * Tinymist Typst (Myriad Dreamin)
  * CodeLLDB (Vadim Chugunov)
  * Even Better TOML (tamasfe)
  * rust-analyzer (The Rust Programming Language)

* Manually Included

  * Typst Companion (Caleb Figgers)
  * Typst Math (Julien THILLARD)
  * Typst Sync (OrangeX4)
  * Code Spell Checker (Street Side Software)
