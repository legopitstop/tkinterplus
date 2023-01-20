# IDEAS
## DUMP
- Better Menu() - add bind text on right - better hover coloring (no margin)
- Photo Editor. A simple image editor widget using PIL and canvas to resize an image (pfp)
- Add support for `customtkinter`
- translate method to translate text using a locale JSON. Will attempt to get the user's locale.
- Universal animation class (both for widgets and canvas items) that can translate, rotate, or scale

## Icons - Change
- If the script is unable to download the icon (no internet, in offline mode or another issue) it should use the default "Missing" icon.
- It should create a new thread when it is downloading the icons. MaterialIconManager

## Windows

## Widgets
### WebFrame
A widget that can render websites. Similar to HTML's `iframe` tag. Needs a JavaScript interpreter.

When focused you can press "control-u" for view page source or "control-C" to open developer tools

Developer Tools
- tools to view the page source.

context menu
- reload (ctrl-r)
- --
- save as (ctrl-s)
- print (ctrl-p)
- cast
- --
- View page source (ctrl-u)
- Inspect (ctrl-C)

https://stackoverflow.com/questions/390992/javascript-parser-in-python
https://www.w3schools.com/tags/att_iframe_sandbox.asp
```py
widget = WebFrame(master, src="https://example.com", width=100, height=100) # tkinter.Canvas subclass
widget.configure(src='https://example.com') # if SRC is defined it should clear and re-render the webpage
widget.refresh() # re-renders the page.
widget.developer_tools() # Open developer tools (new popout window)
widget.pack(expand=1, fill='both')
# src:str - Source file
# srcdoc:str - The HTML doc to render. (view page source) (no scripts)
# width:int - widget width
# height:int - widget height
# allowfullscreen:bool - Set to true if the frame can activate fullscreen mode by calling requestFullscreen()
# sandbox:str - Enables extra set of restrictions: allow-forms, allow-pointer, allow-pointer-lock, allow-popups, allow-same-origin, allow-scripts, allow-top-navigation
# cache:bool:str - The folder to store the requests. When true: <working_dir>/.cache/...
# context_menu:bool - Use the default context_menu.
# __elements:str - The HTML for the page (with scripts)
```


### Notification
- Add 2 styles of notifications. One that slides in from a corner (anchor=NE) or pops up in the middle of the screen.
### Nav menu
A widget similar to Tab but can be expanded or iconified

### TextFormat

A Text Widget but with formatting buttons
`format` should be a supported MIME type

```python
var = StringVar()

t = TextFormat(master,format='html',variable=var)
t.grid()
```

### Canvas
A canvas with a simple 3D engine Mainly made for displaying models.
- Ambient occlusion
```python
canvas = tkinterplus.Canvas(master)
canvas.button_controls(panX='<Move>', panY='<Move>', panZ=None, rotX='<x>', rotY='<y>', rotZ='<z>')
canvas.mouse_controls(panX=True, panY=True, panZ=True, rotX=True, rotY=True, rotZ=True)
canvas.orbit_gizmo()

d3 = canvas.context('3d') # Add items to the 3D space
d3.add_cube(offset=(0,0,0), size=(1,1,1), textures=MateralInstances('north', 'south', 'east', 'west', 'up', 'down'), render_method='opaque|cutout|blend')

d2 = canvas.context('2d') # Allows you to add 2D items to the 3D space (Like a HUD)
d2.add_line()

canvas.grid()
```
- texture loading
- simple shading? (ambient occlusion)
- skybox
- raycast func?
- Render method for shapes

#### Based [three.js](https://threejs.org/docs/index.html#manual/en/introduction/Creating-a-scene)
```python
scene = THREE.Scene()
camera = THREE.PerspectiveCamera(75, width, height, 0.1, 1000)

renderer = THREE.WebGLRender()
renderer.setSize(width, height)

geometry = THREE.BoxGeometry(1, 1, 1)
materal = THREE.MeshBasicMateral(color: 'red')
cube = THREE.Mesh(geometry, materal)
scene.add(cube)

camera.position.z = 5

def animate():
    requestAnimationFrame(animate)

    cube.rotation.x += 0.01
    cube.rotation.y += 0.01
    renderer.render(scene, camera)

```

### Paragraph
A text that contains multiple lines of text. Can also have special formatting. ie. markdown, HTML, BBCode, etc
```python
p = Paragraph(master,textvariable)
p.configure()
```

### Link
Add clickable text that goes to a url. with target=_blank
```python
Link(master, url='', target=BLANK).grid()
```

### Form
submit command is the function to run when the user presses the submit button. if undefined it will not display the button. 
```python
f = Form()
f.add_entry(name)
f.add_text(name)
```
- Returns a diet that contains all the values.
- All options must have a `required` attribute. When true a value must be set for the form to be submitted, else it fails, default: False.
- Convert all option funds to use `def _option(self, type, *args, **kw):`

### Tabs
https://jqueryui.com/tabs/
bind buttons to display different pages.
```python
widget = Frame(root)
t = Tabs(root,orent)
t.add_tab(label, widget, command)
t.grid(row,colum)
```

## Dialogs
### TextEditor
A window is similar to Notepad which adds a few simple options.
```python
t = TextEditor(master, title='')
print(t)
```

### GitHub Issue
```python
import webbrowser

webbrowser.get('https://github.com/legopitstop/Datapacks/issues/new?title=%s&body=%s'%(TITLE, BODY))
issue = GitHubIssue(title='', prefix='', suffix='')

# Internal
issue._add(ENTRY, name, value)

# Default
issue.add_enum(name='Type', 'bug', 'feature')
issue.add_entry(name='Name', value='default') # Insert oneline text
issue.add_text(name='Name', value='default') # Insert Multiline text
issue.add_image(name='Name', value='URL') # Insert an image
issue.add_enum(name='Name', 'item 1', 'item 2') # Select an item from the list
issue.add_option(type='SYSTEM', cpu=True, gpu=True, platform=True, version=True) # Get the users system info
# issue.configure(title='')
```

### Config
Create a window with a bunch of customization options.
```python
c = Config(master, title='')

c.add_string(default='', pattern='')
c.add_boolean(default=None)
c.add_list(default='', 'item1', 'item2', 'item3')
c.add_integer(default='',min=0, max=0)
c.add_float(default='',min=0, max=0,multiple=False)
c.add_filename(default='', filetype='')
c.add_directory(default='')
c.add_color(default='')
```

### askenum
select a value from a list of values.
```python
ask = askenum(title, 'item1', 'item2')
```
