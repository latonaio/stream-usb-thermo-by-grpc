from grpc.tools import protoc

protoc.main(
        (
            '',
            '-I.',
            '--python_out=../src/thermo-camera/',
            '--grpc_python_out=../src/thermo-camera/',
            './thermo.proto'
        )
)
