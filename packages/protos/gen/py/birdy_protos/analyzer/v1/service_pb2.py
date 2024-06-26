# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: analyzer/v1/service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x61nalyzer/v1/service.proto\x12\x0b\x61nalyzer.v1\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"f\n\x06Status\x12\x12\n\x04\x63ode\x18\x01 \x01(\x05R\x04\x63ode\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12.\n\x07\x64\x65tails\x18\x03 \x03(\x0b\x32\x14.google.protobuf.AnyR\x07\x64\x65tails\"T\n\x08Location\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1a\n\x08latitude\x18\x02 \x01(\x02R\x08latitude\x12\x1c\n\tlongitude\x18\x03 \x01(\x02R\tlongitude\"\xca\x01\n\tRecording\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1a\n\x08\x64uration\x18\x02 \x01(\x02R\x08\x64uration\x12\x39\n\nstart_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\x1f\n\x0bstorage_uri\x18\x05 \x01(\tR\nstorageUri\"\xc5\x01\n\tDetection\x12\x1d\n\nstart_time\x18\x01 \x01(\x02R\tstartTime\x12\x19\n\x08\x65nd_time\x18\x02 \x01(\x02R\x07\x65ndTime\x12\x1e\n\nconfidence\x18\x03 \x01(\x02R\nconfidence\x12\x1f\n\x0b\x63ommon_name\x18\x04 \x01(\tR\ncommonName\x12\'\n\x0fscientific_name\x18\x05 \x01(\tR\x0escientificName\x12\x14\n\x05label\x18\x06 \x01(\tR\x05label\"y\n\x0e\x41nalyzeRequest\x12\x34\n\trecording\x18\x01 \x01(\x0b\x32\x16.analyzer.v1.RecordingR\trecording\x12\x31\n\x08location\x18\x02 \x01(\x0b\x32\x15.analyzer.v1.LocationR\x08location\"v\n\x0f\x41nalyzeResponse\x12+\n\x06status\x18\x01 \x01(\x0b\x32\x13.analyzer.v1.StatusR\x06status\x12\x36\n\ndetections\x18\x02 \x03(\x0b\x32\x16.analyzer.v1.DetectionR\ndetections2Y\n\x0f\x41nalyzerService\x12\x46\n\x07\x41nalyze\x12\x1b.analyzer.v1.AnalyzeRequest\x1a\x1c.analyzer.v1.AnalyzeResponse\"\x00\x42l\n\x0f\x63om.analyzer.v1B\x0cServiceProtoP\x01\xa2\x02\x03\x41XX\xaa\x02\x0b\x41nalyzer.V1\xca\x02\x0b\x41nalyzer\\V1\xe2\x02\x17\x41nalyzer\\V1\\GPBMetadata\xea\x02\x0c\x41nalyzer::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'analyzer.v1.service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\017com.analyzer.v1B\014ServiceProtoP\001\242\002\003AXX\252\002\013Analyzer.V1\312\002\013Analyzer\\V1\342\002\027Analyzer\\V1\\GPBMetadata\352\002\014Analyzer::V1'
  _globals['_STATUS']._serialized_start=102
  _globals['_STATUS']._serialized_end=204
  _globals['_LOCATION']._serialized_start=206
  _globals['_LOCATION']._serialized_end=290
  _globals['_RECORDING']._serialized_start=293
  _globals['_RECORDING']._serialized_end=495
  _globals['_DETECTION']._serialized_start=498
  _globals['_DETECTION']._serialized_end=695
  _globals['_ANALYZEREQUEST']._serialized_start=697
  _globals['_ANALYZEREQUEST']._serialized_end=818
  _globals['_ANALYZERESPONSE']._serialized_start=820
  _globals['_ANALYZERESPONSE']._serialized_end=938
  _globals['_ANALYZERSERVICE']._serialized_start=940
  _globals['_ANALYZERSERVICE']._serialized_end=1029
# @@protoc_insertion_point(module_scope)
