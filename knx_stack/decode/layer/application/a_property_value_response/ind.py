from __future__ import annotations
from collections.abc import Iterable
from knx_stack.definition.layer.application.a_property_value_response.ind import (
    Msg,
)
from knx_stack.decode.layer.application import a_property_value
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[Msg]:
    property_values = a_property_value.decode(state, msg)
    property_values_read = [
        Msg(
            asap=property_value.asap,
            object_index=property_value.object_index,
            property_id=property_value.property_id,
            number_of_elements=property_value.number_of_elements,
            start_index=property_value.start_index,
            data=property_value.data,  # type: ignore[arg-type]
        )
        for property_value in property_values
    ]
    return property_values_read
