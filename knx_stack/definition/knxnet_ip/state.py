import knx_stack.state


class State(knx_stack.state.State):

    def __init__(self, medium, association_table=None, datapointtypes=None):
        super(State, self).__init__(medium, association_table, datapointtypes)
        self._communication_channel_id = 0

    @property
    def communication_channel_id(self):
        return self._communication_channel_id

    @communication_channel_id.setter
    def communication_channel_id(self, value):
        self._communication_channel_id = value
