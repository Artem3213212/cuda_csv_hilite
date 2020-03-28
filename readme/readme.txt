Plugin for CudaText.
For CSV (comma-separated values) and TSV (tab-separated values), plugin highlights
different columns in different colors.
Requires "CSV" and "TSV" pseudo lexers (plugin has these lexers as requirements
in Addon Manager, so they are usually auto-intalled).

Also plugin handles hovering mouse over text: it shows index/caption of current
column in the statubar (caption is read from the first line).

Plugin has several commands for manage columns.

Plugin has several options in config file. Call config by menu "Options / Settings-plugins / CSV Helper".

After changing config file perform a reload of opened CSV and TSV files in order
to apply new settings.

Authors:
  Alexey Torgashin (CudaText)
  Artem Gavrilov https://github.com/Artem3213212
  Oleh Lutsak https://github.com/OlehL
License: MIT
