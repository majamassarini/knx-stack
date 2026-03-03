from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    """PropertyValueWrite confirmation message."""

    asap: knx_stack.ASAP
    object_index: int
    property_id: int
    number_of_elements: int
    start_index: int
    data: str
    status: knx_stack.layer.link.ConfirmFlag

    def __repr__(self):
        return (
            "PropertyValueWriteCon {} status {} (object index {}, property id {}, number of elements {}, "
            "start index {} for asap {})".format(
                self.data,
                self.status.value,
                self.object_index,
                self.property_id,
                self.number_of_elements,
                self.start_index,
                self.asap,
            )
        )
