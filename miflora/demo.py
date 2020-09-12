from btlewrap import BluepyBackend

from miflora import miflora_scanner
from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)

def main():
    poller = MiFloraPoller("C4:7C:8D:6A:8D:03", BluepyBackend)
    print(poller.firmware_version())

if __name__ == "__main__":
    main()
