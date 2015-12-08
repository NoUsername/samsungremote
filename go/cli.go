package main

import (
	"flag"
	"fmt"
)

func testSearch() {
	fmt.Println("searching tv ip...")
	ip, err := getSamsungIpAdv(&SearchOpts{DebugLog: true})
	if err != nil {
		panic(err)
	}
	fmt.Println(ip)
}

/**
* quick proof-of-concept. connects to auto-detected samsung tv on your network
* and changes volume up & down (you'll see the volume indicator show up)
* when running for the first time you'll get asked by the tv if you want to allow this connection
 */
func main() {
	ipCheck := flag.Bool("tvip", false, "only try to find TVs ip")
	localIp := flag.String("ip", "127.0.0.1", "local ip")

	flag.Parse()

	if *ipCheck {
		testSearch()
		return
	}

	ip, err := getSamsungIp()
	if err != nil {
		panic(err)
	}

	remote := connect(ip)
	fmt.Println(remote)
	remote.SourceIp = *localIp
	handshake(remote)

	sendKey(remote, "KEY_VOLUP")
	sendKey(remote, "KEY_VOLDOWN")

	close(remote)
}
