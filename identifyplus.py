# -*- coding: utf-8 -*-

#******************************************************************************
#
# IdentifyPlus
# ---------------------------------------------------------
# Extended identify tool. Supports displaying and modifying photos
#
# Copyright (C) 2012 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from __init__ import version

import identifyplustool

import resources_rc

class IdentifyPlus:
  def __init__(self, iface):
    self.iface = iface

    try:
      self.QgisVersion = unicode(QGis.QGIS_VERSION_INT)
    except:
      self.QgisVersion = unicode(QGis.qgisVersion)[ 0 ]

    # For i18n support
    userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/identifyplus"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/identifyplus"

    overrideLocale = QSettings().value("locale/overrideFlag", QVariant(False)).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value("locale/userLocale", QVariant("")).toString()

    if QFileInfo(userPluginPath).exists():
      translationPath = userPluginPath + "/i18n/identifyplus_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/identifyplus_" + localeFullName + ".qm"

    self.localePath = translationPath
    if QFileInfo(self.localePath).exists():
      self.translator = QTranslator()
      self.translator.load(self.localePath)
      QCoreApplication.installTranslator(self.translator)

  def initGui(self):
    if int(self.QgisVersion) < 10900:
      qgisVersion = str(self.QgisVersion[ 0 ]) + "." + str(self.QgisVersion[ 2 ]) + "." + str(self.QgisVersion[ 3 ])
      QMessageBox.warning(self.iface.mainWindow(),
                           QCoreApplication.translate("IdentifyPlus", "Error"),
                           QCoreApplication.translate("IdentifyPlus", "Quantum GIS %1 detected.\n").arg(qgisVersion) +
                           QCoreApplication.translate("IdentifyPlus", "This version of IdentifyPlus requires at least QGIS version 1.9.0\nPlugin will not be enabled."))
      return None

    self.actionRun = QAction(QCoreApplication.translate("IdentifyPlus", "IdentifyPlus"), self.iface.mainWindow())
    self.actionRun.setIcon(QIcon(":/icons/identifyplus.png"))
    self.actionRun.setWhatsThis("Extended identify tool")
    self.actionRun.setCheckable(True)

    self.actionAbout = QAction(QCoreApplication.translate("IdentifyPlus", "About IdentifyPlus..."), self.iface.mainWindow())
    self.actionAbout.setIcon(QIcon(":/icons/about.png"))
    self.actionAbout.setWhatsThis("About IdentifyPlus")

    self.iface.addPluginToVectorMenu(QCoreApplication.translate("IdentifyPlus", "IdentifyPlus"), self.actionRun)
    self.iface.addPluginToVectorMenu(QCoreApplication.translate("IdentifyPlus", "IdentifyPlus"), self.actionAbout)
    self.iface.addVectorToolBarIcon(self.actionRun)

    self.actionRun.triggered.connect(self.run)
    self.actionAbout.triggered.connect(self.about)

    # prepare map tool
    self.mapTool = identifyplustool.IdentifyPlusTool(self.iface.mapCanvas())
    self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

  def unload(self):
    self.iface.removeVectorToolBarIcon(self.actionRun)
    self.iface.removePluginVectorMenu(QCoreApplication.translate("IdentifyPlus", "IdentifyPlus"), self.actionRun)
    self.iface.removePluginVectorMenu(QCoreApplication.translate("IdentifyPlus", "IdentifyPlus"), self.actionAbout)

    del self.mapTool

  def mapToolChanged(self, tool):
    if tool != self.mapTool:
      self.actionRun.setChecked(False)

  def run(self):
    self.iface.mapCanvas().setMapTool(self.mapTool)
    self.actionRun.setChecked(True)

  def about(self):
    pass