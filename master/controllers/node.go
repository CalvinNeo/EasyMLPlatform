// node
package controllers

import (
	"log"
	"mlp/master/node"
	"strconv"

	"github.com/astaxie/beego"
)

// Node Machine API Controller
type NodeController struct {
	beego.Controller
}

// @Title Acquire
// @Description Acquire id
// @Success 200 {string} node id
// @Failure 403 {string} error description
// @router /acquire [post]
func (o *NodeController) Acquire() {
	o.Ctx.WriteString(strconv.FormatInt(node.AcquireId(), 10))
}

// @Title Alive
// @Description Report node machine alive and flush machine status
// @Param	id			form 	int64		true	"The node machine id"
// @Param	cpu			form 	float32		true	"The node machine cpu used rate"
// @Param	memory		form 	float32		true	"The node machine memory used rate"
// @Success 200 body is empty
// @Failure 403 {string} error description
// @router /alive [post]
func (o *NodeController) Alive() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	cpu, err := o.GetFloat("cpu")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	memory, err := o.GetFloat("memory")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	node.UpdateNodeStatus(id, cpu, memory)
}

type NodeStatusList struct {
	Objects []node.NodeStatus
}

// @Title Query
// @Description Query node info
// @Param	id		form 	int64	true		"The node id"
// @Success 200 {object} node.NodeStatus
// @Failure 403 {string} error description
// @router /query [post]
func (o *NodeController) Query() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	d, err := node.QueryNodeStatus(id)
	if err != nil {
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	o.Data["json"] = d
	o.ServeJson()
}

// @Title Query List
// @Description Query all node info
// @Success 200 {object} controllers.NodeStatusList
// @router /query/list [post]
func (o *NodeController) QueryList() {
	ds := node.QueryNodeStatusList()

	o.Data["json"] = NodeStatusList{
		Objects: ds,
	}
	o.ServeJson()
}
