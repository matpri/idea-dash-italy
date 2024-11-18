button_style = {
    'background': 'rgba(255,255,255,0.2)',
    'backdrop-filter': 'blur(5px)',
    'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.1)',
    'border': '1px solid rgba(255,255,255, 0.3)',
    '-webkit-backdrop-filter': 'blur(5px)',
    # size
    'height': '42px',
    'width': '42px',
    # padding
    'padding': '2px 2px',
}
glass_style = {
    'background': 'rgba(47,146,231,0.2)',
    'border-radius': '10px',
    'backdrop-filter': 'blur(5px)',
    'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.5)',
    'border': '1px solid rgba(47,146,231, 0.3)',
    '-webkit-backdrop-filter': 'blur(5px)',
    'padding': '4px 2px 4px 4px',
}

hide_button_style = button_style.copy()
hide_button_style['display'] = 'none'
hide_button_style['align-items'] = 'center'

view_button_style = button_style.copy()
view_button_style['display'] = 'block'
view_button_style['align-items'] = 'center'
