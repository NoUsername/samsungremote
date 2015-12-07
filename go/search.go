package main

import (
	"errors"
	"fmt"
	"github.com/bcurren/go-ssdp"
	"log"
	"net"
	"strings"
	"time"
)

var debugLog bool = false

func getSamsungIp() (string, error) {
	devices, err := ssdp.Search("upnp:rootdevice", 5*time.Second)
	if err != nil {
		return "", errors.New("could not run upnp search")
	}

	var tvIp *string
	for _, result := range devices {
		if debugLog {
			log.Printf("searchresult: %+v\n", result)
		}
		if strings.Contains(strings.ToLower(result.Location.Path), "remotecontrolreceiver") {
			if debugLog {
				log.Printf("\nmatched query!\n", result)
			}
			theIp, _, _ := net.SplitHostPort(result.Location.Host)
			tvIp = &theIp
		}
	}
	if tvIp != nil {
		if debugLog {
			fmt.Printf("found samsung tv @ %v\n", *tvIp)
		}
		return *tvIp, nil
	} else {
		return "", errors.New("could not find samsung tv")
	}
}
