class Notify(object):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 notify_type,
                 active=True):
        """
        Sets up the default notification type.

        :param notify_type: From a list (currently: [stdout])
        :param active: Whether to actually perform the notification or not. Defaults to True.
        """

        self.notify_type = notify_type
        self.active = active

        self.notify_types = ["stdout"]

        assert notify_type in self.notify_types

    # ------------------------------------------------------------------------------------------------------------------
    def notify(self,
               msg):
        """
        Entry point for the notification.

        :param msg: The message we want to send to the user.

        :return: Nothing.
        """

        if self.notify_type == "stdout":
            self.notify_stdout(msg)

    # ------------------------------------------------------------------------------------------------------------------
    def notify_stdout(self,
                      msg):
        """
        Uses the print function to print the message to the stdout.

        :param msg:
        :return:
        """

        if self.active:
            print(msg)
