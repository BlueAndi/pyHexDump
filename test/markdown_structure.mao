<%text># Aurix TC397 - Blinky Example</%text>

<%text>## User Control Block 00</%text>

|Short Name|Value|
|----------|-----|
| BMI_BMHDID | ${UCB00.BMI_BMHDID.hex()} |
| STAD | ${UCB00.STAD.hex()} |
| CRCBMHD | ${UCB00.CRCBMHD.hex()} |
| CRCBMHD_N | ${UCB00.CRCBMHD_N.hex()} |
| PWx | ${UCB00.PWx.hex()} |
| CONFIRMATION | ${UCB00.CONFIRMATION.hex()} |
<%
    bmi_bmhdid = UCB00.BMI_BMHDID
    bmi    = (bmi_bmhdid >>  0) & 0xFFFF
    bmhdid = (bmi_bmhdid >>  16) & 0xFFFF
    pindis = (bmi >> 0) & 0x01
    hwcfg  = (bmi >> 1) & 0x07

    mode_by_hwcfg = "disabled"
    if pindis == 0:
        mode_by_hwcfg = "enabled"

    start_up_mode = "invalid"
    if hwcfg == 0x07:
        start_up_mode = "internal start from flash"
    elif hwcfg == 0x06:
        start_up_mode = "alternate boot mode"
    elif hwcfg == 0x04:
        start_up_mode = "generic bootstrap loader mode"
    elif hwcfg == 0x03:
        start_up_mode = "asc bootstrap loader mode"
    
    is_bmh_valid = "invalid"
    if bmhdid == 0xB359:
        is_bmh_valid = "OK"

    calculated_crc_bmhd = m_calc_checksum("u32le", UCB00.BMI_BMHDID.addr(), UCB00.CRCBMHD.addr(), 0x04c11db7, 32, 0xffffffff, True, True, True)
    calculated_crc_bmhd_n = m_calc_checksum("u32le", UCB00.BMI_BMHDID.addr(), UCB00.CRCBMHD.addr(), 0x04c11db7, 32, 0xffffffff, True, True, False)

    is_bmh_integrity_given = "Not OK"
    if calculated_crc_bmhd == UCB00.CRCBMHD:
        if calculated_crc_bmhd_n == UCB00.CRCBMHD_N:
            is_bmh_integrity_given = "OK"
%>
<%text>### Boot Mode Index (BMI)</%text>
* Mode selection by configuration pins: ${mode_by_hwcfg}
* Start-up mode: ${start_up_mode}

<%text>### Boot Mode Header Identifier (BMHDID)</%text>
Is boot mode header valid: ${is_bmh_valid}

<%text>### Boot Mode Header CRC (CRCBMHD/CRCBMHD_N)</%text>
Is boot mode header integrity given: ${is_bmh_integrity_given}
