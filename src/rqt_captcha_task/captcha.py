import argparse

from qt_gui.plugin import Plugin

from .captcha_widget import CaptchaWidget


class Captcha(Plugin):
    """
    Subclass of Plugin to provide interactive bag visualization, playing(publishing) and recording
    """
    def __init__(self, context):
        """
        :param context: plugin context hook to enable adding widgets as a ROS_GUI pane, ''PluginContext''
        """
        super(Captcha, self).__init__(context)
        self.setObjectName('Captcha')
        self._widget = CaptchaWidget(context)
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)
