# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import time
import glob
import sys

import rospy
import rospkg

from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtGui import QFileDialog, QGraphicsView, QIcon, QWidget, QPixmap, QApplication

import rosbag
# import bag_helper
# from .bag_timeline import BagTimeline


class BagGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(BagGraphicsView, self).__init__()


class CaptchaWidget(QWidget):
    """
    Widget for use with Bag class to display and replay bag files
    Handles all widget callbacks and contains the instance of BagTimeline for storing visualizing bag data
    """
    def __init__(self, context):
        """
        :param context: plugin context hook to enable adding widgets as a ROS_GUI pane, ''PluginContext''
        """
        super(CaptchaWidget, self).__init__()
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('rqt_captcha_task'), 'resources', 'captcha_widget.ui')
        loadUi(ui_file, self, {'BagGraphicsView': BagGraphicsView})
        self.keyPressEvent = self._on_key_press

        self.setObjectName('CaptchaWidget')

        self.push_button.clicked[bool].connect(self._handle_button_clicked)
        # self.next_button.setEnabled(True)
        # self.next_button.setText("Submit")
        self._practice = True
        self.push_button.setVisible(False)
        self.image_count = -1
        self.label.setText("Type the participant ID in the box below.")
        
        path = rp.get_path('rqt_captcha_task') + "/resources/captcha_easy"
        self.image_list = glob.glob( path + '/*.gif')
        self.output_path = rp.get_path('rqt_captcha_task') + "/output/"

    def _on_key_press(self, event):
        # print(qKeyEvent.key())
        if event.key() == Qt.Key_Return: 
            self._handle_next_clicked()
        # else:
        #     super().keyPressEvent(event)

    def _handle_button_clicked(self):
        self._practice = False
        self.push_button.setVisible(False)

    def _handle_next_clicked(self):

        self.image_count += 1
        if self.image_count == 0:
            self.participant_id = self.text_input.text()
            self.output_file = self.output_path + self.participant_id + ".txt"
            with open (self.output_file, 'a') as f:
                f.write ("Time" + ',' + "User Input" +
                    ',' +  "Captcha Text" +'\n')
            self.label.setText("Type the characters you see in the box below:")
            self.push_button.setVisible(True)
        
        
        if not (self.image_count == 0) and not self._practice:
            self._record()
        self.text_input.clear()
        self._set_image()

    def _set_image(self):
        self.image_file = self.image_list[self.image_count]
        self.image.setPixmap(QPixmap(self.image_file))

    def _record(self):
        with open (self.output_file, 'a') as f: 
            f.write (str(rospy.Time.now()) + ',' + self.text_input.text() + 
                ',' +  (self.image_file.split("/")[-1]).split(".")[0] +'\n')
        

if __name__ == "__main__":
    rospy.init_node('captcha_task')
    app = QApplication(sys.argv)
    widget = CaptchaWidget(None)
    widget.show()
    sys.exit(app.exec_())
