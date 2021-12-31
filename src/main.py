import os

from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtPrintSupport import QPrintPreviewDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget,
)

from __init__ import __version__
from about import AboutDialog

version = str(__version__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabs.setIconSize(QSize(16, 16))
        self.tabs.setTabsClosable(True)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        navtb.setMovable(False)
        self.addToolBar(navtb)

        back_btn = QAction(
            QIcon(os.path.join("assets", "icons", "arrow-180.png")),
            "Back",
            self,
        )
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(
            QIcon(os.path.join("assets", "icons", "arrow.png")),
            "Forward",
            self,
        )
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(
            QIcon(os.path.join("assets", "icons", "arrow-circle-315.png")),
            "Reload",
            self,
        )
        reload_btn.setStatusTip("Reload Page")
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload()
        )
        navtb.addAction(reload_btn)

        home_btn = QAction(
            QIcon(os.path.join("assets", "icons", "home.png")), "Home", self
        )
        home_btn.setStatusTip("Go Home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(
            QPixmap(os.path.join("assets", "icons", "lock.png"))
        )
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(
            QIcon(os.path.join("assets", "icons", "cross-circle.png")),
            "Stop",
            self,
        )
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(
            QIcon(os.path.join("assets", "icons", "ui-tab--plus.png")),
            "New Tab",
            self,
        )
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(
            QIcon(os.path.join("assets", "icons", "disk--arrow.png")),
            "Open File...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(os.path.join("assets", "icons", "disk--pencil.png")),
            "Save Page As...",
            self,
        )
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(
            QIcon(os.path.join("assets", "icons", "printer.png")),
            "Print...",
            self,
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(os.path.join("assets", "icons", "question.png")),
            "About Chaser",
            self,
        )
        about_action.setStatusTip("Find out more about Chaser")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_chaser_action = QAction(
            QIcon(os.path.join("assets", "icons", "lifebuoy.png")),
            "Chaser Homepage",
            self,
        )
        navigate_chaser_action.setStatusTip("Go to the Chaser homepage")
        navigate_chaser_action.triggered.connect(self.navigate_chaser)
        help_menu.addAction(navigate_chaser_action)

        self.add_new_tab(QUrl("https://www.google.com"), "Homepage")

        self.show()

        self.setWindowTitle("Chaser")
        self.setWindowIcon(
            QIcon(os.path.join("assets", "icons", "cookie.png"))
        )
        self.setWindowIconText("Chaser")

    def add_new_tab(self, qurl: QUrl = None, label: str = "Blank") -> None:
        if qurl is None:
            qurl = QUrl("")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_urlbar(qurl, browser)
        )
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

    def tab_open_doubleclick(self, i: int) -> None:
        # No tab under the click
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self) -> None:
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i: int) -> None:
        if self.tabs.count() <= 1:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser: QWidget) -> None:
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Chaser")

    def navigate_chaser(self) -> None:
        self.tabs.currentWidget().load(QUrl("https://luciferchase.github.io"))

    def about(self) -> None:
        dlg = AboutDialog()
        dlg.exec()

    def open_file(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Hypertext Markup Language (*.htm *.html);;" "All Files (*)",
        )

        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *.html);;" "All Files (*)",
        )

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, "w") as f:
                f.write(html.encode("utf8"))

    def print_page(self) -> None:
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec()

    def navigate_home(self) -> None:
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self) -> None:
        qurl = QUrl(self.urlbar.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")

        self.tabs.currentWidget().setUrl(qurl)

    def update_urlbar(self, qurl: QUrl, browser: QWidget = None) -> None:
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

        # Secure padlock icon
        if qurl.scheme() == "https":
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("assets", "icons", "lock-ssl.png"))
            )
        # Insecure padlock icon
        else:
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("assets", "icons", "lock.png"))
            )

        self.urlbar.setText(qurl.toString())
        self.urlbar.setCursorPosition(0)


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Chaser")
    app.setApplicationVersion(version)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    app.exec()
