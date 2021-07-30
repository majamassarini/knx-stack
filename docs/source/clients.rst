Clients
=======

The following are simple examples of asynchronous KNX clients using this project code.

USB HID
-------

.. automodule:: knx_stack.client.usbhid

KNXnet IP Tunneling Client
--------------------------

.. automodule:: knx_stack.client.knxnet_ip

KNXnet IP Discovery Request/Listen services
-------------------------------------------

A simple discovery script, able to discover KNXnet IP gateways, is already shipped with this package.

When calling the script specify your ip address::

  python3 -m knx_stack.client.knxnet_ip_discovery 172.31.10.111

.. automodule:: knx_stack.client.knxnet_ip_discovery
