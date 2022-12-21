<%
    def addr_to_hex(addr):
        return f"0x{addr:08X}"
%>
<%text># Example</%text>

| Name | Address (hex) | Value (hex) | Value |
|------|---------------|-------------|-------|
| paraBlkExampleLE_uint8 | ${addr_to_hex(paraBlkExampleLE_uint8.addr())} | ${paraBlkExampleLE_uint8.hex()} | ${paraBlkExampleLE_uint8} |
| paraBlkExampleLE_uint16le | ${addr_to_hex(paraBlkExampleLE_uint16le.addr())} | ${paraBlkExampleLE_uint16le.hex()} | ${paraBlkExampleLE_uint16le} |
| paraBlkExampleLE_uint32le | ${addr_to_hex(paraBlkExampleLE_uint32le.addr())} | ${paraBlkExampleLE_uint32le.hex()} | ${paraBlkExampleLE_uint32le} |
| paraBlkExampleLE_uint64le | ${addr_to_hex(paraBlkExampleLE_uint64le.addr())} | ${paraBlkExampleLE_uint64le.hex()} | ${paraBlkExampleLE_uint64le} |
| paraBlkExampleLE_int8 | ${addr_to_hex(paraBlkExampleLE_int8.addr())} | ${paraBlkExampleLE_int8.hex()} | ${paraBlkExampleLE_int8} |
| paraBlkExampleLE_int16le | ${addr_to_hex(paraBlkExampleLE_int16le.addr())} | ${paraBlkExampleLE_int16le.hex()} | ${paraBlkExampleLE_int16le} |
| paraBlkExampleLE_int32le | ${addr_to_hex(paraBlkExampleLE_int32le.addr())} | ${paraBlkExampleLE_int32le.hex()} | ${paraBlkExampleLE_int32le} |
| paraBlkExampleLE_float32le | ${addr_to_hex(paraBlkExampleLE_float32le.addr())} | ${paraBlkExampleLE_float32le.hex()} | ${paraBlkExampleLE_float32le} |
| paraBlkExampleLE_float64le | ${addr_to_hex(paraBlkExampleLE_float64le.addr())} | ${paraBlkExampleLE_float64le.hex()} | ${paraBlkExampleLE_float64le} |
| paraBlkExampleLE_utf8 | ${addr_to_hex(paraBlkExampleLE_utf8.addr())} | ${paraBlkExampleLE_utf8.hex()} | ${m_read_string(paraBlkExampleLE_utf8.addr())} |
