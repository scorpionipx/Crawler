import logging

from crawler.utils.connection.client import Client
from crawler.utils.commands import Command, Commands, COMMAND_HEADER, HEADER_LITERAL, ID_LITERAL, VALUE_LITERAL

logger = logging.getLogger("ipx_logger")


class CrawlerController:
    """CrawlerController
        Class used to handle Crawler's controller.
    """
    def __init__(self, ip, port):
        """Constructor
        """
        self.connection = Client(host=ip, port=port)
        self.commands = Commands()

    def connect_to_crawler(self):
        """connect_to_crawler
            Create connection between Crawler and controller
        :return: None
        """
        self.connection.connect_to_host()

    def __create_package__(self, _header, _id, _value):
        """__create_package__
            Create package to be sent to Crawler
        :return:
        """
        _package = HEADER_LITERAL + str(_header) + ID_LITERAL + str(_id) + VALUE_LITERAL + str(_value)
        return _package

    def send_command(self, command, value=None):
        """send_command
            Send a command to Crawler.
        :param command: Command type object.
        :param value: Value to be applied on command (optional).
        :return: None
        """
        if isinstance(command, Command):
            pass
        else:
            logging.warning('Invalid command argument in CrawlerController.send_command(command). Command object '
                            'expected!')
            return

        if command.value_required and value is None:
            logging.warning('Warning! Command {} needs a value specified to be sent! No value provided!'
                            .format(command.name))
            return

        package = self.__create_package__(COMMAND_HEADER, command.id, value)
        self.connection.send_package(package)

        logger.debug("Command package [{}] sent!".format(package))

    def drive_forward(self, speed):
        """drive_forward
            Tell Crawler to drive forward according to the specified speed.
        :param speed: Speed of the crawler as percentage (PWM duty cycle) - integer ranged [0, 100]
        :return: None
        """
        if speed > 100 or speed < 0:
            logging.warning("Invalid speed value specified in drive_forward! Integer in range [0, 100] expected!")
            return

        speed *= 4.8  # max speed is 480 according to library for the Pololu Dual MC33926 Motor Driver for Raspberry Pi
        speed = int(speed)

        self.send_command(self.commands.drive, speed)

    def drive_backward(self, speed):
        """drive_backward
            Tell Crawler to drive backward according to the specified speed.
        :param speed: Speed of the crawler as percentage (PWM duty cycle) - integer ranged [0, 100]
        :return: None
        """
        if speed > 100 or speed < 0:
            logging.warning("Invalid speed value specified in drive_backward! Integer in range [0, 100] expected!")
            return

        speed *= -4.8  # max speed is 480 according to library for the Pololu Dual MC33926 Motor Driver for Raspberry Pi
        speed = int(speed)

        self.send_command(self.commands.drive, speed)

    def drive(self, speed):
        """drive
            Tell Crawler to drive according to the specified speed. Positive speed - forward, negative speed - backward.
        :param speed: Speed of the crawler as percentage (PWM duty cycle) - integer ranged [-100, 100].
        :return: None
        """
        if speed > 100 or speed < -100:
            logging.warning("Invalid speed value specified in drive! Integer in range [-100, 100] expected!")
            return

        speed *= 4.8  # max speed is 480 according to library for the Pololu Dual MC33926 Motor Driver for Raspberry Pi
        speed = int(speed)

        self.send_command(self.commands.drive, speed)

    def steer(self, steering):
        """steer
            Tell Crawler to steer according to the specified steering power. Positive - steer right and vice-versa.
        :param steering: Steering power - integer ranged [-100, 100].
        :return: None
        """
        if steering > 100 or steering < -100:
            logging.warning("Invalid steering value specified in steer! Integer in range [-100, 100] expected!")
            return

        steering *= 4.8  # max steer is 480 according to library for the Pololu Dual MC33926 Motor Driver for RPi
        steering = int(steering)

        self.send_command(self.commands.steer, steering)

    def speak(self, speech):
        """speak
            Tell Crawler to speak.
        :param speech: text to be spoken.
        :return: None
        """
        self.send_command(self.commands.speak, speech)

    def enable_motor_control(self):
        """enable_motor_control
            Tell Crawler to enable motor control.
        :return: None
        """
        self.send_command(self.commands.enable_motor_control)

    def disable_motor_control(self):
        """disable_motor_control
            Tell Crawler to disable motor control.
        :return: None
        """
        self.send_command(self.commands.disable_motor_control)





