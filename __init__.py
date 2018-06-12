import os
from cudatext import *
from cudax_lib import html_color_to_int
from .csv_proc import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_csv_hilite.ini')
MYTAG = 201
TIMERTIME = 150
TIMERCALL = 'module=cuda_csv_hilite;cmd=timer_tick;'

PALETTE = (0xFF0000,0x00AA00,0x0000FF,0x880000,0x004400,0x000088)
COLOR_COMMA = 0x000000

option_color_comma = '#000000'
option_colors_fixed = '#0000FF,#00AA00,#E00000,#000080,#004400,#900000,#909000'
option_colors_themed = 'Id,Id1,Id2,Id3,Id4,IdVar,String,Comment,Comment2,Label,Color'
option_use_theme_colors = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

_theme = app_proc(PROC_THEME_SYNTAX_DATA_GET, '')

def _theme_item(name):
    for i in _theme:
        if i['name']==name:
            return i['color_font']
    return 0x808080


class Command:

    def __init__(self):

        global option_color_comma
        global option_colors_fixed
        global option_colors_themed
        global option_use_theme_colors
        global PALETTE
        global COLOR_COMMA

        option_color_comma = ini_read(fn_config, 'op', 'color_comma', option_color_comma)
        option_colors_fixed = ini_read(fn_config, 'op', 'colors_fixed', option_colors_fixed)
        option_colors_themed = ini_read(fn_config, 'op', 'colors_themed', option_colors_themed)
        option_use_theme_colors = str_to_bool(ini_read(fn_config, 'op', 'use_theme_colors', bool_to_str(option_use_theme_colors)))

        if option_use_theme_colors:
            COLOR_COMMA = _theme_item('Symbol')
            PALETTE = [_theme_item(s) for s in option_colors_themed.split(',')]
        else:
            COLOR_COMMA = html_color_to_int(option_color_comma)
            PALETTE = [html_color_to_int(s) for s in option_colors_fixed.split(',')]

    def config(self):

        ini_write(fn_config, 'op', 'color_comma', option_color_comma)
        ini_write(fn_config, 'op', 'colors_fixed', option_colors_fixed)
        ini_write(fn_config, 'op', 'colors_themed', option_colors_themed)
        ini_write(fn_config, 'op', 'use_theme_colors', bool_to_str(option_use_theme_colors))
        file_open(fn_config)

    def on_open(self, ed_self):

        self.update()

    def on_scroll(self, ed_self):

        self.update()

    def on_change_slow(self, ed_self):

        self.update()

    def update(self):

        timer_proc(TIMER_STOP, TIMERCALL, 0)
        timer_proc(TIMER_START_ONE, TIMERCALL, TIMERTIME)

    def timer_tick(self, tag='', info=''):

        self.update_work()

    def update_work(self):

        ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)

        pagesize = ed.get_prop(PROP_VISIBLE_LINES)
        line1 = max(ed.get_prop(PROP_LINE_TOP) - pagesize, 0)
        line2 = min(ed.get_prop(PROP_LINE_BOTTOM) + pagesize, ed.get_line_count()-1)

        for line in range(line1, line2+1):
            s = ed.get_text_line(line)
            if not s: continue

            res = parse_csv_line(s)
            if not res: continue

            for x1, x2, kind in res:
                if kind<0:
                    ncolor = COLOR_COMMA
                else:
                    ncolor = PALETTE[kind%len(PALETTE)]

                ed.attr(MARKERS_ADD,
                    tag=MYTAG,
                    x=x1,
                    y=line,
                    len=x2-x1,
                    color_font=ncolor,
                    color_bg=COLOR_NONE,
                    )


    def get_header(self, n):

        s = ed.get_text_line(0)
        if not s: return
        res = parse_csv_line(s)
        if not res: return

        for x1, x2, kind in res:
            if kind==n:
                s = s[x1:x2]
                s = s.strip('"').replace('""', '"')
                return s


    def on_mouse_stop(self, ed_self, x, y):

        msg_status('')
        res = ed_self.convert(CONVERT_PIXELS_TO_CARET, x, y, '')
        if res is None: return
        x, y = res
        if y==0: return

        s = ed_self.get_text_line(y)
        if not s: return
        if x>=len(s): return

        res = parse_csv_line(s)
        if not res: return

        for x1, x2, kind in res:
            if x1<=x<x2:
                if kind>=0:
                    cap = self.get_header(kind) or '?'
                    msg_status('Column %d (%s)' % (kind+1, cap))
                break
