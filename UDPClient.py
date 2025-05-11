import socket
import xml.etree.ElementTree as ET


class UDPClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345):
        """Initialize the UDP client."""
        self.server = (server_host, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)

    def send(self, message: bytes):
        """Send an XML message to the server and receive the response."""
        try:
            # Outgoing XML parsing (no schema validation)
            outgoing_xml = message.decode('utf-8')
            outgoing_element = ET.fromstring(outgoing_xml)
            print("[MEME_MAYHEM/UDP_CLIENT]: <SENT_MSG> ~ \n", outgoing_xml)

        except ET.ParseError as e:
            print(f"[MEME_MAYHEM/UDP_CLIENT]: <INVALID_OUTGOING_XML> ✗\nError: {e}")
            return None

        try:
            # Send the message to the server
            self.sock.sendto(message, self.server)

            # Receive server response
            data, _ = self.sock.recvfrom(4096)
            xml_data = data.decode('utf-8')

            print(f"[MEME_MAYHEM/UDP_CLIENT]: <RECEIVED_RAW> ~ \n{xml_data}")

            try:
                # Parse the incoming response
                incoming_element = ET.fromstring(xml_data)

                print("[MEME_MAYHEM/UDP_CLIENT]: <INCOMING_XML_PARSED> ✓")

                return incoming_element

            except ET.ParseError as e:
                print(f"[MEME_MAYHEM/UDP_CLIENT]: <INVALID_INCOMING_XML> ✗\nError: {e}")
                return None

        except socket.timeout:
            print("[MEME_MAYHEM/UDP_CLIENT]: <RECEIVE_TIMEOUT> Response from server timed out")
            return None

        except Exception as e:
            print(f"[MEME_MAYHEM/UDP_CLIENT]: <UNEXPECTED_ERROR> ⚠\nError: {e}")
            return None

    def close(self):
        """Close the UDP socket."""
        self.sock.close()
