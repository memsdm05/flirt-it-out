package main

import (
	"github.com/memsdm05/flirt-it-out/routes"
)

func main() {
	routes.InitRoutes().Run(":8080")
}
