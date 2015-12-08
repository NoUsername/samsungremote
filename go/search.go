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

type SearchOpts struct {
	SearchSeconds int
	DebugLog      bool
}

func defaults(opts *SearchOpts) {
	if opts.SearchSeconds == 0 {
		opts.SearchSeconds = 3
	}
}

func getSamsungIp() (string, error) {
	return getSamsungIpAdv(&SearchOpts{DebugLog: false})
}

func getSamsungIpAdv(opts *SearchOpts) (string, error) {
	defaults(opts)
	debugLog := opts.DebugLog
	devices, err := ssdp.Search("upnp:rootdevice", time.Duration(opts.SearchSeconds)*time.Second)
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
