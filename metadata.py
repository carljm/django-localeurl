import subprocess
import os.path

try:
    # don't get confused if our sdist is unzipped in a subdir of some
    # other hg repo
    if os.path.isdir('.hg'):
        p = subprocess.Popen(['hg', 'parents', r'--template={rev}\n'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not p.returncode:
            fh = open('HGREV', 'w')
            fh.write((p.communicate()[0].splitlines()[0] or '').decode('utf-8'))
            fh.close()
except (OSError, IndexError):
    pass

try:
    hgrev = open('HGREV').read()
except IOError:
    hgrev = ''

name = 'localeurl'
authors = 'Joost Cassee, Artiom Diomin and Carl Meyer'
copyright_years = '2008-2010'
version = '2.0.2.post%s' % hgrev
release = version
