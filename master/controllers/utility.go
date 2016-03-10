// utility
package controllers

import "github.com/astaxie/beego/context"

func FinishRequest(ctx *context.Context, status int, body string) {
	ctx.Output.SetStatus(status)
	ctx.Output.Body([]byte(body))
}
