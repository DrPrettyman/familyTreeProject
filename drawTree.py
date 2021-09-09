

def svg_rectangle(x, y, color, width=100, height=50):
    s = ''
    s += '\n\t<rect '
    s += 'x="{0}" y="{1}" rx="20" ry="20" width="{2}" height="{3}" '.format(x, y, width, height)
    s += '\n\tstyle="fill:{0};stroke:black;stroke-width:2;opacity:0.6" />'.format(color)
    return s


def svg_text(x, y, text, font_size=20):
    s = ''
    s += '\n\t<text font-size="{0}px" font-family="Verdana" x="{1}" y="{2}">'.format(font_size, x, y)
    s += '\n\t{}'.format(text)
    s += '\n\t</text>'
    return s


def text_len(text):
    length = 0
    for char in text:
    # 'abcdeghknopqrsuvxyz'
        if char in ' fijlt.,-':
            length += 0.5
        elif char in 'mw':
            length += 1.5
        else:
            length += 1
    return length*0.62


def svg_text_rectangle(x, y, color, text, width=200, height=50):

    font_size = 10
    text_length = text_len(text) * font_size

    midpoint = x + 0.5*width
    text_x = midpoint - 0.5*text_length
    text_y = y + 30

    s = svg_rectangle(x, y, color, width=width, height=height)
    s += svg_text(text_x, text_y, text, font_size=font_size)
    return s


def write_html():
    with open('ft.html', 'w', newline=None) as webpage:
        webpage.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Page Title</title>\n</head>\n<body>')
        webpage.write('\n')
        webpage.write('\n<svg width="1000" height="1000">')

        webpage.write(svg_text_rectangle(200, 60, 'red', 'Amber Prettyman'))
        webpage.write(svg_text_rectangle(200, 150, 'blue', 'Ruben'))

        webpage.write('\n\tSorry, your browser does not support inline SVG.')
        webpage.write('\n</svg>')
        webpage.write('\n')
        webpage.write('\n</body>\n</html>')


def draw_family_tree():
    ft_people, ft_unions = read_csv_files()
    draw_tree(ft_people, ft_unions)