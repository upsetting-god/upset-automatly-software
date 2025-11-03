package main

import (
	"fmt"
	"net/http"
	"sync"
)

func main() {
	fmt.Println("Enter link on website: ")
	var url string
	fmt.Scanln(&url)
	fmt.Println("How many requests?: ")
	var res int
	fmt.Scanln(&res)
	wg := sync.WaitGroup{}
	for i := range res {
		wg.Add(1)
		go func() {
			checkurl(i, url)
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println("OK")
}

func checkurl(i int, url string) {
	fmt.Println("will send", i, "request")
	_, err := http.Get(url)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}
	fmt.Println("request", i, "success")
}
