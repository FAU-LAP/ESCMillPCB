Building ESCMillPCB
===================

Building the programm into an executable file is easily possible by running *build.bat* in the source base
directory. This invokes the complete toolchain including building the documentation and copying ressource
files to the build destination directory *_dist*.

.. note::

   `PyInstaller <https://www.pyinstaller.org/>`_ is used for the build, so make sure PyInstaller is installed in your python distribution.
   Also it may be necessary to run *build.bat* from the Anaconda promt, if you are using the Anaconda distribution.
   
.. warning::
	
   The current version of PyInstaller (v3.5) has a bug associated with German localization. On a German Windows, it may be
   necessary to add a work around to *<pythondir>/Lib/site-packages/PyInstaller/compat.py*:
   Locate the function *exec_command* and change *out = out.decode(encoding)* to out = *out.decode(encoding, errors='replace')*.

.. note::
   The documentation is created with `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_, 
   so make shure Sphinx is installed in your python distribution.
   
.. note::

   Please increase the build number in the version string of the :py:class:`Base.AppBase` class. If the program
   was significantly changed (e.g. features added), also increase the version itself.

   
Build internals
---------------

`PyInstaller <https://www.pyinstaller.org/>`_ is used to pack the programm into a single executable file. 
The build spec file *ESCMillPCB.spec* with the build settings is located in the source base directory.

PyQt's system for promoting widgets to custom widgets in QtDesigner leads to hidden imports not
visible to PyInstaller. Therefore it is necessary to inform PyInstaller about these modules in the spec file.
When extending the software with new widgets which are not directly included in the code, remember to
extend the *hiddenimports* list accordingly.

Unfortunatelly, the single executable file does not work completely out of the box. 
A few resource files need to be included in the *_dist* directory next to the executable:

* The files in the *_platforms* directory, which need to be placed in *_dist/platforms* and contains necessary Qt DLLs.
* The *_docs* directory which contains this documentation.

This is automatically done when using *build.bat*.


Building the documentation
--------------------------

This documentation is created using `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_. The documentation
source files are located in the *_docsrc* folder. It can be build using *makedocs.bat html* (it may be necessary
to run this from the Anaconda prompt). Note that the output directory is *_docs*, the *_dist/_docs* directory
is not updated.

API documentation is created automatically by extracting docstrings from the source codes. This sis done using the
`Autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ plugin and it's *automodule*
directive. Adding new modules to the project will require to add them also the corresponding module index file
of the documentation sources. This can be automated using `apidoc <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html>`_.

.. todo::

   Maybe add apidoc to the build toolchain.