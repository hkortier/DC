"""
An IPython extension for generating circuit diagrams using LaTeX/Circuitikz
from within ipython notebook.
"""
import os
from IPython.core.magic import magics_class, cell_magic, Magics
from IPython.display import Image, SVG

#%\usepackage[paperwidth=%s,paperheight=%s,margin=0in]{geometry}
latex_template = r"""\documentclass{standalone}
\usepackage{tikz}
\usepackage[%s]{circuitikz}
\begin{document}
%s
\end{document}
"""

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

@magics_class
class Circuitikz(Magics):

    @cell_magic
    def circuitikz(self, line, cell):
        """Generate and display a circuit diagram using LaTeX/Circuitikz.
        
        Usage:
        
            %circuitikz [key1=value1] [key2=value2] ...

            Possible keys and default values are

                filename = ipynb-circuitikz-output
                dpi = 100 (for use with format = png)
                options = europeanresistors,americaninductors
                format = svg (svg or png)

        """
        options = {'filename': 'ipynb-circuitikz-output',
                   'dpi': '100',
                   'format': 'png',
                   'options': 'europeanresistors,americaninductors',
                   'folder' : 'circuits/',
                   'replace': 'true'}


        for option in line.split(" "):
            try:
                key, value = option.split("=")
                if key in options:
                    options[key] = value
                else:
                    print("Unrecongized option %s" % key)
            except:
                pass

        folder = options['folder']
        filename = options['filename']
        code = cell

        if options['replace'] != 'false':

            if not os.path.exists(folder):
                os.makedirs(folder)

            os.system("rm -f %s.tex %s.pdf %s.png" % (folder+filename, folder+filename, folder+filename))        

            with open(folder+filename + ".tex", "w") as file:
                file.write(latex_template % (options['options'], cell))
    
            os.system("pdflatex -interaction batchmode -output-directory=%s %s.tex" % (folder,filename))
            os.system("rm -f %s.aux %s.log" % (folder+filename, folder+filename))        
            os.system("pdfcrop %s.pdf %s-tmp.pdf" % (folder+filename, folder+filename))
            os.system("mv %s-tmp.pdf %s.pdf" % (folder+filename, folder+filename))        

            if options['format'] == 'png':
                os.system("convert -density %s %s.pdf %s.png" % (options['dpi'], folder+filename, folder+filename))
                result = Image(filename=folder+filename + ".png")
            else:
                os.system("pdf2svg %s.pdf %s.svg" % (folder+filename, folder+filename))
                result = SVG(folder+filename + ".svg")

            return result
        else:

            if options['format'] == 'png':
                #os.system("convert -density %s %s.pdf %s.png" % (options['dpi'], filename, filename))
                result = Image(filename=folder+filename + ".png")
            else:
               # os.system("pdf2svg %s.pdf %s.svg" % (filename, filename))
                result = SVG(folder+filename + ".svg")

            return result


def load_ipython_extension(ipython):
    ipython.register_magics(Circuitikz)
