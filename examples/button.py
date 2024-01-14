"""
Listens for button presses via the custom service

Press and hold iTag button to power on. iTag beeps twice and blinks LED to indicate device is on.

* Connects to specific tag by its public address
* Listens for button presses
* Disconnects from tag
* Tag starts slow-beeping indicating it's been disconnected. Press tag button to ack.

Press and hold iTag button to power off. iTag long-beeps once to indicate device is now off.

The tag has a custom service (0xffe0) with custom characteristic (0xffe1) with value 0x01.
Each time you press the iTag button, it sends a notification with value 0x01.

Example output:
	Connecting to Blue iTag ("ff:ff:33:31:8a:76")
	Connected
	Listen for 5x iTag button presses
	Waiting for button press 1/5
	Button press 1/5 detected. Custom characteristic was notified with value: 0x01
	Waiting for button press 2/5
	Button press 2/5 detected. Custom characteristic was notified with value: 0x01
	Waiting for button press 3/5
	Button press 3/5 detected. Custom characteristic was notified with value: 0x01
	Waiting for button press 4/5
	Button press 4/5 detected. Custom characteristic was notified with value: 0x01
	Waiting for button press 5/5
	Button press 5/5 detected. Custom characteristic was notified with value: 0x01
	Disconnect
	iTag will start slow-beeping. Press button to ack.
"""

import uasyncio as asyncio
import aioble
import bluetooth

# org.bluetooth.service.custom_service
_CUSTOM_SVC_UUID = bluetooth.UUID(0xFFE0)

# org.bluetooth.characteristic.custom
_CUSTOM_CHAR_UUID = bluetooth.UUID(0xFFE1)

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
			custom_service = await connection.service(_CUSTOM_SVC_UUID)
			custom_characteristic = await custom_service.characteristic(_CUSTOM_CHAR_UUID)
		except asyncio.TimeoutError:
			print("Timeout discovering services/characteristics")
			return

		# Listen for 5 button presses
		print("Listen for 5x iTag button presses")

		for i in range(5):
			print(f"Waiting for button press {i+1}/5")
			data = await custom_characteristic.notified()
			print(f"Button press {i+1}/5 detected. Custom characteristic was notified with value: 0x{data[0]:02X}")
			# Note: value is always 0x01

		await asyncio.sleep_ms(500)

		print("Disconnect")
		# iTag starts slow-beeping to warn about disconnection
		print("iTag will start slow-beeping. Press button to ack.")

asyncio.run(main())
