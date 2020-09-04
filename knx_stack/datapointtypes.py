from ctypes import c_uint8, c_uint32, c_uint16, c_float, LittleEndianStructure, Union
from enum import IntEnum, Enum
import inspect
import math
import decimal


class DPT_Factory(object):

    @staticmethod
    def make(dpt: str, fields_values: dict) -> 'knx_stack.datapointtypes.DPT':
        """
        Build a knx_stack.datapointtypes.DPT from a dpt name and a dictionary of values.

        :param dpt: a DPT name
        :param fields_values: a dictionary of values for the DPT's fields
        :return: a knx_stack.datapointtypes.DPT instance

        >>> import knx_stack
        >>> factory = knx_stack.datapointtypes.DPT_Factory()

        >>> dpt = factory.make("DPT_Control_Dimming", {"step": 7, "direction": "up"})
        >>> dpt.step
        7
        >>> dpt.direction == knx_stack.datapointtypes.DPT_Control_Dimming.Direction.up
        True

        >>> dpt = factory.make("DPT_Value_Temp", {"decoded_value": -1.0})
        >>> dpt.decode()
        -1.0
        """
        from knx_stack import datapointtypes
        dpt = getattr(datapointtypes, dpt)()
        for key, value in fields_values.items():
            if key == "decoded_value":
                dpt.encode(value)
            else:
                setattr(dpt, key, value)

        return dpt


class Description_Factory(object):

    @staticmethod
    def make(dpt):
        """
        Build a *Description* from a *knx_stack.datapointtypes.DPT*

        A *Description* is a tuple **(dpt name, dictionary with dpt fields values)**

        :param dpt: knx_stack.datapointtypes.DPT
        :return: a tuple *(dpt name, dictionary with dpt fields values)*


        >>> import knx_stack
        >>> factory = knx_stack.datapointtypes.Description_Factory()

        >>> switch = knx_stack.datapointtypes.DPT_Switch()
        >>> factory.make(switch)
        ('DPT_Switch', {'action': 'off'})

        >>> brightness = knx_stack.datapointtypes.DPT_Value_Lux()
        >>> brightness.encode(10000)
        >>> factory.make(brightness)
        ('DPT_Value_Lux', {'decoded_value': 9999.36})
        """
        description = {}
        fields = (set([name for name, _ in inspect.getmembers(dpt.__class__, inspect.isdatadescriptor)]) -
                      set(['bits', 'value', '__weakref__', '_b_base_', '_b_needsfree_', '_objects']))
        for name in fields:
            field = dpt.__getattribute__(name)
            if isinstance(field, IntEnum):
                description[name] = field.name
            else:
                description[name] = field
        if (isinstance(dpt, DPT_Float_16) or
                isinstance(dpt, DPT_Float_32)):
            description["decoded_value"] = dpt.decode()
        elif not fields:
            description["value"] = dpt.value
        return dpt.__class__.__name__, description


class DPT(object):
    """
    An abstract KNX DPT
    """

    class Length(Enum):
        LESS_THAN_A_BYTE = "less_than_a_byte"
        A_BYTE_OR_MORE = "a_byte_or_more"

    def __repr__(self):
        description = Description_Factory.make(self)
        return "{} {}".format(description[0], description[1])

    length = Length.A_BYTE_OR_MORE


class _DPT_Switch(LittleEndianStructure):

    _fields_ = [('action', c_uint8, 1)]


class DPT_Switch(Union, DPT):
    """
    >>> import knx_stack
    >>> dpt = knx_stack.datapointtypes.DPT_Switch()
    >>> dpt.value = 0x80
    >>> dpt.action == dpt.Action.off
    True
    >>> dpt.value = 0x81
    >>> dpt.action == dpt.Action.on
    True
    >>> dpt.action = "off"
    >>> dpt.bits.action
    0
    """

    length = DPT.Length.LESS_THAN_A_BYTE

    class Action(IntEnum):
        off = 0x00,
        on = 0x01,

    @property
    def action(self):
        return self.Action(self.bits.action)
    
    @action.setter
    def action(self, value):
        value = getattr(self.Action, value)
        self.bits.action = self.Action(value)

    _fields_ = [('bits', _DPT_Switch),
                ('value', c_uint8)]


