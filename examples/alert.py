"""
Writes to the Immediate Alert service to make the iTag beep

Press and hold iTag button to power on. iTag beeps twice and blinks LED to indicate device is on.

* Connects to specific tag by its public address
* Reads battery level and prints (as percentage, 0-100)
* Writes 0x01 to the alert service to make tag start fast-beeping for 5 sec
* Writes 0x00 to the alert service to make tag stop fast-beeping
* Disconnects from tag
* Tag starts slow-beeping indicating it's been disconnected. Press tag button to ack.

Press and hold iTag button to power off. iTag long-beeps once to indicate device is now off.

Example output:
	Connecting to Blue iTag ("ff:ff:33:31:8a:76")
	Connected
	Battery: 99%
	Start fast-beeping for 5sec
	Stop fast-beeping
	Disconnect
	iTag will start slow-beeping. Press button to ack.
"""

import uasyncio as asyncio
import aioble
import bluetooth

# org.bluetooth.service.immediate_alert
_IM_ALERT_UUID = bluetooth.UUID(0x1802)

# org.bluetooth.characteristic.alert_level
_IM_ALERT_LEVEL_UUID = bluetooth.UUID(0x2A06)
# write 0x00 no alert
# write 0x01 mild alert
# write 0x02 high alert
# 0x03..0xff is reserved
# The iTag does not support different alert levels.
# It beeps the same volume/frequency for 0x01-0xFF.

# org.bluetooth.service.battery_service
_BAT_UUID = bluetooth.UUID(0x180F)

# org.bluetooth.characteristic.battery_level
_BAT_LEVEL_UUID = bluetooth.UUID(0x2A19)
# Returns a percentage 0x00..0x64 for 0-100%

# The public mac address of my blue iTAG
_BLUE_ITAG_PUBLIC_ADDR = "ff:ff:33:31:8a:76"

async def main():
	device = aioble.Device(aioble.ADDR_PUBLIC, _BLUE_ITAG_PUBLIC_ADDR)
	try:
		print(f'Connecting to Blue iTag ("{_BLUE_ITAG_PUBLIC_ADDR}")')
		connection = await device.connect()
	except asyncio.TimeoutError:
		print("Connection timeout")
		return

	async with connection:
		print("Connected")

		try:
			bat_service = await connection.service(_BAT_UUID)
			bat_level_characteristic = await bat_service.characteristic(_BAT_LEVEL_UUID)

			im_alert_service = await connection.service(_IM_ALERT_UUID)
			alert_level_characteristic = await im_alert_service.characteristic(_IM_ALERT_LEVEL_UUID)
		except asyncio.TimeoutError:
			print("Timeout discovering services/characteristics")
			return

		# Read battery level
		level = await bat_level_characteristic.read()
		print(f"Battery: {level[0]}%")
		await asyncio.sleep_ms(1000)

		# Start fast-beeping
		print("Start fast-beeping for 5sec")
		await alert_level_characteristic.write(b'\x01')
		await asyncio.sleep_ms(5000)

		# Stop fast-beeping
		print("Stop fast-beeping")
		await alert_level_characteristic.write(b'\x00')
		await asyncio.sleep_ms(500)

		print("Disconnect")
		# iTag starts slow-beeping to warn about disconnection
		print("iTag will start slow-beeping. Press button to ack.")

asyncio.run(main())
