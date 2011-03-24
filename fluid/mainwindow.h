#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QtOpenGL>

#include "fluidmodel.h"


class QTimer;
class QLine;

class MainWindow : public QGLWidget {
    
    Q_OBJECT

    public:

        MainWindow(int w, int h);
        ~MainWindow();

    protected:

        void initializeGL();
        void resizeGL(int w, int h);
        void paintGL();

        void mousePressEvent(QMouseEvent *event);
        void mouseReleaseEvent(QMouseEvent *event);
        void mouseMoveEvent(QMouseEvent *event);
       
    private:
        
        FluidModel     *fluid;

        QTimer         *timer;
};

#endif
