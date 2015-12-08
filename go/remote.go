package main

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"net"
)

var appstring = "linux.iapp.samsung"

// Might need changing to match your TV type
var tvappstring = "iphone.UE55C8000.iapp.samsung"

//What gets reported when it asks for permission
var remotename = "Go Samsung Remote"

type Remote struct {
	Connection net.Conn
	SourceIp   string
	TargetIp   string
	SourceMac  string
}

func connect(ip string) Remote {
	conn, err := net.Dial("tcp", ip+":55000")
	if err != nil {
		// handle error
	}
	return Remote{Connection: conn, SourceMac: "11-11-11-11-11-12"}
}

func encode(val string) []byte {
	return []byte(base64.URLEncoding.EncodeToString([]byte(val)))
}

func sendKey(remote Remote, key string) {
	keyEnc := encode(key)

	partBuf := new(bytes.Buffer)
	partBuf.WriteByte(0)
	partBuf.WriteByte(0)
	partBuf.WriteByte(0)
	partBuf.WriteByte(byte(len(keyEnc)))
	partBuf.WriteByte(0)
	partBuf.Write(keyEnc)

	remote.Connection.Write(createMessage(partBuf))
}

func handshake(remote Remote) {
	sourceIpEnc := encode(remote.SourceIp)
	sourceMacEnc := encode(remote.SourceMac)
	remoteNameEnc := encode(remotename)

	partBuf := new(bytes.Buffer)
	partBuf.WriteByte(0x64)
	partBuf.WriteByte(0x00)
	partBuf.WriteByte(byte(len(sourceIpEnc)))
	partBuf.WriteByte(0x00)
	partBuf.Write(sourceIpEnc)
	partBuf.WriteByte(byte(len(sourceMacEnc)))
	partBuf.WriteByte(0x00)
	partBuf.Write(sourceMacEnc)
	partBuf.WriteByte(byte(len(remoteNameEnc)))
	partBuf.WriteByte(0x00)
	partBuf.Write(remoteNameEnc)

	remote.Connection.Write(createMessage(partBuf))

	partBuf = new(bytes.Buffer)
	partBuf.WriteByte(0xc8)
	partBuf.WriteByte(0x00)

	remote.Connection.Write(createMessage(partBuf))
}

func createMessage(buffer *bytes.Buffer) []byte {
	msgBuf := new(bytes.Buffer)
	msgBuf.WriteByte(0)
	msgBuf.WriteByte(byte(len(appstring)))
	msgBuf.WriteByte(0)
	msgBuf.Write([]byte(appstring))

	fmt.Println("writing bytes: ", buffer.Len())
	msgBuf.WriteByte(byte(buffer.Len()))
	msgBuf.WriteByte(0)
	msgBuf.Write(buffer.Bytes())

	return msgBuf.Bytes()
}

func close(remote Remote) {
	remote.Connection.Close()
}
