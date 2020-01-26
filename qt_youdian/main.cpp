#include "qt_youdian.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	qt_youdian w;
	w.show();
	return a.exec();
}
