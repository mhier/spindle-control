import subprocess

class Spindle:
    def __init__(self, config):
        self.printer = config.get_printer()
        gcode = self.printer.lookup_object('gcode')
        self.gcode_move = self.printer.lookup_object('gcode_move')
        self.printer.register_event_handler("klippy:ready", self._handle_ready)

        gcode.register_command("M3", self.cmd_START)
        gcode.register_command("M03", self.cmd_START)
        gcode.register_command("M5", self.cmd_STOP)
        gcode.register_command("M05", self.cmd_STOP)

        self.handler_M220 = gcode.register_command("M220", None)
        gcode.register_command("M220", self.cmd_M220)

        self.handler_G0 = gcode.register_command("G0", None)
        gcode.register_command("G0", self.cmd_G0)
        gcode.register_command("G00", self.cmd_G0)

        self.handler_G1 = gcode.register_command("G1", None)
        gcode.register_command("G01", self.handler_G1)

        self.spindle_speed = 0

    def _handle_ready(self):
        self.tool = self.printer.lookup_object('toolhead')

    def cmd_START(self, gcmd):

        # wait until toolhead is in position
        self.tool.wait_moves()

        p = gcmd.get_command_parameters()
        self.spindle_speed = int(float(p['S']))

        cmd = "/home/mhier/spindle-control/start"
        output = subprocess.Popen(cmd, shell=True,                             \
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)                   \
            .communicate()[0]
        gcmd.respond_info(output)

        # self.speed_factor is 1/60 by default, so it converts to Hz
        cmd = "/home/mhier/spindle-control/set_frequency " +                   \
            str(self.spindle_speed * self.gcode_move.speed_factor)
        output = subprocess.Popen(cmd, shell=True,                             \
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)                   \
            .communicate()[0]
        gcmd.respond_info(output)


    def cmd_STOP(self, gcmd):

        # wait until toolhead is in position
        self.tool.wait_moves()

        cmd = "/home/mhier/spindle-control/stop"
        output = subprocess.Popen(cmd, shell=True,                             \
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)                   \
            .communicate()[0]
        gcmd.respond_info(output)


    def cmd_G0(self, gcmd):
        speed = self.gcode_move.speed
        self.gcode_move.speed = 1e9
        self.handler_G0(gcmd)
        self.gcode_move.speed = speed

    def cmd_G0(self, gcmd):
        speed = self.gcode_move.speed
        self.gcode_move.speed = 1e9
        self.handler_G0(gcmd)
        self.gcode_move.speed = speed


    def cmd_M220(self, gcmd):

        # wait until toolhead is in position
        self.tool.wait_moves()

        self.handler_M220(gcmd)
        gcmd.respond_info(                                                     \
            "New speed factor: %5.3f" % self.gcode_move.speed_factor)

        cmd = "/home/mhier/spindle-control/set_frequency " +                   \
            str(self.spindle_speed * self.gcode_move.speed_factor)
        output = subprocess.Popen(cmd, shell=True,                             \
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)                   \
            .communicate()[0]
        gcmd.respond_info(output)


def load_config(config):
    return Spindle(config)
