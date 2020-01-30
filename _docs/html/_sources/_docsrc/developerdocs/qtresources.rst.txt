Qt Resources
============

Qt Creator / Designer was used to both create GUI templates and a Qt resource file for icons.

UI Files
--------

The \*.ui files are located in *resources/ui* and need to be converted to Python files first with *pyuic5*.
The Python files are located in *ui/templates*. The conversion of the UI files is performed
automatically each time when running ESCMillPCB from the sources via a python shell and therefore
is not needed to be performed manually. This conversion is done by the function
:func:`Base.UITools.convertUI` which is called in the import section of ESCMillPCB.py.

This approach has the advantage over uic.loadUi that the \*.ui files do not have to be included
as additional resources to the executable directory and therefore cannot be altered by the
end user.

Resource File
-------------

Icons used in the application are included into the executable file by using Qt's resource system.
The resource file is located in *resources* and the icons are stored in *resources/images*.
The resource file can be edited with a text editor or with Qt Creator / Designer. If the file
(or one of the image files) has been edited, it is necessary to convert the resource file
into a python file via *pyrcc5*. Similar to the \*.ui files, this is done automatically when running
ESCMillPCB from the sources via a python shell and therefore is not needed to be performed manually.