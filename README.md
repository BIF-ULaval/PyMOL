# PyMOL CHEATSHEET

## Official cheatsheet:
[Link here](https://pymolwiki.org/images/2/20/Refcard.png)

## Selection
- Select multiple residues:
```shell
select <new_select_name>, resi <indices>  # Example: <indices> = 10-18+33+81-83
```
- Select residues within X of selection:
```
select <new_sel_name>, byres (within 5 of <seletion>)
```

## Render
- Change the [ray trace mode](https://pymolwiki.org/index.php/Ray#Modes)
    ```shell
    set ray_trace_mode, 1  # For general outline effects when ray-tracing
    ```
  - Set the thinness of the outline
  ```shell
  set ray_trace_gain, 0.0-2.0  # Default is usually around 0.1-0.2
  ```
  - Change the color of the outline
  ```shell
  set ray_trace_color, magenta   # Example 1
  set ray_trace_color, 0x0033ff  # Example 2
  ```

## Coloring
- Color like Alphafold, see this extension:  [pymol-color-alphafold](https://github.com/cbalbin-bio/pymol-color-alphafold)
- Load a great color theme:
  Load the extension
  ```
  run https://raw.githubusercontent.com/BIF-ULaval/PyMOL/refs/heads/main/extensions/scientific_colors.py
  ```
- Color using hydrophobicity:
  1. Load the extension
  ```
  run <link>
  ```
  2. Run:
  ```
  color_hydro <sele | object>
  ```
- Set background color
```shell
  bg_color <color> # Example: bg_color white
  ```
- Change lighting
```shell
  set ambient, <value> # Where value can range between 0-1.
  ```

## TODO
Here are the next steps I want to do to improve this project
- [X] Understand how they add menus in PyMOL, and make an extension that use better colors [ref](https://github.com/smsaladi/pymol_viridis/blob/master/viridispalettes.py)
