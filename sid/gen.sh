#!/usr/bin/env bash
echo "Generating go server output"
protoc ./sid.proto --go_out=plugins=grpc:../server/pkg/gen
echo "Generating python daemon output"
python -m grpc_tools.protoc --proto_path=./ --python_out=../daemon --grpc_python_out=../daemon sid.proto