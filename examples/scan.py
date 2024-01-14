"""
Scan for iTag devices

Press and hold iTag button to power on. iTag beeps twice and blinks LED to indicate device is on.

* scans for nearby iTag devices
* prints their public mac addresses

Press and hold iTag button to power off. iTag long-beeps once to indicate device is now off.

Example output:
	Scanning for iTag devices
	Found device: ff:ff:70:03:ef:92, Best RSSI: -51
	Found device: ff:ff:33:31:8a:76, Best RSSI: -66
"""

# My iTag public mac addresses
# ff:ff:33:31:8a:76 = Blue iTag
# ff:ff:70:03:ef:92 = Pink iTag
# ff:ff:20:03:ce:bf = Green iTag
# ff:ff:33:01:9a:e4 = Black iTag
# ff:ff:99:90:3c:34 = White iTag

import uasyncio as asyncio
import aioble
import bluetooth

async def main():
	devices = dict()

	print('Scanning for iTag devices')
	async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
		async for result in scanner:
			# Note: there's a bunch of whitespace in the tags result name, eg. "iTAG            "
			if result.name() is not None and result.name().startswith("iTAG") and result.device.addr_type == 0x00:
				addr = result.device.addr_hex()
				if addr not in devices:
					# Add match to dict
					devices[addr] = result.rssi
				elif devices[addr] < result.rssi:
					# Update best RSSI
					devices[addr] = result.rssi

		# Print scan results
		for device in devices:
			print(f'Found device: {device}, Best RSSI: {devices[device]}')

asyncio.run(main())
