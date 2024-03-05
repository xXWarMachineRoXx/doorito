from etimetracklite import eTimeTrackLite

machine = eTimeTrackLite(domain="192.168.2.201")
machine.set_request_body({
	"from_time": "2023-12-05 07:30:30",
	"to_time": "2023-12-05 08:30:30",
	"serial_no": "CGKK220762223",
	"username": "essl",
	"password": "essl",
})
machine.fetch_logs()
print(machine.logs[0]) # ['1002', '2023-12-05 07:30:30', '']