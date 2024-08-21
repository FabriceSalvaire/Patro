####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2022 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path
import shutil

from invoke import task

from .clean import flycheck as _clean_flycheck
from .release import update_git_sha as _update_git_sha

####################################################################################################

PATRO_SOURCE_PATH = Path(__file__).resolve().parents[1]

SPHINX_PATH = PATRO_SOURCE_PATH.joinpath('doc', 'sphinx')
BUILD_PATH = SPHINX_PATH.joinpath('build')
RST_SOURCE_PATH = SPHINX_PATH.joinpath('source')
RST_API_PATH = RST_SOURCE_PATH.joinpath('api')
RST_EXAMPLES_PATH = RST_SOURCE_PATH.joinpath('examples')

####################################################################################################

@task
def clean_build(ctx):
    # ctx.run('rm -rf {}'.format(BUILD_PATH))
    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)

####################################################################################################

@task
def clean_api(ctx):
    # ctx.run('rm -rf {}'.format(RST_API_PATH))
    if RST_API_PATH.exists():
        shutil.rmtree(RST_API_PATH)

@task(_update_git_sha, _clean_flycheck, clean_api)
def make_api(ctx):
    print()
    print('Generate RST API files')
    ctx.run('pyterate-rst-api {0.Package}'.format(ctx))
    run_sphinx(ctx)
    print('')
    print('<<< Check API contains undocumented >>>')

####################################################################################################

@task
def run_sphinx(ctx):
    print()
    print('Run Sphinx')
    working_path = SPHINX_PATH
    # subprocess.run(('make-html'), cwd=working_path)
    # --clean
    with ctx.cd(str(working_path)):
        ctx.run('make-html')

####################################################################################################

@task
def xdg_open(ctx):
    ctx.run('xdg-open doc/sphinx/build/html/index.html')
