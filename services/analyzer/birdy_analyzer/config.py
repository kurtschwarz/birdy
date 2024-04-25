class Config:
    verbose: bool
    kafka_enabled: bool
    kafka_brokers: list[str]

    grpc_enabled: bool
    grpc_port: int

    storage: str
    storage_s3_endpoint: str
    storage_s3_access_key: str
    storage_s3_secret_key: str
    storage_s3_bucket_unanalyzed: str
    storage_s3_bucket_analyzed: str

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
