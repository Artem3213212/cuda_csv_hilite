import os
import cudatext as ct
import cudatext_cmd
from cudax_lib import html_color_to_int
from .csv_proc import parse_csv_line, parse_csv_line_as_dict
# from debug import snoop


fn_config = os.path.join(ct.app_path(ct.APP_DIR_SETTINGS), "cuda_csv_hilite.ini")
MYTAG = 201
TIMERTIME = 150
TIMERCALL = "module=cuda_csv_hilite;cmd=timer_tick;"
LEXER_CSV = "CSV ^"
LEXER_TSV = "TSV ^"

PALETTE = (0xFF0000, 0x00AA00, 0x0000E0, 0x800000, 0x004400, 0x000090, 0x009090)
COLOR_COMMA = 0x000000

option_color_comma = "#000000"
option_colors_fixed = "#0000FF,#00AA00,#E00000,#000080,#004400,#900000,#909000"
option_colors_themed = "Id,Id1,Id2,Id3,Id4,IdVar,String,Comment,Comment2,Label,Color"
option_use_theme_colors = True


def msg(s):
    ct.msg_status('CSV Helper: '+s)


def bool_to_str(v):
    return "1" if v else "0"


def str_to_bool(s):
    return s == "1"


_theme = ct.app_proc(ct.PROC_THEME_SYNTAX_DICT_GET, "")


def _theme_item(name):
    if name in _theme:
        return _theme[name]["color_font"]
    else:
        return 0x808080


