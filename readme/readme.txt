Plugin for CudaText.
For CSV (comma-separated values) and TSV (tab-separated values), plugin highlights
different columns in different colors.
Plugin creates "CSV ^" and "TSV ^" lexers at startup (without creating files, these
are 'virtual' in-memory lexers), and these lexers are used to detect data files.

Features:

* Plugin handles hovering mouse over text: it shows index/caption of current
column in the statubar (caption is read from the first line).

* Plugin has several commands for manage columns.

* Plugin has several options in config file. Call config by menu "Options / Settings-plugins / CSV Helper". Typical config file (in INI format) looks like this:

[op]
color_comma=#000000
colors_fixed=#0000FF,#00AA00,#E00000,#000080,#004400,#900000,#909000
colors_themed=Id,Id1,Id2,Id3,Id4,IdVar,String,Comment,Comment2,Label,Color
use_theme_colors=1
separator=,

After changing config file perform a reload of opened CSV and TSV files in order
to apply new settings.


Authors:
  Alexey Torgashin (CudaText)
  Artem Gavrilov https://github.com/Artem3213212
  Oleh Lutsak https://github.com/OlehL
License: MIT