class DPT_Alarm(DPT_Switch, DPT):
    """
    >>> import knx_stack
    >>> dpt = knx_stack.datapointtypes.DPT_Alarm()
    >>> dpt.value = 0x80
    >>> dpt.action == dpt.Action.no_alarm
    True
    >>> dpt.value = 0x81
    >>> dpt.action == dpt.Action.alarm
    True
    >>> dpt.action = "no_alarm"
    >>> dpt.bits.action
    0
    """

    length = DPT.Length.LESS_THAN_A_BYTE

    class Action(IntEnum):
        no_alarm = 0x00,
        alarm = 0x01,

    _fields_ = [('bits', _DPT_Switch),
                ('value', c_uint8)]

class _DPT_UpDown(LittleEndianStructure):

    _fields_ = [('direction', c_uint8, 1)]    
    
class DPT_UpDown(Union, DPT):
    """
    >>> import knx_stack
    >>> updown = knx_stack.datapointtypes.DPT_UpDown()
    >>> updown.value = 0x80
    >>> updown.direction == updown.Direction.up
    True
    >>> updown.value = 0x81
    >>> updown.direction == updown.Direction.down
    True
    >>> updown.direction = "up"
    >>> updown.bits.direction
    0
    """

    length = DPT.Length.LESS_THAN_A_BYTE

    class Direction(IntEnum):
        up = 0x00,
        down = 0x01,

    @property
    def direction(self):
        return self.Direction(self.bits.direction)
    
    @direction.setter
    def direction(self, value):
        value = getattr(self.Direction, value)
        self.bits.direction = self.Direction(value)

    _fields_ = [('bits', _DPT_UpDown),
                ('value', c_uint8)]


class _DPT_Start(LittleEndianStructure):

    _fields_ = [('action', c_uint8, 1)]

class DPT_Start(Union, DPT):
    """
    >>> import knx_stack
    >>> start = knx_stack.datapointtypes.DPT_Start()
    >>> start.value = 0x80
    >>> start.action == start.Action.stop
    True
    >>> start.value = 0x81
    >>> start.action == start.Action.start
    True
    >>> start.action = "stop"
    >>> start.bits.action
    0
    """

    length = DPT.Length.LESS_THAN_A_BYTE

    class Action(IntEnum):
        stop = 0x00,
        start = 0x01,

    @property
    def action(self):
        return self.Action(self.bits.action)

    @action.setter
    def action(self, value):
        value = getattr(self.Action, value)
        self.bits.action = self.Action(value)

    _fields_ = [('bits', _DPT_Start),
                ('value', c_uint8)]


class DPT_Info_Switch(DPT_Switch):
    pass

class _DPTVimarScene(LittleEndianStructure):

    _fields_ = [('index', c_uint8, 6),
                ('command', c_uint8, 2)]


class DPTVimarScene(Union, DPT):
    """
    >>> import knx_stack
    >>> scene = knx_stack.datapointtypes.DPTVimarScene()
    >>> scene.value = 0x01
    >>> scene.command == scene.Command.attiva
    True
    >>> scene.index == 1
    True
    >>> scene.command = "identifica"
    >>> scene.bits.command
    3
    """

    class Command(IntEnum):
        attiva = 0x00,
        cancella = 0x01,
        memorizza = 0x02,
        identifica = 0x03

    @property
    def command(self):
        return self.Command(self.bits.command)
    
    @command.setter
    def command(self, value):
        value = getattr(self.Command, value)
        self.bits.command = self.Command(value)
        
    @property
    def index(self):
        return self.bits.index
    
    @index.setter
    def index(self, value):
        self.bits.index = value

    _fields_ = [('bits', _DPTVimarScene),
                ('value', c_uint8)]


class _DPT_SceneControl(LittleEndianStructure):
    _fields_ = [('number', c_uint8, 6),
                ('reserved', c_uint8, 1),
                ('command', c_uint8, 1)]


