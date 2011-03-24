/* This version:
 * Copyright Xueqiao Xu ( http://code.google.com/p/mycodeplayground )
 * MIT License ( http://www.opensource.org/licenses/mit-license.php )
 * Download from: http://code.google.com/p/mycodeplayground

 * Python version:
 * Copyright Xueqiao Xu ( http://code.google.com/p/mycodeplayground )
 * MIT License ( http://www.opensource.org/licenses/mit-license.php )
 * Download from: http://code.google.com/p/mycodeplayground

 * Javascript version:
 * Copyright Stephen Sinclair (radarsat1) ( http://www.music.mcgill.ca/~sinclair )
 * MIT License ( http://www.opensource.org/licenses/mit-license.php )
 * Download from: http://www.music.mcgill.ca/~sinclair/blog

 * Flash version:
 * Copyright iunpin ( http://wonderfl.net/user/iunpin )
 * MIT License ( http://www.opensource.org/licenses/mit-license.php )
 * Download from: http://wonderfl.net/c/6eu4

 * Original Java version:
 * http://grantkot.com/MPM/Liquid.html
 */

/* Note:
 * make sure that the following line is present in the file "fluid.pro":
 *    QT += opengl
 */


#include <QApplication>

#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow window(600, 600);
    window.show();
    return app.exec();
} 