class Command:
    def __init__(self):

        global option_color_comma
        global option_colors_fixed
        global option_colors_themed
        global option_use_theme_colors

        option_color_comma = ct.ini_read(
            fn_config, "op", "color_comma", option_color_comma
        )
        option_colors_fixed = ct.ini_read(
            fn_config, "op", "colors_fixed", option_colors_fixed
        )
        option_colors_themed = ct.ini_read(
            fn_config, "op", "colors_themed", option_colors_themed
        )
        option_use_theme_colors = str_to_bool(
            ct.ini_read(
                fn_config,
                "op",
                "use_theme_colors",
                bool_to_str(option_use_theme_colors),
            )
        )

        self.update_colors()

    def config(self):

        ct.ini_write(fn_config, "op", "color_comma", option_color_comma)
        ct.ini_write(fn_config, "op", "colors_fixed", option_colors_fixed)
        ct.ini_write(fn_config, "op", "colors_themed", option_colors_themed)
        ct.ini_write(fn_config, "op", "use_theme_colors", bool_to_str(option_use_theme_colors))
        ct.file_open(fn_config)

    def on_open(self, ed_self):

        self.ed_ = ed_self
        self.update()

    def on_scroll(self, ed_self):

        self.ed_ = ed_self
        self.update()

    def on_change_slow(self, ed_self):

        self.ed_ = ed_self
        self.update()

    def on_state(self, ed_self, state):

        global _theme

        if state == ct.APPSTATE_THEME_SYNTAX:
            _theme = ct.app_proc(ct.PROC_THEME_SYNTAX_DICT_GET, "")

            if self.update_colors():
                self.ed_ = ed_self
                self.update()

    def update(self):

        ct.timer_proc(ct.TIMER_STOP, TIMERCALL, 0)
        ct.timer_proc(ct.TIMER_START_ONE, TIMERCALL, TIMERTIME)

    def timer_tick(self, tag="", info=""):

        self.update_work()

    def update_colors(self):
        global PALETTE
        global COLOR_COMMA

        if option_use_theme_colors:
            COLOR_COMMA = _theme_item("Symbol")
            PALETTE = [_theme_item(s) for s in option_colors_themed.split(",")]
            return True
        else:
            COLOR_COMMA = html_color_to_int(option_color_comma)
            PALETTE = [html_color_to_int(s) for s in option_colors_fixed.split(",")]
            return False

    def get_sep(self, ed):

        lex = ed.get_prop(ct.PROP_LEXER_FILE, "")
        if lex==LEXER_TSV:
            return '\t'
        elif lex==LEXER_CSV:
            return ','
        else:
            return ''

    def update_work(self):

        ed = self.ed_  # used ed_self here
        sep = self.get_sep(ed)
        if not sep:
            return
        ed.attr(ct.MARKERS_DELETE_BY_TAG, tag=MYTAG)

        pagesize = ed.get_prop(ct.PROP_VISIBLE_LINES)
        line1 = max(ed.get_prop(ct.PROP_LINE_TOP) - pagesize, 0)
        line2 = min(ed.get_prop(ct.PROP_LINE_BOTTOM) + pagesize,
                    ed.get_line_count() - 1)

        for line in range(line1, line2 + 1):
            s = ed.get_text_line(line)
            if not s:
                continue

            res = parse_csv_line(s, sep=sep)
            if not res:
                continue

            for x1, x2, kind in res:
                if kind < 0:
                    ncolor = COLOR_COMMA
                else:
                    ncolor = PALETTE[kind % len(PALETTE)]

                ed.attr(
                    ct.MARKERS_ADD,
                    tag=MYTAG,
                    x=x1,
                    y=line,
                    len=x2 - x1,
                    color_font=ncolor,
                    color_bg=ct.COLOR_NONE,
                )

    def get_header(self, ed, n, sep):

        s = ed.get_text_line(0)
        if not s:
            return
        res = parse_csv_line(s, sep=sep)
        if not res:
            return

        for x1, x2, kind in res:
            if kind == n:
                s = s[x1:x2]
                s = s.strip('"').replace('""', '"')
                return s

    def on_mouse_stop(self, ed_self, x, y):

        ct.msg_status("")
        res = ed_self.convert(ct.CONVERT_PIXELS_TO_CARET, x, y, "")
        if res is None:
            return
        x, y = res
        if y == 0:
            return

        s = ed_self.get_text_line(y)
        if not s:
            return
        if x >= len(s):
            return

        sep = self.get_sep(ed_self)
        res = parse_csv_line(s, sep=sep)
        if not res:
            return

        for x1, x2, kind in res:
            if x1 <= x < x2:
                if kind >= 0:
                    cap = self.get_header(ed_self, kind, sep) or "?"
                    ct.msg_status("Column %d (%s)" % (kind + 1, cap))
                break

    # @snoop()
    def get_current_col(self, sep):
        carets = ct.ed.get_carets()
        if len(carets) > 1:
            msg('multi-carets not supported')
            return
        x0, y0, x1, y1 = carets[0]
        if x1 != -1 or y1 != -1:
            msg('selection not supported')
            return
        line = ct.ed.get_text_line(y0)
        for k, v in parse_csv_line_as_dict(line, sep=sep).items():
            if x0 >= v[0] and x0 <= v[1]:
                return k

    # @snoop()
    def current_col_do(self, what='del'):

        sep = self.get_sep(ct.ed)
        current_col = self.get_current_col(sep)
        if current_col is None:
            return
        lines = ct.ed.get_text_all().split('\n')

        carets = ct.ed.get_carets()
        cur_x0, cur_y0, _, _ = carets[0]

        new_text = []
        markers = []
        for y, line in enumerate(lines):
            _csv = parse_csv_line_as_dict(line, sep=sep)
            if not _csv:
                break
            last_col = max(_csv.keys())
            if last_col < current_col:
                msg('file contains a different number of columns')
                return
            x0, x1 = _csv[current_col]

            if what == 'new':
                new_text.append((x0, y))
                markers.append((x0, y, y))

            elif what == 'rnew':
                new_text.append((x1, y))
                markers.append((x1+1, y, y))

            elif what == 'del':
                if y == cur_y0:
                    cur_x0 = x0
                if current_col == 0:
                    new_line = line[:x0] + line[x1+1:]
                else:
                    new_line = line[:x0-1] + line[x1:]
                new_text.append(new_line)

            elif what == 'move_left':
                if current_col == 0:
                    break
                else:
                    prev_x0, prev_x1 = _csv[current_col-1]
                    if y == cur_y0:
                        cur_x0 = cur_x0 - x0 + prev_x0
                    new_line = line[:prev_x0] + line[x0:x1] +\
                        sep + line[prev_x0:prev_x1] + line[x1:]
                    new_text.append(new_line)

            elif what == 'move_right':
                if current_col == last_col:
                    break
                else:
                    next_x0, next_x1 = _csv[current_col+1]
                    if y == cur_y0:
                        cur_x0 = cur_x0 + next_x1 - next_x0 + 1
                    new_line = line[:x0] + line[next_x0:next_x1] +\
                        sep + line[x0:x1] + line[next_x1:]
                    new_text.append(new_line)

        ct.ed.markers(ct.MARKERS_DELETE_ALL)

        if what in ['new', 'rnew']:
            for s in new_text:
                ct.ed.insert(*s, sep)
            markers.reverse()
            for m in markers:
                ct.ed.markers(ct.MARKERS_ADD, *m)
            ct.ed.set_prop(ct.PROP_TAB_COLLECT_MARKERS, '1')
            ct.ed.cmd(cudatext_cmd.cmd_Markers_GotoLastAndDelete)

        elif what in ['del', 'move_left', 'move_right']:
            for i, s in enumerate(new_text):
                ct.ed.set_text_line(i, s)
            ct.ed.set_caret(cur_x0, cur_y0)

        self.update()

    def new_col(self):
        self.current_col_do('new')

    def rnew_col(self):
        self.current_col_do('rnew')

    def del_current_col(self):
        self.current_col_do('del')

    def move_left_current_col(self):
        self.current_col_do('move_left')

    def move_right_current_col(self):
        self.current_col_do('move_right')
