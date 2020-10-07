import socket
import pickle
import time
import struct
import logging
import argparse
from multiprocessing import Process

import numpy as np
from tqdm import tqdm


logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def query(socket_file, epoch, data):
    while True:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(socket_file)

                t0 = time.time()
                for _ in tqdm(range(epoch)):
                    msg = pickle.dumps(data)
                    logger.debug('client sending {!r}'.format(msg))
                    logger.debug('msg length: {}'.format(len(msg)))
                    sock.sendall(struct.pack('!i', len(msg)))
                    sock.sendall(msg)

                    length_bytes = sock.recv(4)
                    length = struct.unpack('!i', length_bytes)[0]
                    logger.debug('expect length: {}'.format(length))
                    recv = recvall(sock, length)
                    logger.debug('recv length: {}'.format(len(recv)))
                    _ = pickle.loads(recv)

                logger.info('Time: {}'.format(time.time() - t0))
                logger.info('close client socket')
                break
        except BrokenPipeError:
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', default='./uds.socket', required=False)
    parser.add_argument('--epoch', default=1000, type=int, required=False)
    parser.add_argument('--process', default=1, type=int, required=False)
    args = parser.parse_args()
    logger.info(args)

    matrix = (np.random.random((800, 800, 3)) * 256).astype(np.uint8)
    logger.info('matrix shape: {}, type: {}'.format(matrix.shape, matrix.dtype))

    if args.process == 1:
        query(args.addr, args.epoch, matrix)
    else:
        processes = [Process(target=query, args=(args.addr, args.epoch, matrix), daemon=True) for _ in range(args.process)]
        for p in processes:
            p.start()

        for p in processes:
            p.join()
