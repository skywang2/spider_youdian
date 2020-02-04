/********************************************************************************
** Form generated from reading UI file 'qt_youdian.ui'
**
** Created by: Qt User Interface Compiler version 5.12.6
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_QT_YOUDIAN_H
#define UI_QT_YOUDIAN_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_qt_youdianClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *qt_youdianClass)
    {
        if (qt_youdianClass->objectName().isEmpty())
            qt_youdianClass->setObjectName(QString::fromUtf8("qt_youdianClass"));
        qt_youdianClass->resize(600, 400);
        menuBar = new QMenuBar(qt_youdianClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        qt_youdianClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(qt_youdianClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        qt_youdianClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(qt_youdianClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        qt_youdianClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(qt_youdianClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        qt_youdianClass->setStatusBar(statusBar);

        retranslateUi(qt_youdianClass);

        QMetaObject::connectSlotsByName(qt_youdianClass);
    } // setupUi

    void retranslateUi(QMainWindow *qt_youdianClass)
    {
        qt_youdianClass->setWindowTitle(QApplication::translate("qt_youdianClass", "qt_youdian", nullptr));
    } // retranslateUi

};

namespace Ui {
    class qt_youdianClass: public Ui_qt_youdianClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_QT_YOUDIAN_H
