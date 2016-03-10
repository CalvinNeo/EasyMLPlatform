// object
package models

type ResultSet struct {
	Id int64 `orm:"auto;pk"`

	FilePath string

	// Meta data
	Meta string

	// Ext data
	Ext string
}
