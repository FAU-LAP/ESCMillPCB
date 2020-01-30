"""
Created on 17.06.2019

@author: Christian Ott

Adapted from Martin Hauck
"""

import logging
logger = logging.getLogger(__name__)

import glob
import os
import sys
#import re

def convertUI():
    """
    Converts Qt *.ui files to python files.
    """
    for ui_path in glob.iglob(r'resources\ui\*.ui'):
        base_path=r'ui\templates'
        class_name = ui_path.split('\\')[-1][:-3]
        ui_class_name = "Ui_" + class_name
        ui_class_path = os.path.join(base_path, ui_class_name + '.py')
        logger.info('Converting "{}" to "{}"'.format(ui_path, ui_class_path))
        os.system('{} -m PyQt5.uic.pyuic {} -o {}'.format(sys.executable, ui_path, ui_class_path))
        #         if not os.path.exists(os.path.join(base_path, class_name + '.py')):
        #             with open(ui_path, 'r') as ui_file:
        #                 print(class_name)
        #                 superclass_name = re.findall(
        #                     '<widget class="(.*)" name="{}"'.format(class_name),
        #                     ui_file.read())[0]
        #             logger.info('Creating "{}"'.format(class_name + '.py'))
        #             with open(class_name + '.py', 'w+') as class_file:
        #                 class_file.writelines(
        #                     # noinspection PyStatementEffect
        #                     ['from PyQt5.QtCore import pyqtSlot\n',
        #                      'from PyQt5.QtWidgets import {}\n'.format(superclass_name),
        #                      'from GUI.Ui_{} import Ui_{}\n'.format(class_name, class_name),
        #                      '\n', '\n',
        #                      'class {}({}, {}):\n'.format(class_name, superclass_name, ui_class_name),
        #                      '\n',
        #                      '    def __init__(self, parent=None):\n',
        #                      '\n',
        #                      '        super({}, self).__init__(parent)\n'.format(class_name),
        #                      '        self.setupUi(self)\n'])
        

def convertResources():
    """
    Converts Qt *.qrc files to python files.
    """
    for qrc_path in glob.iglob(r'resources\*.qrc'):
        base_path=r'ui'
        module_name, _ = os.path.splitext(os.path.basename(qrc_path))
        module_path = os.path.join(base_path, module_name + '.py')
        logger.info('Converting "{}" to "{}"'.format(qrc_path, module_path))
        os.system('{} -m PyQt5.pyrcc_main {} -o {}'.format(sys.executable, qrc_path, module_path))