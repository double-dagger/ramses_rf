#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""RAMSES RF - a RAMSES-II protocol decoder & analyser.

Test the Command.put_*, Command.set_* APIs.
"""

from datetime import datetime as dt

from ramses_rf.const import SZ_DOMAIN_ID
from ramses_rf.helpers import shrink
from ramses_rf.protocol.address import HGI_DEV_ADDR

from ramses_rf.protocol.message import Message
from ramses_rf.protocol.packet import Packet
from tests.common import gwy  # noqa: F401

from tests_rf.mock.command import MockCommand as Command


def _test_api_good(gwy, api, packets):  # noqa: F811  # NOTE: incl. addr_set check
    """Test a verb|code pair that has a Command constructor."""

    for pkt_line in packets:
        pkt = _assert_pkt_from_frame(gwy, pkt_line.split("#")[0].rstrip())
        msg = Message(gwy, pkt)

        _assert_cmd_from_msg(api, msg)

        if isinstance(packets, dict) and (payload := packets[pkt_line]):
            assert shrink(msg.payload, keep_falsys=True) == eval(payload)


def _assert_pkt_from_frame(gwy, pkt_line) -> Packet:  # noqa: F811
    """Create a pkt from a pkt_line and assert their frames match."""

    pkt = Packet.from_port(gwy, dt.now(), pkt_line)
    assert str(pkt) == pkt_line[4:]
    return pkt


def _assert_cmd_from_msg(api, msg) -> None:  # noqa: F811

    cmd = api(
        msg.src.id,
        **{k: v for k, v in msg.payload.items() if k[:1] != "_"},
        dst_id=msg.dst.id,
    )

    assert cmd == msg._pkt  # assert str(cmd) == str(pkt)
    assert cmd.dst.id == msg._pkt.dst.id
    assert cmd.verb == msg._pkt.verb
    assert cmd.code == msg._pkt.code
    assert cmd.payload == msg._pkt.payload

    return cmd


def test_pet_0005(gwy):  # noqa: F811
    _test_api_good(gwy, Command.put_system_zones, PUT_0005_GOOD)


PUT_0005_GOOD = (
    # "...  I --- 01:145038 --:------ 01:145038 0005 004 00087B0F",
    "... RP --- 01:145038 18:000730 --:------ 0005 004 00087B0F",
)
