import os
from cudatext import *
from .csv_proc import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_csv_hilite.ini')
MYTAG = 201

PALETTE = (0xFF0000,0x00AA00,0x0000FF,0x880000,0x004400,0x000088)
COLOR_COMMA = 0x000000

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    
    def __init__(self):

        global option_int
        global option_bool
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):

        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)
        
    def on_open(self, ed_self):
    
        self.update()

    def on_scroll(self, ed_self):
    
        self.update()

    def on_change_slow(self, ed_self):
    
        self.update()

    def update(self):
    
        if ed.get_prop(PROP_LEXER_FILE, '') != 'CSV': return
        ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)
    
        line1 = ed.get_prop(PROP_LINE_TOP)
        line2 = ed.get_prop(PROP_LINE_BOTTOM)+1
        
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
