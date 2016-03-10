// id
package node

import "sync/atomic"

var (
	nextId int64 = 1
)

func AcquireId() int64 {
	return atomic.AddInt64(&nextId, 1) - 1
}
