import os
import json

# download zip file from https://fontawesome.com/ and extract into fontawesome directory.
INPUT_FILE = os.path.join("fontawesome-free-6.5.1-desktop", "metadata", "icons.json")
# INPUT_FILE = os.path.join("fontawesome-pro-6.5.1-desktop", "metadata", "icons.json")
OUTPUT_FILE = 'fontawesome6.sty'

OUTPUT_HEADER = r'''
% Identify this package.
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{fontawesome6}[2024/01/06 v6.5.1 font awesome icons]
% Requirements to use.
\usepackage{fontspec}
% Configure a directory location for fonts(default: 'fonts/')
\newcommand*{\fontdir}[1][fonts/]{\def\@fontdir{#1}}
\fontdir
% Define pro option
\DeclareOption{pro}{
  % Define shortcut to load the Font Awesome pro font.
  \newfontfamily\FA[
    Path=\@fontdir,
    UprightFont=*-Regular-400,
    ItalicFont=*-Light-300,
    BoldFont=*-Solid-900,
    BoldItalicFont=*-Thin-100,
  ]{Font Awesome 6 Pro}
  \newfontfamily\FAduotone[
    Path=\@fontdir,
    UprightFont=*-Solid-900,
  ]{Font Awesome 6 Duotone}
  \newfontfamily\FAsharp[
    Path=\@fontdir,
    UprightFont=*-Regular-400,
    ItalicFont=*-Light-300,
    BoldFont=*-Solid-900,
    BoldItalicFont=*-Thin-100,
  ]{Font Awesome 6 Sharp}
}
\ProcessOptions\relax
% Define shortcut to load the Font Awesome font for brands.
\newfontfamily{\FAbrands}[Path=\@fontdir]{Font Awesome 6 Brands-Regular-400}
% Define shortcut to load the Font Awesome font.
\@ifundefined{FA}{%
\newfontfamily\FA[
  Path=\@fontdir,
  UprightFont=*-Regular-400,
  BoldFont=*-Solid-900,
]{Font Awesome 6 Free}
}{}
% Generic command displaying an icon by its name.
\def \ifempty#1{\def\temp{#1} \ifx\temp\empty }
\newcommand*{\faicon}[2][]{{
  \ifempty{#1}\csname faicon@#2\endcsname\else\csname faicon@#1@#2\endcsname\fi
}}
'''

OUTPUT_LINE = '\expandafter\def\csname faicon@%(type)s%(name)s\endcsname {%(font)s\symbol{"%(symbol)s}} \n'

def write_line(w, icon_name, icons, font, type):
    w.write(
        OUTPUT_LINE % {
            'name': icon_name,
            'symbol': icons[icon_name]["unicode"].upper(),
            'font': font,
            'type': type
        }
    )

def main():
    with open(INPUT_FILE, 'r') as json_data:
        icons = json.load(json_data)
        with open(OUTPUT_FILE, 'w') as w:
            w.write(OUTPUT_HEADER)
            for icon_name in sorted(icons.keys()):
                if "brands" in icons[icon_name]["styles"]:
                    font = "\FAbrands"
                    type = ""
                    write_line(w, icon_name, icons, font, type)
                if "duotone" in icons[icon_name]["styles"]:
                    font = "\FAduotone"
                    type = "duotone@"
                    write_line(w, icon_name, icons, font, type)
                if "regular" in icons[icon_name]["styles"]:
                    write_line(w, icon_name, icons, "\FA", "")
                    write_line(w, icon_name, icons, "\FAsharp", "sharp@")
            w.write(r'\endinput')


if __name__ == "__main__":
    main()
