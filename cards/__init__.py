from smartcard.System import readers
from smartcard.util import toHexString

# Connect to the first available smart card reader
reader = readers()[0]
connection = reader.createConnection()
connection.connect()

# Define the command APDU for writing data to the smart card
write_cmd = [0xFF, 0xD0, 0x00, 0x00, 0x10]  # 0xFFD0000010
data_to_write = b"Hello, world!"

# Send the write command APDU to the smart card
write_response, _ = connection.transmit(write_cmd + list(data_to_write))
print("Write response:", toHexString(write_response))

# Define the command APDU for reading data from the smart card
read_cmd = [0xFF, 0xB0, 0x00, 0x00, 0x10]  # 0xFFB0000010

# Send the read command APDU to the smart card
read_response, _ = connection.transmit(read_cmd)
print("Read response:", toHexString(read_response))
