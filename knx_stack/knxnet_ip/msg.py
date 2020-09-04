import struct
import socket

from knx_stack import Msg as Parent


class Msg(Parent):

    def HPAI(self):
        """
        Host protocol address information
        """
        (struct_len, body) = self.octect()
        (ipv4_udp, body) = body.octect()
        (ip, body) = body.long()
        (port, body) = body.short()
        return (socket.inet_ntoa(struct.pack('!I', ip.value)),
                port.value,
                body)

    def CRI(self):
        """
        Connection request information
        """
        (struct_len, body) = self.octect()
        (tunnel_connection, body) = body.octect()
        (knx_layer, body) = body.octect()
        (reserved, body) = body.octect()
        return tunnel_connection.value, knx_layer.value, body

    def CRD(self):
        """
        Connection Response Data Block
        """
        (struct_len, body) = self.octect()
        (tunnel_connection, body) = body.octect()
        (individual_address, body) = body.short()
        return tunnel_connection.value, individual_address.value, body

    def header(self):
        """
        Connection Header
        """
        (struct_len, body) = self.octect()
        (communication_channel_id, body) = body.octect()
        (sequence_counter, body) = body.octect()
        (status, body) = body.octect()
        return communication_channel_id.value, sequence_counter.value, status.value, body