class DPT_SceneControl(Union, DPT):
    """
    >>> import knx_stack
    >>> scene = knx_stack.datapointtypes.DPT_SceneControl()
    >>> scene.value = 0x01
    >>> scene.command == scene.Command.activate
    True
    >>> scene.number == 1
    True
    >>> scene.command = "learn"
    >>> scene.bits.command
    1
    """

    class Command(IntEnum):
        activate = 0x00,
        learn = 0x01,

    @property
    def command(self):
        return self.Command(self.bits.command)

    @command.setter
    def command(self, value):
        value = getattr(self.Command, value)
        self.bits.command = self.Command(value)

    @property
    def number(self):
        return self.bits.number

    @number.setter
    def number(self, value):
        self.bits.number = value

    _fields_ = [('bits', _DPT_SceneControl),
                ('value', c_uint8)]


class _DPT_Control_Dimming(LittleEndianStructure):

    _fields_ = [('step', c_uint8, 3),
                ('direction', c_uint8, 1)]


class DPT_Control_Dimming(Union, DPT):
    """
    >>> import knx_stack
    >>> c = knx_stack.datapointtypes.DPT_Control_Dimming()
    >>> c.value = 0x0F
    >>> c.step == 7
    True
    >>> c.direction == 1
    True
    >>> c.direction = "down"
    >>> c.value
    7
    """

    class Direction(IntEnum):
        down = 0x00,
        up = 0x01,

    @property
    def step(self):
        return self.bits.step

    @step.setter
    def step(self, value):
        self.bits.step = value

    @property
    def direction(self):
        return self.Direction(self.bits.direction)

    @direction.setter
    def direction(self, value):
        value = getattr(self.Direction, value)
        self.bits.direction = self.Direction(value)

    _fields_ = [('bits', _DPT_Control_Dimming),
                ('value', c_uint8)]

class DPT_Brightness(Union, DPT):
    """
    >>> import knx_stack
    >>> brightness = knx_stack.datapointtypes.DPT_Brightness()
    >>> brightness.value = 0x32
    >>> brightness.value
    50
    """    

    _fields_ = [('bits', c_uint8),
                ('value', c_uint8)]


class _DPTSetupClima(LittleEndianStructure):

    _fields_ = [
                ('temporizzazione', c_uint8, 8),

                ('setpoint', c_uint8, 8),

                ('differenziale', c_uint8, 5),
                ('variazione_setpoint', c_uint8, 2),
                ('unita_misura', c_uint8, 1),

                ('funzionamento', c_uint8, 4),
                ('centralizzato', c_uint8, 1),
                ('stagione', c_uint8, 1),
                ('terziario', c_uint8, 1),
                ('riservato', c_uint8, 1),
                ]


