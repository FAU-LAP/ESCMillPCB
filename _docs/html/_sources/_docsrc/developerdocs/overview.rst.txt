Overview
========

This part of the documentation is meant to aid future developers to orient themselves in the
program's structure and is an addition to the API documentation which is generated from the
docstrings. It is by no means a complete developer documentation and the reader is strongly
encouraged to add missing information.

Source directory
----------------

The following table lists and describes files and folders in the project base directory.

===============  =========================================================================
File/directory   Description
===============  =========================================================================
_build           Working directory for PyInstaller
_dist            Contains the freezed version of the program
_docs            Contains this documentation
_docsrc          Contains the source files used to create this documentation
_platforms       Contains additional Qt DLLs necessary to run the freezed version.
                 The contents are copied to _dist/platforms during the build process.
_static          ??
_templates       ??
_test            Files used for testing the program
Algorithm        Algorithm package sources
Base             Base package sources
EagleImport      EagleImport package sources
Machines         Machines package sources
pyqtgraph        Modified version of the pyqtgraph library
resources        Additional resources which are included in the freezed exe file
                 (images/icons, Qt ui files, Qt resource files)
ui               ui package sources
build.bat        Batch file to run the whole build process
conf.py          Configuration file for the Sphinx documentation builder
docindex.rst     Base source file of this documentation
ESCMillPCB.py    Entry file of the program's Python source
ESCMillPCB.spec  Configuration file for PyInstaller
makedocs.bat     Batch file for building this documentation
test.py          Some tests used during development
===============  =========================================================================

pyqtgraph
---------

The Python library `pyqtgraph <http://www.pyqtgraph.org>`_ by Luke Campagnola is used extensively
for the GUI and the settings system (see :class:`Base.AppSettings.AppSettings`). Due to some
bugs in the used version pyqtgraph, a modified version of pyqtgraph is included in the source
folder *pyqtgraph*. Note that using an unmodified version of pyqtgraph might not work.
