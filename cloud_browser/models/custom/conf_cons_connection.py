class ConfConsConnection:
    def __init__(self, server_name, ip_address, operating_system, group, putty_session):
        self.group = group
        self.ip_address = ip_address
        self.name = server_name
        self.operating_system = operating_system
        self.putty_session = putty_session
