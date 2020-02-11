#!/usr/bin/env bash
echo "Generating go server output"
protoc ./sid.proto --go_out=plugins=grpc:../server/pkg/gen
echo "Generating python daemon output"
python -m grpc_tools.protoc --proto_path=./ --python_out=../daemon \
      --grpc_python_out=../daemon sid.proto
echo "Generating typescript ui output"
protoc --plugin="protoc-gen-ts=$(npm root -g)/ts-protoc-gen/bin/protoc-gen-ts" \
    --js_out="import_style=commonjs,binary:../ui/src/proto" \
    --ts_out=service=grpc-web:"../ui/src/proto" sid.proto