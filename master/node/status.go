// status
package node

import (
	"errors"
	"sync"
)

type NodeStatus struct {
	Id     int64
	Cpu    float64
	Memory float64
}

var (
	ErrNodeNotFound error = errors.New("node not found")

	lock sync.Mutex

	nodeMap map[int64]NodeStatus
)

func init() {
	nodeMap = map[int64]NodeStatus{}
}

func UpdateNodeStatus(id int64, cpu, memory float64) {
	lock.Lock()
	defer lock.Unlock()

	nodeMap[id] = NodeStatus{
		Id:     id,
		Cpu:    cpu,
		Memory: memory,
	}
}

func QueryNodeStatus(id int64) (*NodeStatus, error) {
	lock.Lock()
	defer lock.Unlock()

	s, ok := nodeMap[id]
	if !ok {
		return nil, ErrNodeNotFound
	}
	return &s, nil
}

func QueryNodeStatusList() []NodeStatus {
	lock.Lock()
	defer lock.Unlock()

	ns := []NodeStatus{}
	for _, v := range nodeMap {
		ns = append(ns, v)
	}
	return ns
}
