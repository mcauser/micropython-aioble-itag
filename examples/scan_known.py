"""
Scan for known iTag devices

Press and hold iTag button to power on. iTag beeps twice and blinks LED to indicate device is on.

* scans for nearby iTag devices
* looks for specific known iTag devices by their public address
* prints results

Press and hold iTag button to power off. iTag long-beeps once to indicate device is now off.

Example output:
	Scanning for known iTag devices
	Found iTag: Green (ff:ff:20:03:ce:bf), RSSI: -54
	Found iTag: Blue (ff:ff:33:31:8a:76), RSSI: -60
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

known = {
	'ff:ff:33:31:8a:76': 'Blue',
	'ff:ff:70:03:ef:92': 'Pink',
	'ff:ff:20:03:ce:bf': 'Green',
	'ff:ff:33:01:9a:e4': 'Black',
	'ff:ff:99:90:3c:34': 'White'
}

async def main():
	devices = dict()

	print('Scanning for known iTag devices')
	async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
		async for result in scanner:
			# Note: there's a bunch of whitespace in the tags result name, eg. "iTAG            "
			if result.name() is not None and result.name().startswith("iTAG") and result.device.addr_type == 0x00:
				addr = result.device.addr_hex()
				if addr not in devices and addr in known.keys():
					print(f'Found iTag: {known[addr]} ({addr}), RSSI: {result.rssi}')
					# Add match to dict so it only shows once
					devices[addr] = result.rssi

asyncio.run(main())
