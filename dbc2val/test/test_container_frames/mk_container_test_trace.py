#! /usr/bin/python3
#
# Produces a shell script that can be used to generate the trace file
# included with this test. This assumes the usage of socketcan (i.e.,
# Linux) and the presence of the can-utils package. Usage:
#
#    sudo ip link add dev vcan0 type vcan
#    sudo ip link set dev vcan0 up
#    # (run `candump -L vcan0` in a different terminal window)
#    eval $(python3 ./mk_container_test_trace.py)
import cantools
import time
import sys

db = cantools.database.load_file(sys.argv[1])

m = db.get_message_by_name("OneToContainThemAll")

cm = m.get_contained_message_by_name("message2")

# send the signal using a container message. make sure that the
# receiver ignores garbage
raw = m.encode([("message2", {
    'signal3': 2,
    'signal2': 0x123,
    'signal4': "two",
}),
        (cm.header_id, bytes([0x77]*(cm.length+1))),
        (cm.header_id, bytes([0x55]*(cm.length-1))),
          ])
raw += b'\x10\x20\x30\x00'
print(f"cansend vcan0 {m.frame_id:x}##5{raw.hex()};")
print("sleep 2;")

# send a container frame which does not contain the signal
raw = m.encode([("message1", {
           "message1_SeqCounter": 1,
           "message1_CRC": 2,
           "signal6": 0.05,
           "signal1": 4,
           "signal5": 5,
}),
          ])

print(f"cansend vcan0 {m.frame_id:x}##5{raw.hex()};")
print("sleep 1;")

# send the signal using a normal message
m = db.get_message_by_name("Message2")
raw = m.encode({
    'signal3': 3,
    'signal2': 0x124,
    'signal4': "one",
})
print(f"cansend vcan0 {m.frame_id:x}#{raw.hex()};")
print("sleep 0.5;")

# send a garbled message which normally would contain the signal
print(f"cansend vcan0 {m.frame_id:x}#001122;")
print("sleep 0.25;")


# send an unrelated message
print(f"cansend vcan0 123#001122;")
print("sleep 0.125;")
