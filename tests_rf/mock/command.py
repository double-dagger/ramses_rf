#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""RAMSES RF - a RAMSES-II protocol decoder & analyser.

Mocked devices used for testing.Will provide an appropriate Tx for a given Rx.
"""

from __future__ import annotations

from ramses_rf.protocol.address import NON_DEV_ADDR
from ramses_rf.protocol.command import Command, validate_api_params
from ramses_rf.protocol.const import I_, RP, Code
from ramses_rf.protocol.helpers import flag8_to_hex

# from .const import __dev_mode__


class MockCommand(Command):
    @classmethod  # constructor for I/RP|0005
    @validate_api_params()
    def put_system_zones(
        cls,
        src_id: str,
        zone_type: str,  # payload[2:4], aka heating_type, zone_class
        zone_mask: list[int],  # payload[4:6]
        dst_id: str = None,
    ) -> Command:
        """Constructor for I/RP|0005."""

        if dst_id is None:
            verb = I_
            addr2 = src_id
        else:
            verb = RP
            addr2 = NON_DEV_ADDR.id

        zone_mask = flag8_to_hex(zone_mask[:8], lsb=True) + flag8_to_hex(
            zone_mask[8:], lsb=True
        )
        payload = f"00{zone_type}{zone_mask}"

        return cls._from_attrs(
            verb, Code._0005, payload, addr0=src_id, addr1=dst_id, addr2=addr2
        )

    @classmethod  # constructor for I|31D9
    @validate_api_params()
    def _put_fan_state(
        cls,
        fan_id: str,
        _flags: str,  # payload[2:4]
        fan_mode: str,  # payload[4:6]
        *,
        sub_idx: str = "00",
    ):
        """Constructor for I|31DA."""

        payload = f"{sub_idx}{_flags}{fan_mode}"

        return cls._from_attrs(RP, Code._31D9, payload, addr0=fan_id, addr2=fan_id)
