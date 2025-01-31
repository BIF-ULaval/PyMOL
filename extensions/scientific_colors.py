"""
Thank you to Shyam Saladi for his code for this extension: https://github.com/smsaladi/pymol_viridis/blob/master/viridispalettes.py
This extension has been inspired by his.
"""
from pymol import cmd, menu
import pymol
# ------------------------------------------------------ Setup ------------------------------------------------------- #
def _hex_to_rgb(hex_color):
    """Convert a hex color string to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip("#")  # Remove the '#' if present
    if len(hex_color) != 6:
        raise ValueError("Hex color must be in the format #RRGGBB")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _is_added():
    names = {c[0] for c in menu.all_colors_list}
    return "theme" in names

def _colorize_text(text):
    '''Colorizes text given a list of RGB color values (NNN format)
    '''
    palette = _cmap8
    text = list(text)
    palette = list(palette)

    palette.append(888)  # last character white again
    palette = palette[:min(len(palette), len(text))]
    for i, col in enumerate(palette):
        if text[i] == '(':
            text[i] = '\\%s%s' % ('888', text[i])
            break
        text[i] = '\\%s%s' % (col, text[i])

    return ''.join(text) + '\\888'

def _scientific_menu(self_cmd, sele):
    scientific_col = _colorize_text('scientific')

    r = [
        [2, 'Viridis:', ''],
        [1, scientific_col + '(elem C)',
            'cmd.spectrum("count", "scientific", selection="('+sele+') & elem C")'   ],
        [1, scientific_col + '(*/CA)'  ,
            'cmd.spectrum("count", "scientific", selection="('+sele+') & */CA")'     ],
        [1, scientific_col             ,
            'cmd.spectrum("count", "scientific", selection="'+sele+'", byres=1)'     ],
        [0, '', ''],
        [1, 'b-factors'             ,
            'cmd.spectrum("b", "scientific", selection=("'+sele+'"), quiet=0)'       ],
        [1, 'b-factors(*/CA)'       ,
            'cmd.spectrum("b", "scientific", selection="(('+sele+') & */CA)", quiet=0)'],
        [0, '', ''],
        [1, 'area (molecular)'      ,
            'util.color_by_area(("'+sele+'"), "molecular", palette="scientific")'    ],
        [1, 'area (solvent)'        ,
            'util.color_by_area(("'+sele+'"), "solvent", palette="scientific")'      ],
        ]
    with pymol.menu.menucontext(self_cmd, sele) as mc:
        r += [
            [0, '', ''],
            [1, 'user properties', [[ 2, 'User Properties:', '' ]] + [
                [ 1, key, [[ 2, 'Palette', '' ]] + [
                    [1, palette, 'cmd.spectrum("properties[%s]", "%s", "%s")' % (repr(key), palette, sele)]
                    for palette in ('viridis', 'blue white red', 'green red')
                ]] for key in mc.props
            ]],
        ]
    return r


def _by_chain_patch(self_cmd, sele):
    by_chain_col = _colorize_text('by chain')
    by_segi_col = _colorize_text('by segi ')
    chainbows_col = _colorize_text('chainbows')

    r = pymol.menu._by_chain(self_cmd, sele) + [
        [0, '', ''],
        [0, '', ''],
        [1, by_chain_col + '(elem C)',
         'util.color_chains("(' + sele + ' and elem C)", palette="scientific", _self=cmd)'],
        [1, by_chain_col + '(*/CA)',
         'util.color_chains("(' + sele + ' and name CA)", palette="scientific", _self=cmd)'],
        [1, by_chain_col,
         'util.color_chains("(' + sele + ')", palette="scientific", _self=cmd)'],
        [0, '', ''],
        [1, chainbows_col,
         'util.chainbow("(' + sele + ')", palette="scientific", _self=cmd)'],
        [0, '', ''],
        [1, by_segi_col + '(elem C)',
         'cmd.spectrum("segi", "scientific", "(' + sele + ') & elem C")'],
        [1, by_segi_col,
         'cmd.spectrum("segi", "scientific", "' + sele + '")'],
    ]
    return r

def _color_auto_patch(self_cmd, sele):
    by_obj_col = _colorize_text('by obj')
    by_obj_c_col = _colorize_text('by obj(elem C)')
    chainbows_col = _colorize_text('chainbows')
    r = pymol.menu._color_auto(self_cmd, sele) + [
        [ 0, '', ''],
        [ 1, by_obj_col,
          'util.color_objs("('+sele+' and elem C)", palette="scientific", _self=cmd)'],
        [ 1, by_obj_c_col,
          'util.color_objs("('+sele+')", palette="scientific", _self=cmd)'],
        ]
    return r


def _mol_color_patch(self_cmd, sele):
    scientific_col = _colorize_text('scientific')
    with pymol.menu.menucontext(self_cmd, sele):
        for i, item in enumerate(pymol.menu._mol_color(self_cmd, sele)):
            _, text, _ = item
            if text == 'auto':
                auto_menu_idx = i
                break

        r = pymol.menu._mol_color(self_cmd, sele)
        r.insert(auto_menu_idx - 1, [1, scientific_col, _scientific_menu(self_cmd, sele)])
        return r

# ---------------------------------------------------- Constants ----------------------------------------------------- #
scientific_colors = {
        "Red": "#FA6967",
        "Pink": "#EF9B89",
        "Cyan": "#53BBC6",
        "Blue": "#4B8EC6",
        "Green": "#A2BB40",
        "Grey": "#515151",
        "Yellow": "#FCDDA4",
        "Purple": "#8087B8",
        "Light Grey": "#D5D5D5"
}

cmap = ['#f4d4b3', '#f4d4b3', '#f4d3b3', '#f4d3b3', '#f4d2b3', '#f4d2b3', '#f3d1b3', '#f3d1b3', '#f3d1b3', '#f3d0b3',
        '#f3d0b3', '#f3cfb3', '#f3cfb3', '#f3ceb2', '#f3ceb2', '#f3ceb2', '#f2cdb2', '#f2cdb2', '#f2ccb2', '#f2ccb2',
        '#f2ccb2', '#f2cbb2', '#f2cbb2', '#f2cab2', '#f2cab2', '#f2c9b2', '#f2c9b2', '#f1c9b2', '#f1c8b2', '#f1c8b2',
        '#f1c7b2', '#f1c7b2', '#f1c6b2', '#f1c6b2', '#f1c6b2', '#f1c5b2', '#f1c5b2', '#f1c4b2', '#f0c4b2', '#f0c3b1',
        '#f0c3b1', '#f0c3b1', '#f0c2b1', '#f0c2b1', '#f0c1b1', '#f0c1b1', '#f0c1b1', '#f0c0b1', '#efc0b1', '#efbfb1',
        '#efbfb1', '#efbeb1', '#efbeb1', '#efbeb1', '#efbdb1', '#efbdb1', '#efbcb1', '#efbcb1', '#efbbb1', '#eebbb1',
        '#eebbb1', '#eebab1', '#eebab1', '#eeb9b1', '#eeb9b0', '#eeb8b0', '#eeb8b0', '#eeb8b0', '#eeb7b0', '#eeb7b0',
        '#edb6b0', '#edb6b0', '#edb6b0', '#edb5b0', '#edb5b0', '#edb4b0', '#edb4b0', '#edb3b0', '#edb3b0', '#edb3b0',
        '#ecb2b0', '#ecb2b0', '#ecb1b0', '#ecb1b0', '#ecb0b0', '#ecb0b0', '#ecb0b0', '#ecafb0', '#ecafb0', '#ecaeb0',
        '#ecaeaf', '#ebadaf', '#ebadaf', '#ebadaf', '#ebacaf', '#ebacaf', '#ebabaf', '#ebabaf', '#ebaaaf', '#ebaaaf',
        '#ebaaaf', '#eaa9af', '#eaa9af', '#eaa8af', '#eaa8af', '#eaa8af', '#eaa7af', '#eaa7af', '#eaa6af', '#eaa6af',
        '#eaa5af', '#eaa5af', '#e9a5af', '#e9a4af', '#e9a4af', '#e9a3ae', '#e9a3ae', '#e9a2ae', '#e9a2ae', '#e9a2ae',
        '#e9a1ae', '#e9a1ae', '#e9a0ae', '#e8a0ae', '#e89fae', '#e89fae', '#e89fae', '#e89eae', '#e79eae', '#e69eae',
        '#e59dae', '#e49dae', '#e39dae', '#e29dae', '#e19cae', '#e09cae', '#df9cae', '#de9bae', '#dd9bae', '#dc9bae',
        '#db9bae', '#da9aae', '#d99aae', '#d89aae', '#d79aaf', '#d699af', '#d599af', '#d499af', '#d399af', '#d298af',
        '#d198af', '#d098af', '#cf97af', '#ce97af', '#cd97af', '#cc97af', '#ca96af', '#c996af', '#c896af', '#c796af',
        '#c695af', '#c595af', '#c495af', '#c395af', '#c294af', '#c194af', '#c094af', '#bf93af', '#be93af', '#bd93af',
        '#bc93af', '#bb92af', '#ba92af', '#b992af', '#b892af', '#b791af', '#b691b0', '#b591b0', '#b491b0', '#b390b0',
        '#b290b0', '#b190b0', '#b08fb0', '#af8fb0', '#ae8fb0', '#ac8fb0', '#ab8eb0', '#aa8eb0', '#a98eb0', '#a88eb0',
        '#a78db0', '#a68db0', '#a58db0', '#a48db0', '#a38cb0', '#a28cb0', '#a18cb0', '#a08bb0', '#9f8bb0', '#9e8bb0',
        '#9d8bb0', '#9c8ab0', '#9b8ab0', '#9a8ab0', '#998ab0', '#9889b0', '#9789b0', '#9689b0', '#9589b1', '#9488b1',
        '#9388b1', '#9288b1', '#9187b1', '#8f87b1', '#8e87b1', '#8d87b1', '#8c86b1', '#8b86b1', '#8a86b1', '#8986b1',
        '#8885b1', '#8785b1', '#8685b1', '#8585b1', '#8484b1', '#8384b1', '#8284b1', '#8183b1', '#8083b1', '#7f83b1',
        '#7e83b1', '#7d82b1', '#7c82b1', '#7b82b1', '#7a82b1', '#7981b1', '#7881b1', '#7781b1', '#7681b1', '#7580b1',
        '#7480b2', '#7280b2', '#717fb2', '#707fb2', '#6f7fb2', '#6e7fb2', '#6d7eb2', '#6c7eb2', '#6b7eb2', '#6a7eb2',
        '#697db2', '#687db2', '#677db2', '#667db2', '#657cb2', '#647cb2']

_cmap8 = tuple(dict.fromkeys(f'{int(10*_hex_to_rgb(c)[0]/256)}{int(10*_hex_to_rgb(c)[1]/256)}{int(10*_hex_to_rgb(c)[2]/256)}' for c in cmap))

# --------------------------------------------------- Build Menu ----------------------------------------------------- #

def def_theme_palette():
    '''Add the color blind-friendly colormaps/palettes to PyMOL.'''
    def format_colors(values):
        return ' '.join(values).replace('#', '0x')

    pymol.viewing.palette_colors_dict["scientific"] = format_colors(cmap)

    return
def def_theme_colors():
    """
    Defines theme colors in PyMOL.
    """
    # Define the colors in PyMOL
    for name, color in scientific_colors.items():
        rgb = [c/255 for c in _hex_to_rgb(color)]
        cmd.set_color(f'theme_{name}', rgb)



def add_scientific_color_menu():
    """
    Extends PyMOL's color menu by adding the "Scientific Colors" submenu.
    """

    colors = [(f'theme_{name}', _hex_to_rgb(co)) for name, co in scientific_colors.items()]

    # Update the color menu
    menu.all_colors_list.append(
        ('theme', [
            (f'{int(10*r/256)}{int(10*g/256)}{int(10*b/256)}', name) for name, (r, g, b) in colors
        ])
    )


def add_scientific_cmap_menu():
    '''Add viridis options to the PyMOL OpenGL menus where spectrum options exist
    '''

    # Abort if PyMOL is too old.
    try:
        from pymol.menu import all_colors_list
    except ImportError:
        print('PyMOL version too old for palettes menus. Requires 1.6.0 or later.')
        return

    # These will each be monkey-patched
    pymol.menu._by_chain = pymol.menu.by_chain
    pymol.menu._mol_color = pymol.menu.mol_color
    pymol.menu._color_auto = pymol.menu.color_auto

    # Add the menu
    pymol.menu.by_chain = _by_chain_patch
    pymol.menu.mol_color = _mol_color_patch
    pymol.menu.color_auto = _color_auto_patch

    return

def init():
    if not _is_added():
        # Define static colors
        def_theme_colors()
        # Define the cmap
        def_theme_palette()

        # Add the menus to the gui
        add_scientific_color_menu()
        add_scientific_cmap_menu()
        print("Successfully added color menus")
    else:
        print("Color menus already added")

init()