class DPTSetupClima(Union, DPT):
    """
    >>> import knx_stack
    >>> setup = knx_stack.datapointtypes.DPTSetupClima()
    >>> setup.value = 0x00
    >>> setup.funzionamento == setup.Funzionamento.off
    True
    >>> setup.stagione == setup.Stagione.inverno
    True
    >>> setup.setpoint = 200
    >>> setup.bits.setpoint
    200
    """

    class Funzionamento(IntEnum):
        off = 0x00
        forced_off = 0x01
        off_a_tempo = 0x02
        antigelo = 0x03
        riduzione_notturna = 0x04
        riduzione_notturna_a_tempo = 0x05
        manuale = 0x06
        manuale_a_tempo = 0x07
        automatico = 0x08
        automatico_invio_temperatura_abilitato = 0x08
        automatico_invio_temperatura_disabilitato = 0x0E

    class Stagione(IntEnum):
        inverno = 0x00
        estate = 0x01

    class UnitaMisura(IntEnum):
        celsius = 0x00
        farenheit = 0x01

    @property
    def funzionamento(self):
        return self.Funzionamento(self.bits.funzionamento)

    @funzionamento.setter
    def funzionamento(self, value):
        value = getattr(self.Funzionamento, value)
        self.bits.funzionamento = self.Funzionamento(value)

    @property
    def stagione(self):
        return self.Stagione(self.bits.stagione)

    @stagione.setter
    def stagione(self, value):
        value = getattr(self.Stagione, value)
        self.bits.stagione = self.Stagione(value)

    @property
    def unita_misura(self):
        return self.UnitaMisura(self.bits.unita_misura)

    @unita_misura.setter
    def unita_misura(self, value):
        value = getattr(self.UnitaMisura, value)
        self.bits.unita_misura = self.UnitaMisura(value)

    @property
    def centralizzato(self):
        return self.bits.centralizzato

    @centralizzato.setter
    def centralizzato(self, value):
        self.bits.centralizzato = value

    @property
    def terziario(self):
        return self.bits.terziario

    @terziario.setter
    def terziario(self, value):
        self.bits.terziario = value

    @property
    def setpoint(self):
        return self.bits.setpoint

    @setpoint.setter
    def setpoint(self, value):
        self.bits.setpoint = value

    @property
    def differenziale(self):
        return self.bits.differenziale

    @differenziale.setter
    def differenziale(self, value):
        self.bits.differenziale = value

    @property
    def temporizzazione(self):
        return self.bits.temporizzazione

    @temporizzazione.setter
    def temporizzazione(self, value):
        self.bits.temporizzazione = value

    @property
    def variazione_setpoint(self):
        return self.bits.variazione_setpoint

    @variazione_setpoint.setter
    def variazione_setpoint(self, value):
        self.bits.variazione_setpoint = value

    _fields_ = [('bits', _DPTSetupClima),
                ('value', c_uint32)]


class _DPTInfoClimaReport(LittleEndianStructure):

    _fields_ = [
        ('temperatura_lsb', c_uint8, 8),
        ('temperatura_msb', c_uint8, 1),
        ('temporizzazione', c_uint8, 7),

        ('setpoint', c_uint8, 8),

        ('funzionamento', c_uint8, 4),
        ('centralizzato', c_uint8, 1),
        ('stagione', c_uint8, 1),
        ('terziario', c_uint8, 1),
        ('stato_rele', c_uint8, 1),
    ]


class DPTInfoClimaReport(Union, DPT):
    """
    >>> import knx_stack
    >>> info = knx_stack.datapointtypes.DPTInfoClimaReport()
    >>> info.value = 0x00E3E369
    >>> info.temperatura
    36.1
    >>> info.funzionamento == info.Funzionamento.off
    True
    >>> info.stagione == info.Stagione.inverno
    True
    """

    Funzionamento = DPTSetupClima.Funzionamento
    Stagione = DPTSetupClima.Stagione

    @property
    def funzionamento(self):
        return self.Funzionamento(self.bits.funzionamento)

    @funzionamento.setter
    def funzionamento(self, value):
        value = getattr(self.Funzionamento, value)
        self.bits.funzionamento = self.Funzionamento(value)

    @property
    def stagione(self):
        return self.Stagione(self.bits.stagione)

    @stagione.setter
    def stagione(self, value):
        value = getattr(self.Stagione, value)
        self.bits.stagione = self.Stagione(value)

    @property
    def setpoint(self):
        return self.bits.setpoint

    @setpoint.setter
    def setpoint(self, value):
        self.bits.setpoint = value

    @property
    def temperatura(self):
        return ((self.bits.temperatura_msb << 8) + self.bits.temperatura_lsb)/10

    @temperatura.setter
    def temperatura(self, value):
        self.bits.temperatura_msb = int((value*10)) >> 8
        self.bits.temperatura_lsb = int((value*10))

    _fields_ = [('bits', _DPTInfoClimaReport),
                ('value', c_uint32)]


