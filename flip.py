import socket

HOST = "10.114.162.203"
PORT = 1337

username = b"admin&password=tUp3rPaSs1"
password = b"B" * 16

def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

with socket.create_connection((HOST, PORT)) as s:
    print(recv_until(s, b"username: ").decode(errors="ignore"), end="")
    s.sendall(username + b"\n")

    print(recv_until(s, b"password: ").decode(errors="ignore"), end="")
    s.sendall(password + b"\n")

    data = recv_until(s, b"enter ciphertext: ")
    text = data.decode(errors="ignore")
    print(text, end="")

    ct_hex = text.split("Leaked ciphertext: ")[1].splitlines()[0].strip()
    ct = bytearray.fromhex(ct_hex)

    # We want to change the last byte of plaintext block 2 from 't' to 's'
    # In CBC:
    # P2 = D(C2) XOR C1
    # so changing the last byte of C1 changes the last byte of P2
    #
    # old_plain_byte ^ old_cipher_byte ^ new_cipher_byte = new_plain_byte
    # therefore:
    # new_cipher_byte = old_cipher_byte ^ ord('t') ^ ord('s')

    ct[15] ^= ord('t') ^ ord('s')

    s.sendall(ct.hex().encode() + b"\n")

    result = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        result += chunk

    print(result.decode(errors="ignore"))
