# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: collector/v1/service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x63ollector/v1/service.proto\x12\x0c\x63ollector.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"@\n\x08Recorder\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x10\n\x03lat\x18\x02 \x01(\tR\x03lat\x12\x12\n\x04long\x18\x03 \x01(\tR\x04long\"\xa3\x01\n\tRecording\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x38\n\tstartTime\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x34\n\x07\x65ndTime\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\x16\n\x06\x62uffer\x18\x04 \x01(\x0cR\x06\x62uffer\"{\n\x0e\x43ollectRequest\x12\x32\n\x08recorder\x18\x01 \x01(\x0b\x32\x16.collector.v1.RecorderR\x08recorder\x12\x35\n\trecording\x18\x02 \x01(\x0b\x32\x17.collector.v1.RecordingR\trecording\"!\n\x0f\x43ollectResponse\x12\x0e\n\x02ok\x18\x01 \x01(\x08R\x02ok2^\n\x10\x43ollectorService\x12J\n\x07\x43ollect\x12\x1c.collector.v1.CollectRequest\x1a\x1d.collector.v1.CollectResponse\"\x00(\x01\x42q\n\x10\x63om.collector.v1B\x0cServiceProtoP\x01\xa2\x02\x03\x43XX\xaa\x02\x0c\x43ollector.V1\xca\x02\x0c\x43ollector\\V1\xe2\x02\x18\x43ollector\\V1\\GPBMetadata\xea\x02\rCollector::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'collector.v1.service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\020com.collector.v1B\014ServiceProtoP\001\242\002\003CXX\252\002\014Collector.V1\312\002\014Collector\\V1\342\002\030Collector\\V1\\GPBMetadata\352\002\rCollector::V1'
  _globals['_RECORDER']._serialized_start=77
  _globals['_RECORDER']._serialized_end=141
  _globals['_RECORDING']._serialized_start=144
  _globals['_RECORDING']._serialized_end=307
  _globals['_COLLECTREQUEST']._serialized_start=309
  _globals['_COLLECTREQUEST']._serialized_end=432
  _globals['_COLLECTRESPONSE']._serialized_start=434
  _globals['_COLLECTRESPONSE']._serialized_end=467
  _globals['_COLLECTORSERVICE']._serialized_start=469
  _globals['_COLLECTORSERVICE']._serialized_end=563
# @@protoc_insertion_point(module_scope)
