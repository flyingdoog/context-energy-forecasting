"""Compile the supplied manuscript only. No assets or experiments are recomputed."""
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    latex=shutil.which('pdflatex')
    bibtex=shutil.which('bibtex')
    if not latex or not bibtex:
        raise SystemExit('Use a LaTeX installation with pdflatex, bibtex, IEEEtran and balance.')
    build=ROOT/'tmp/pdfs'
    build.mkdir(parents=True,exist_ok=True)
    command=[latex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
             '-output-directory='+str(build),'main.tex']
    for step in range(3):
        result=subprocess.run(command,cwd=ROOT/'paper',capture_output=True,text=True,
                              errors='replace',timeout=120)
        (build/f'latex_{step}.log').write_text(result.stdout+result.stderr,encoding='utf8')
        if result.returncode:
            raise SystemExit('LaTeX failed; inspect '+str(build/f'latex_{step}.log'))
        if step==0:
            shutil.copy2(ROOT/'paper/references.bib',build/'references.bib')
            result=subprocess.run([bibtex,'main'],cwd=build,capture_output=True,text=True,
                                  errors='replace',timeout=60)
            (build/'bibtex.log').write_text(result.stdout+result.stderr,encoding='utf8')
            if result.returncode:
                raise SystemExit('BibTeX failed; inspect '+str(build/'bibtex.log'))
    shutil.copy2(build/'main.pdf',ROOT/'paper/context_energy_forecasting.pdf')
    shutil.copy2(build/'main.bbl',ROOT/'paper/main.bbl')
    print('Compiled paper/context_energy_forecasting.pdf. Check page count and layout after edits.')

if __name__=='__main__':main()
