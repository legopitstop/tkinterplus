# IDEAS
## DUMP
- Better Menu() - add bind text on right - better hover coloring (no margin)
- Photo Editor. A simple image editor widget using PIL and canvas to create, or edit an image.
- Add support for customtkinter
- Tooltip using Frame.place() to create a 100% custom tooltip. Could also include a sub-widget that simply has the label already inside for displaying text tips.
- translate method to translate text using a locale JSON. Will attempt to get the user's locale.

## Widgets
### Nav menu
A widget similar to Tab but can be expanded or iconified

### TextFormat

A Text Widget but with formatting buttons
```python
var = StringVar()

t = TextFormat(master,format='html',variable=var)
t.grid()

```

### Canvas3D
A canvas with a simple 3D engine Mainly made for displaying models.
- Ambient occlusion
```python
canvas = Canvas3D(master)
canvas.button_controls(panX='<Move>', panY='<Move>', panZ=None, rotX='<x>', rotY='<y>', rotZ='<z>')
canvas.mouse_controls(panX=True, panY=True, panZ=True, rotX=True, rotY=True, rotZ=True)
canvas.orbit_gizmo()

d3 = canvas.context('3d') # Add items to the 3D space
d3.add_cube(offset=(0,0,0), size=(1,1,1), textures={'north', 'south', 'east', 'west', 'up', 'down'}, render_method='opaque|cutout|blend')

d2 = canvas.context('2d') # Allows you to add 2D items to the 3D space (Like a HUD)
d2.add_line()

canvas.grid()

```
- texture loading
- simple shading? (ambient occlusion)
- skybox
- raycast func?
- Render method for shapes

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
