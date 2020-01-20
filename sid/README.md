# Proto 

## Installation

See https://github.com/protocolbuffers/protobuf/blob/master/src/README.md

Get go protoc generator
```bash
go get -u github.com/golang/protobuf/protoc-gen-go
```

## Update

```bash
 protoc ./sid.proto --go_out=plugins=grpc:../sid
 ```