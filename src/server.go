package main

import (
	"encoding/binary"
	"io"
	"log"
	"net"
	"os"
)

const sockAddr = "./uds.socket"

func main() {
	if _, err := os.Stat(sockAddr); err == nil {
		if err := os.Remove(sockAddr); err != nil {
			log.Printf("Remove socket file error: %v", err)
		}
	}

	sock, err := net.Listen("unix", sockAddr)
	if err != nil {
		log.Fatal("Listen error: ", err)
	}
	defer sock.Close()

	for {
		conn, err := sock.Accept()
		if err != nil {
			log.Fatal("Accept error: ", err)
		}
		log.Println("connection accepted.")

		go func(conn net.Conn) {
			lengthBuf := make([]byte, 4)
			for {
				len, err := io.ReadFull(conn, lengthBuf)
				if err != nil || len != 4 {
					if err == io.EOF {
						log.Println("end of file")
						break
					}
					log.Fatal("read length buffer error", err, len)
				}
				length := binary.BigEndian.Uint32(lengthBuf)
				// log.Println("length:", length)
				dataBuf := make([]byte, length)
				len, err = io.ReadFull(conn, dataBuf)
				if err != nil || len != int(length) {
					log.Fatal("read data buffer error", err, len, length)
				}

				_, err = conn.Write(lengthBuf)
				if err != nil {
					log.Fatal("Send to client error: ", err)
				}
				_, err = conn.Write(dataBuf)
				if err != nil {
					log.Fatal("Send to client error: ", err)
				}
			}
		}(conn)
	}
}
