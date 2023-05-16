<%
    def addr_to_hex(addr):
        return f"0x{addr:08X}"
%>
<%text># Example</%text>

| Name | Address (hex) | Value (hex) | Value |
|------|---------------|-------------|-------|
% for element in config_elements:
| ${element.name()} | ${addr_to_hex(element.addr())} | ${element.hex()} | ${element} |
% endfor
