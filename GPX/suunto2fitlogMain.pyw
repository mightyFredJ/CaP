# python
import sys
import os

# other
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# mine
from gui import Ui_MainWindow
from work_funcs import identify_files, gather_activities, save_as_fitlog

# -------------------------------------------------------------------

app = QtGui.QApplication(sys.argv)

# -------------------------------------------------------------------

class suunto2fitlogApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
    # init des composants créés avec le designer
        super(suunto2fitlogApp, self).__init__(parent)
        self.createWidgets()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # sinon ça crashe à la fermeture

    # other
        self.ui.btnCheck.clicked.connect(self.checkList)
        self.ui.btnGo.clicked.connect(self.go)
        self.ui.btnEnregistrer.clicked.connect(self.enreg)
        
    # qqs manips perso
        self.settings = QtCore.QSettings("simple.ini", QtCore.QSettings.IniFormat)
        self.loadConfig()

    def createWidgets(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

# ----------------
    
    def closeEvent(self, event):
        self.saveConfig()
        QtGui.QWidget.closeEvent(self, event)

    def saveConfig(self):
        """ renvoie False en cas d'échec """
        success = False
        try:
            self.settings.beginGroup('geom')
            self.settings.setValue('size', self.size())
            self.settings.setValue('pos', self.pos())
            self.settings.endGroup()
            self.settings.beginGroup('ui')
            self.settings.setValue('smlsdir', self.ui.txtInputDir.text())
            self.settings.setValue('from', self.ui.dateFrom.date().toString('yyyy-MM-dd'))
            self.settings.setValue('to', self.ui.dateTo.date().toString('yyyy-MM-dd'))
            self.settings.setValue('gpxdir', self.ui.txtOutputDir.text())   
            success = True
        except BaseException as ex:
            self.ui.statusbar.message('echec lors de l\'enregistrement de la config : %s' % (str(ex)))
        finally:
            self.settings.endGroup()
        
        return success
        
    def loadConfig(self):
        """ renvoie False en cas d'échec """
        success = False
        try:
            self.settings.beginGroup('geom')
            self.resize(self.settings.value('size', QtCore.QSize(900, 600)))
            self.move(self.settings.value('pos', QtCore.QPoint(10, 10)))
            self.settings.endGroup()
            self.settings.beginGroup('ui')
            self.ui.txtInputDir.setText(self.settings.value('smlsdir', ''))
            self.ui.txtOutputDir.setText(self.settings.value('gpxdir', ''))
            self.ui.dateFrom.setDate(QtCore.QDate.fromString(self.settings.value('from', '2016-09-01'), 'yyyy-MM-dd'))
            self.ui.dateTo.setDate(QtCore.QDate.fromString(self.settings.value('to', '2019-12-31'), 'yyyy-MM-dd'))
            success = True
        except BaseException as ex:
            self.ui.statusbar.message('echec lors du chargement de la précédente config %s' % (str(ex)))
        finally:
            self.settings.endGroup()

        return success

# ----------------
# tringlerie pour mutualiser les traitements communs

    def waiting_effects(func):
        """
            decorator pour changer temporairement l'aspect du curseur
                pendant une opération potentiellement lngueo
            
            >>> @waiting_effects
            ... def doLengthyProcess():
            ...     # do lengthy process
            ...     pass
            
            copié from http://stackoverflow.com/questions/8218900/how-can-i-change-the-cursor-shape-with-pyqt
            adapté avec http://sametmax.com/comprendre-les-decorateur-python-pas-a-pas-partie-2/
                (passque ça marchait pas sans ça, pb d'arguments)
        """
        def wrapper(*args, **kwargs):
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                QtGui.QApplication.restoreOverrideCursor()
        return wrapper

    def redirect_output_to(txtedit):
        """
            décorateur permettant de capturer la sortie standard des fonctions appelées
                et de les rediriger vers la zone de texte
            
            c'est le "1er" niveau de décorateur qui permet de gérer des arguments
            >>> @redirect_output_to(param)
            >>> func():
            ...
            est équivalent à 
            >>> func = redirect_output_to(param)(func)
                
            cf. https://openclassrooms.com/courses/apprenez-a-programmer-en-python/les-decorateurs
        """
        def redirect_decorator(func):
            """
                "2ème" niveau de décorateur qui permet d'encapsuler la fonction :
                >>> @redirect_decorator
                >>> func():
                ...
                est équivalent à 
                >>> func = redirect_decorator(func)
            """
            # warn: textedit est défini à l'iniitialisation lors la création de la fonction décorée,
            #   mais comme personne ne pointe dessus ensuite, son compteur de références tombe à séro
            #   et donc il est supprimé et sera inaccessible au runtime lors de l'appel de modified_func
            # j'en fait donc une copie pour l'usage lors du runtime
            target = txtedit
            def modified_func(self, *args, **kwargs):
                """ comme func est une méthode de classe, modified_func le devient aussi
                        (modified_func est appelée pdt le runtime par self qui est
                         l'instance de la classe)
                         
                    cf. http://stackoverflow.com/questions/7590682/access-self-from-decorator
                     
                    rem. : l'important c'est de bien respecter les signatures de modified_func et de func
                           au fond osef qu'il y ait un self ou non, on pourrait s'en passer et travailler
                           avec args[0] car on sait qu'il est là, mais je préfère cette notation
                """
                try:
                    class OutLog:
                        def __init__(self, edit):
                            self.edit = edit
                        def write(self, m):
                            self.edit.moveCursor(QtGui.QTextCursor.End)
                            self.edit.insertPlainText( m )
                    txteditor = getattr(self.ui, target)
                    sys.stdout = OutLog(txteditor)
                    txteditor.setText('')

                    return func(self, *args, **kwargs)
                except BaseException as ex:
                    raise ex
                finally:
                    sys.stdout = sys.__stdout__
            return modified_func
        return redirect_decorator

# ----------------            
            
    @waiting_effects
    @redirect_output_to("txtOutputPy")
    def checkList(self, checked = False):
        try:
            initdir = os.getcwd()
            workdir = self.ui.txtInputDir.text()
            os.chdir(workdir)

            after = self.ui.dateFrom.date().toString('yyyy-MM-dd')
            before = self.ui.dateTo.date().toString('yyyy-MM-dd')
            self.found_files = identify_files(['*.sml'], after, before, quiet=True)

        except BaseException as ex:
            self.ui.statusbar.message('echec lors de l\'appel du programme: %s' % (str(ex)))
        finally:
            os.chdir(initdir)

        
    @redirect_output_to("txtOutputPy")
    @waiting_effects
    def go(self, checked = False):
        if not 'found_files' in dir(self) or len(self.found_files) == 0:
            self.ui.statusbar.message('aucun fichier identifié')
            return
        
        try:
            initdir = os.getcwd()
            self.ui.prgbarAvancement.setValue(0)
            step = 100. / len(self.found_files)
            
            workdir = self.ui.txtInputDir.text()
            os.chdir(workdir)

            def majWindow():
                self.ui.prgbarAvancement.setValue(self.ui.prgbarAvancement.value() + step)
                app.processEvents()
                
            self.def_activities = gather_activities(self.found_files, head=True, quiet=True, ui=majWindow)

        except BaseException as ex:
            self.ui.statusbar.message('echec lors de l\'appel du programme: %s' % (str(ex)))
        finally:
            os.chdir(initdir)


    @redirect_output_to("txtOutputPy")
    @waiting_effects
    def enreg(self, checked = False):
        if not 'def_activities' in dir(self) or len(self.def_activities) == 0:
            self.ui.statusbar.message('aucune activité chargée')
            return

        fitlogfile = self.ui.txtOutputFile.text()
        if fitlogfile == "":
            fitlogfile = "temp.fitlog"
        fitlogfile = os.path.join(self.ui.txtOutputDir.text(), fitlogfile)
        ext = '.fitlog'
        if not fitlogfile.endswith(ext):
            fitlogfile += ext
        save_as_fitlog(self.def_activities, fitlogfile)
        
# -------------------------------------------------------------------

# if __name__ == "__main__":
mywindow = suunto2fitlogApp()
mywindow.show()
sys.exit(app.exec_())
