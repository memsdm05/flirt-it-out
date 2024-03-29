package routes

import (
	"fmt"

	"github.com/gin-gonic/gin"
	"github.com/memsdm05/flirt-it-out/game"
)

// GET /rooms
func createRoom(ctx *gin.Context) {
	room := game.NewRoom()
	ctx.JSON(200, room)
}

// GET /rooms/:code
func getRoom(ctx *gin.Context) {
	code := ctx.Param("code")
	room, ok := game.Rooms[code]
	if ok {
		ctx.JSON(200, room)
	} else {
		ctx.JSON(404, gin.H{
			"error": fmt.Sprintf("The room with code %s does not exist", code),
		})
	}
}

// DELETE /rooms/:code
func closeRoom(ctx *gin.Context) {
	code := ctx.Param("code")
	// TODO make sure to shutdown server
	delete(game.Rooms, code)
}

func InitRoutes() *gin.Engine {
	router := gin.Default()

	api := router.Group("/api")
	{
		api.GET("/rooms", createRoom)
		api.GET("/rooms/:code", getRoom)
		api.DELETE("/rooms/:code", closeRoom)
	}

	initHostRoutes(api)
	initClientRoutes(api)

	return router
}
