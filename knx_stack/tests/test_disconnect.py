import unittest
import knx_stack


class TestDisconnect(unittest.TestCase):

    # DisconnectRequest from gateway: channel 5, control endpoint 127.0.0.1:1234
    DISCONNECT_REQUEST_MSG = "061002090010050008017F00000104D2"
    # DisconnectResponse: channel 5, status E_NO_ERROR
    DISCONNECT_RESPONSE_MSG = "0610020A00080500"

    def test_disconnect_request_decode(self):
        """Test decoding DISCONNECT_REQUEST from gateway"""
        state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip)
        state.communication_channel_id = 5
        msg = knx_stack.knxnet_ip.Msg.make_from_str(
            self.DISCONNECT_REQUEST_MSG
        )
        data = knx_stack.decode_msg(state, msg)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(
            data[0], knx_stack.knxnet_ip.core.disconnect.req.Msg
        )
        self.assertEqual(data[0].addr_control_endpoint, "127.0.0.1")
        self.assertEqual(data[0].port_control_endpoint, 1234)

    def test_disconnect_response_encode(self):
        """Test encoding DISCONNECT_RESPONSE to gateway"""
        state = knx_stack.knxnet_ip.State(
            knx_stack.Medium.knxnet_ip, None, None
        )
        state.communication_channel_id = 5
        disconnect_res = knx_stack.knxnet_ip.core.disconnect.res.Msg(
            communication_channel_id=5,
            status=knx_stack.knxnet_ip.ErrorCodes.E_NO_ERROR,
        )
        encoded = knx_stack.encode_msg(state, disconnect_res)
        self.assertEqual(
            str(encoded).upper(), self.DISCONNECT_RESPONSE_MSG.upper()
        )

    def test_disconnect_request_encode(self):
        """Test encoding DISCONNECT_REQUEST from client"""
        state = knx_stack.knxnet_ip.State(
            knx_stack.Medium.knxnet_ip, None, None
        )
        state.communication_channel_id = 5
        disconnect_req = knx_stack.knxnet_ip.core.disconnect.req.Msg(
            addr_control_endpoint="127.0.0.1", port_control_endpoint=1234
        )
        encoded = knx_stack.encode_msg(state, disconnect_req)
        self.assertEqual(
            str(encoded).upper(), self.DISCONNECT_REQUEST_MSG.upper()
        )
