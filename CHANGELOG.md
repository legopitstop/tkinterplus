# Changelogs
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - unreleased
- GridFrame and ScrollableGridFrame have been moved out of the experimental submodule. 

## [1.1.0] - 10/23/2022

### General
- `Icon` has now been changed to accept a file path to an image or any built-in icons ex: Asset.TK_PLUME
- Added MaterialIcon to download and use any [Google Material Icons](https://fonts.google.com/icons?selected=Material+Icons). NOTE that you may want to add GitHub auth to not get rate limited. (max of 60 uses per hr)
    - Add `GITHUB_TOKEN = 'YOUR_TOKEN'` to your .env file (replace `YOUR_TOKEN` with your access token) to use that token for all material icons
- Added Animations for animating your widgets and canvas items.

- To use any experimental widget you will need to import them separately. Doing so will print a warning message in the console.
    ```py
    from tkinterplus.experimental import *
    ```
- 

### Breaking Changes
- Renamed `Picture` to `Picturebox`

### New
- BaseWidgetPlus
- BindButton
- FileButton
- DirectoryButton
- ColorButton

### Experimental
- Notification
- Carousel
- WebFrame
- DeveloperTools

### Changes/Fixes
- Removed tabs widget. Use ttk.Notebook instead
- You can now add images to Accordions.

#### Tooltip
- tkinterplus tooltip is now a subclass to tktooltip.ToolTip for textvariable support.

#### `Input`
- Renamed to "EntryTypes" however "Input" can still be used.
- Renamed `text` type to `short` and `number` type to `integer`
- New types `keybind`, `long`, `float`

#### `Footer`:
- You can now add widgets next to the buttons in the footer.
- Should now use the correct geometry method (grid or pack) depending on the method that is already being used. Will use grid if geometry is not used.

#### `Modal`:
- Should now be centered in the window when it opens for the first time.
- The modal will now change its title bar depending on the platform: Windows, Linux, Darwin.
- Resizing the master window will now stick to the side instead of moving "outside" the window
- Modal hitbox now uses a "clamp" method.

#### `TextEditor`: - This should get undone.
- It will now change its appearance depending on the platform to look like it's native editor:
    - Windows: Notepad
    - Linux: Vi
    - Darwin: TextEdit
- ``

## [1.0.0] - 10/23/2022
- Initial Release
