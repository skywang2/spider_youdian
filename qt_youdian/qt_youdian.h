#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_qt_youdian.h"

class qt_youdian : public QMainWindow
{
	Q_OBJECT

public:
	qt_youdian(QWidget *parent = Q_NULLPTR);

private:
	Ui::qt_youdianClass ui;
};
