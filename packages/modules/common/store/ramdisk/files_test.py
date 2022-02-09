from modules.common.store.ramdisk import files


def test_get_file_path():
    # Battery
    # -------
    assert files.battery.energy_exported.filename == "speicherekwh"
    assert files.battery.energy_imported.filename == "speicherikwh"
    assert files.battery.power.filename == "speicherleistung"
    assert files.battery.soc.filename == "speichersoc"

    # Charge points
    # -------------
    assert files.charge_points[0].current_target.filename == "llsoll"
    assert files.charge_points[1].current_target.filename == "llsolls1"
    assert files.charge_points[2].current_target.filename == "llsolls2"
    assert files.charge_points[3].current_target.filename == "llsolllp4"
    assert files.charge_points[4].current_target.filename == "llsolllp5"

    assert files.charge_points[0].currents[0].filename == "lla1"
    assert files.charge_points[0].currents[1].filename == "lla2"
    assert files.charge_points[0].currents[2].filename == "lla3"
    assert files.charge_points[1].currents[0].filename == "llas11"
    assert files.charge_points[1].currents[1].filename == "llas12"
    assert files.charge_points[1].currents[2].filename == "llas13"
    assert files.charge_points[2].currents[0].filename == "llas21"
    assert files.charge_points[2].currents[1].filename == "llas22"
    assert files.charge_points[2].currents[2].filename == "llas23"
    assert files.charge_points[3].currents[0].filename == "lla1lp4"
    assert files.charge_points[3].currents[1].filename == "lla2lp4"
    assert files.charge_points[3].currents[2].filename == "lla3lp4"
    assert files.charge_points[4].currents[0].filename == "lla1lp5"
    assert files.charge_points[4].currents[1].filename == "lla2lp5"
    assert files.charge_points[4].currents[2].filename == "lla3lp5"

    assert files.charge_points[0].energy.filename == "llkwh"
    assert files.charge_points[1].energy.filename == "llkwhs1"
    assert files.charge_points[2].energy.filename == "llkwhs2"
    assert files.charge_points[3].energy.filename == "llkwhlp4"
    assert files.charge_points[4].energy.filename == "llkwhlp5"

    assert files.charge_points[0].frequency.filename == "llhz"
    assert files.charge_points[1].frequency.filename == "llhzs1"
    assert files.charge_points[2].frequency.filename == "llhzs2"

    assert files.charge_points[0].is_charging.filename == "chargestat"
    assert files.charge_points[1].is_charging.filename == "chargestats1"
    assert files.charge_points[2].is_charging.filename == "chargestatlp3"
    assert files.charge_points[3].is_charging.filename == "chargestatlp4"
    assert files.charge_points[4].is_charging.filename == "chargestatlp5"

    assert files.charge_points[0].is_plugged.filename == "plugstat"
    assert files.charge_points[1].is_plugged.filename == "plugstats1"
    assert files.charge_points[2].is_plugged.filename == "plugstatlp3"
    assert files.charge_points[3].is_plugged.filename == "plugstatlp4"
    assert files.charge_points[4].is_plugged.filename == "plugstatlp5"

    assert files.charge_points[0].power.filename == "llaktuell"
    assert files.charge_points[1].power.filename == "llaktuells1"
    assert files.charge_points[2].power.filename == "llaktuells2"
    assert files.charge_points[3].power.filename == "llaktuelllp4"
    assert files.charge_points[4].power.filename == "llaktuelllp5"

    assert files.charge_points[0].power_factors[0].filename == "llpf1"
    assert files.charge_points[0].power_factors[1].filename == "llpf2"
    assert files.charge_points[0].power_factors[2].filename == "llpf3"
    assert files.charge_points[1].power_factors[0].filename == "llpfs11"
    assert files.charge_points[1].power_factors[1].filename == "llpfs12"
    assert files.charge_points[1].power_factors[2].filename == "llpfs13"
    assert files.charge_points[2].power_factors[0].filename == "llpfs21"
    assert files.charge_points[2].power_factors[1].filename == "llpfs22"
    assert files.charge_points[2].power_factors[2].filename == "llpfs23"

    assert files.charge_points[0].soc.filename == "soc"
    assert files.charge_points[1].soc.filename == "soc1"

    assert files.charge_points[0].voltages[0].filename == "llv1"
    assert files.charge_points[0].voltages[1].filename == "llv2"
    assert files.charge_points[0].voltages[2].filename == "llv3"
    assert files.charge_points[1].voltages[0].filename == "llvs11"
    assert files.charge_points[1].voltages[1].filename == "llvs12"
    assert files.charge_points[1].voltages[2].filename == "llvs13"
    assert files.charge_points[2].voltages[0].filename == "llvs21"
    assert files.charge_points[2].voltages[1].filename == "llvs22"
    assert files.charge_points[2].voltages[2].filename == "llvs23"
    assert files.charge_points[3].voltages[0].filename == "llv1lp4"
    assert files.charge_points[3].voltages[1].filename == "llv2lp4"
    assert files.charge_points[3].voltages[2].filename == "llv3lp4"
    assert files.charge_points[4].voltages[0].filename == "llv1lp5"
    assert files.charge_points[4].voltages[1].filename == "llv2lp5"
    assert files.charge_points[4].voltages[2].filename == "llv3lp5"

    # EVU
    # ---
    assert files.evu.currents[0].filename == "bezuga1"
    assert files.evu.currents[1].filename == "bezuga2"
    assert files.evu.currents[2].filename == "bezuga3"

    assert files.evu.energy_export.filename == "einspeisungkwh"
    assert files.evu.energy_import.filename == "bezugkwh"
    assert files.evu.frequency.filename == "evuhz"

    assert files.evu.power_factors[0].filename == "evupf1"
    assert files.evu.power_factors[1].filename == "evupf2"
    assert files.evu.power_factors[2].filename == "evupf3"

    assert files.evu.power_import.filename == "wattbezug"

    assert files.evu.powers_import[0].filename == "bezugw1"
    assert files.evu.powers_import[1].filename == "bezugw2"
    assert files.evu.powers_import[2].filename == "bezugw3"

    assert files.evu.voltages[0].filename == "evuv1"
    assert files.evu.voltages[1].filename == "evuv2"
    assert files.evu.voltages[2].filename == "evuv3"

    # PV
    # --
    assert files.pv[0].currents[0].filename == "pva1"
    assert files.pv[0].currents[1].filename == "pva2"
    assert files.pv[0].currents[2].filename == "pva3"
    assert files.pv[1].currents[0].filename == "pv2a1"
    assert files.pv[1].currents[1].filename == "pv2a2"
    assert files.pv[1].currents[2].filename == "pv2a3"

    assert files.pv[0].energy.filename == "pvkwh"
    assert files.pv[1].energy.filename == "pv2kwh"

    assert files.pv[0].power.filename == "pvwatt"
    assert files.pv[1].power.filename == "pv2watt"