class _DPT_Float_16(LittleEndianStructure):

    _fields_ = [('_mantissa_lsb', c_uint8, 8),

                ('_mantissa_msb', c_uint8, 3),
                ('exponent', c_uint8, 4),
                ('_sign', c_uint8, 1),

                ]

    @property
    def sign(self):
        sign = 1 if self._sign == 0 else -1
        return sign

    @sign.setter
    def sign(self, value):
        if value > 0:
            self._sign = 0
        else:
            self._sign = 1

    @property
    def mantissa(self):
        mantissa = self._mantissa_msb << 8
        mantissa += self._mantissa_lsb
        return mantissa

    @mantissa.setter
    def mantissa(self, value):
        self._mantissa_msb = value >> 8
        self._mantissa_lsb = value


class DPT_Float_16(Union):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Float_16()
    >>> f.value = 1000
    >>> f.decode()
    10.0
    >>> f.value = 2000
    >>> f.decode()
    20.0
    >>> f.value = 100
    >>> f.decode()
    1.0
    >>> f.value = 34806
    >>> f.decode()
    -0.1
    >>> f.value = 34316
    >>> f.decode()
    -5.0
    >>> f.value = 0x8760
    >>> f.decode()
    -1.6
    >>> f.value = 14180
    >>> f.encode(0.5)
    >>> f.decode()
    0.5
    >>> f.encode(19)
    >>> f.value
    1900
    """

    _fields_ = [('bits', _DPT_Float_16),
                ('value', c_uint16)]

    length = DPT.Length.A_BYTE_OR_MORE

    def decode(self):
        mantissa = self.bits.mantissa if self.bits.sign == 1 else self.twos_comp(self.bits.mantissa, 11)
        decoded_data = self.bits.sign*(0.01*mantissa)*(2**self.bits.exponent)
        return decoded_data

    def encode(self, value):
        sign = math.copysign(1, value)

        decimal_mantissa = decimal.Decimal(value/0.01)  # used decimal to avoid different rounding
        mantissa = abs(int(round(decimal_mantissa, 2)))  # two decimals

        exp = 0
        max_mantissa_value = (1 << 11) - 1
        max_exp_value = (1 << 4) - 1

        while mantissa > max_mantissa_value:
            mantissa >>= 1
            exp += 1
        if exp > max_exp_value:
            raise Exception("DPT_Float_16 number not representable")

        self.bits.exponent = exp
        if sign < 0:
            mantissa = (1 << 11) - mantissa
        self.bits.mantissa = mantissa
        self.bits.sign = int(sign)

    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        max_mantissa_value = (1 << bits) - 1
        comp_two = abs(max_mantissa_value - val) + 1
        return comp_two

    def __repr__(self):
        DPT = {"decoded_value": self.decode()}
        return self.__class__.__name__ + ": " + str(DPT)


class DPT_Value_Wsp(DPT_Float_16):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Value_Wsp()
    >>> f.value = 1000
    >>> f.decode()
    10.0
    >>> f.value = 600
    >>> f.decode()
    6.0
    """


class DPT_Value_Temp(DPT_Float_16):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Value_Temp()
    >>> f.value = 1000
    >>> f.decode()
    10.0
    >>> f.value = 1900
    >>> f.decode()
    19.0
    """


class DPT_Value_Lux(DPT_Float_16):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Value_Lux()
    >>> f.value = 1000
    >>> f.decode()
    10.0
    >>> f.encode(30000)
    >>> f.value
    23992
    >>> f.encode(25000)
    >>> f.value
    23748
    >>> f.encode(800)
    >>> f.value
    13538
    """


class DPT_Float_32(Union):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Float_32()
    >>> f.value = 0x45C80000
    >>> f.decode()
    6400.0
    >>> f.value = 0x3F800000
    >>> f.decode()
    1.0
    >>> f.value = 0x43FF8000
    >>> f.decode()
    511.0
    """

    _fields_ = [('bits', c_float),
                ('value', c_uint32)]

    length = DPT.Length.A_BYTE_OR_MORE

    def decode(self):
        return self.bits

    def encode(self, value):
        self.bits = value

    def __repr__(self):
        DPT = {"decoded_value": self.decode()}
        return self.__class__.__name__ + ": " + str(DPT)


class DPT_Value_Power(DPT_Float_32):
    """
    >>> import knx_stack
    >>> f = knx_stack.datapointtypes.DPT_Value_Power()
    """

