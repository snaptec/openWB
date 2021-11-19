from typing import Type, Union
try:
    from ..common import lovato
    from ..common import mpm3pm
    from ..common import sdm630
    from ..common.module_error import ModuleError, ModuleErrorLevel
except (ImportError, ValueError, SystemError):
    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import sdm630
    from modules.common.module_error import ModuleError, ModuleErrorLevel


def kit_version_factory(version: int) -> Type[Union[mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]]:
    if version == 0:
        return mpm3pm.Mpm3pm
    elif version == 1:
        return lovato.Lovato
    elif version == 2:
        return sdm630.Sdm630
    else:
        raise ModuleError("Version "+str(version) +
                          " unbekannt.", ModuleErrorLevel.ERROR)
