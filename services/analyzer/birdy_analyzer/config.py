class Config:
    verbose: bool
    kafka_enabled: bool
    kafka_brokers: list[str]

    grpc_enabled: bool
    grpc_port: int

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
