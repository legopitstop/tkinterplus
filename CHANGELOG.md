# Changelogs

## 1.1.0 - dd/mm/yyyy
- Icon has now been changed to accept a file path to an image or any built-in icons ex: Asset.TK_PLUME
- Added MaterialIcon to download and use any Google Material. NOTE that you may want to add GitHub auth to not get rate limited. (max of 60 uses per hr)
    - Add `GITHUB_TOKEN = 'YOUR_TOKEN'` to your .env file (replace `YOUR_TOKEN` with your access token) to use that token for all material icons

- To use any experimental widget you will need to import them seperatly
    ```py
    from tkinterplus.experimental import *
    ```

### New Widgets
- `Notification`
- `Tabs`

### Widget Changes/Fixes
- Input now uses the tkinterplus tooltip instead of the tktooltip.
- You can now add images to Accordions.
- Footer:
    - You can now add widgets next to the buttons in the footer.
    - Should now use the correct geometry method (grid or pack) depending on the method that is already being used. Will use grid if empty.
- Modal:
    - Should now be centered in the window when it opens for the first time.
    - The modal will now change its title bar depending on the platform: Windows, Linux, Darwin
- TextEditor:
    - It will now change its appearance depending on the platform to look like it's native editor:
        - Windows: Notepad
        - Linux: Vi
        - Darwin: TextEdit
- 
## 1.0.0 - 10/23/2022
- Initial Release