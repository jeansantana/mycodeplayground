#include <QtGui>
#include <QtOpenGL>

#include "mainwindow.h"
#include "fluidmodel.h"

MainWindow::MainWindow(int w, int h) {

    resize(w, h);

    fluid = new FluidModel(w / 4, h / 4, 100, 100);
    
    timer = new QTimer;
    timer->setSingleShot(false);

    connect(timer, SIGNAL(timeout()), this, SLOT(updateGL()));
    timer->start(20);
}


MainWindow::~MainWindow() {
    delete fluid;
    delete timer;
}


void MainWindow::initializeGL() {
    glClearColor(1.0, 1.0, 1.0, 1.0);
}


void MainWindow::resizeGL(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, w, 0, h);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}


void MainWindow::paintGL() {
    fluid->step();
    const Line *lines = fluid->getLines();
    
    glClear(GL_COLOR_BUFFER_BIT);
    
    glColor3f(0.3, 0.3, 1.0);
    for (unsigned i = 0; i < 100 * 100; ++i) {
        glBegin(GL_LINES);
        glVertex2d(lines[i].x1 * 4, height() - lines[i].y1 * 4);
        glVertex2d(lines[i].x2 * 4, height() - lines[i].y2 * 4);
        glEnd();
    }
}


void MainWindow::mousePressEvent(QMouseEvent *event) {
    fluid->setMovePos(event->x(), event->y());
    fluid->setPressed(true);
}


void MainWindow::mouseReleaseEvent(QMouseEvent *event) {
    fluid->setPressed(false);
}

void MainWindow::mouseMoveEvent(QMouseEvent *event) {
    fluid->setMovePos(event->x(), event->y());
}
