// @generated by protoc-gen-es v1.8.0 with parameter "target=ts"
// @generated from file analyzer/v1/service.proto (package analyzer.v1, syntax proto3)
/* eslint-disable */
// @ts-nocheck

import type { BinaryReadOptions, FieldList, JsonReadOptions, JsonValue, PartialMessage, PlainMessage } from "@bufbuild/protobuf";
import { Any, Message, proto3 } from "@bufbuild/protobuf";

/**
 * @generated from message analyzer.v1.Status
 */
export class Status extends Message<Status> {
  /**
   * @generated from field: int32 code = 1;
   */
  code = 0;

  /**
   * @generated from field: string message = 2;
   */
  message = "";

  /**
   * @generated from field: repeated google.protobuf.Any details = 3;
   */
  details: Any[] = [];

  constructor(data?: PartialMessage<Status>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.Status";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "code", kind: "scalar", T: 5 /* ScalarType.INT32 */ },
    { no: 2, name: "message", kind: "scalar", T: 9 /* ScalarType.STRING */ },
    { no: 3, name: "details", kind: "message", T: Any, repeated: true },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): Status {
    return new Status().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): Status {
    return new Status().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): Status {
    return new Status().fromJsonString(jsonString, options);
  }

  static equals(a: Status | PlainMessage<Status> | undefined, b: Status | PlainMessage<Status> | undefined): boolean {
    return proto3.util.equals(Status, a, b);
  }
}

/**
 * @generated from message analyzer.v1.Location
 */
export class Location extends Message<Location> {
  /**
   * @generated from field: string id = 1;
   */
  id = "";

  /**
   * @generated from field: string latitude = 2;
   */
  latitude = "";

  /**
   * @generated from field: string longitude = 3;
   */
  longitude = "";

  constructor(data?: PartialMessage<Location>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.Location";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "id", kind: "scalar", T: 9 /* ScalarType.STRING */ },
    { no: 2, name: "latitude", kind: "scalar", T: 9 /* ScalarType.STRING */ },
    { no: 3, name: "longitude", kind: "scalar", T: 9 /* ScalarType.STRING */ },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): Location {
    return new Location().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): Location {
    return new Location().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): Location {
    return new Location().fromJsonString(jsonString, options);
  }

  static equals(a: Location | PlainMessage<Location> | undefined, b: Location | PlainMessage<Location> | undefined): boolean {
    return proto3.util.equals(Location, a, b);
  }
}

/**
 * @generated from message analyzer.v1.Recording
 */
export class Recording extends Message<Recording> {
  /**
   * @generated from field: string id = 1;
   */
  id = "";

  constructor(data?: PartialMessage<Recording>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.Recording";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "id", kind: "scalar", T: 9 /* ScalarType.STRING */ },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): Recording {
    return new Recording().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): Recording {
    return new Recording().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): Recording {
    return new Recording().fromJsonString(jsonString, options);
  }

  static equals(a: Recording | PlainMessage<Recording> | undefined, b: Recording | PlainMessage<Recording> | undefined): boolean {
    return proto3.util.equals(Recording, a, b);
  }
}

/**
 * @generated from message analyzer.v1.Detection
 */
export class Detection extends Message<Detection> {
  /**
   * @generated from field: float start_time = 1;
   */
  startTime = 0;

  /**
   * @generated from field: float end_time = 2;
   */
  endTime = 0;

  /**
   * @generated from field: float confidence = 3;
   */
  confidence = 0;

  /**
   * @generated from field: string common_name = 4;
   */
  commonName = "";

  /**
   * @generated from field: string scientific_name = 5;
   */
  scientificName = "";

  /**
   * @generated from field: string label = 6;
   */
  label = "";

  constructor(data?: PartialMessage<Detection>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.Detection";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "start_time", kind: "scalar", T: 2 /* ScalarType.FLOAT */ },
    { no: 2, name: "end_time", kind: "scalar", T: 2 /* ScalarType.FLOAT */ },
    { no: 3, name: "confidence", kind: "scalar", T: 2 /* ScalarType.FLOAT */ },
    { no: 4, name: "common_name", kind: "scalar", T: 9 /* ScalarType.STRING */ },
    { no: 5, name: "scientific_name", kind: "scalar", T: 9 /* ScalarType.STRING */ },
    { no: 6, name: "label", kind: "scalar", T: 9 /* ScalarType.STRING */ },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): Detection {
    return new Detection().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): Detection {
    return new Detection().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): Detection {
    return new Detection().fromJsonString(jsonString, options);
  }

  static equals(a: Detection | PlainMessage<Detection> | undefined, b: Detection | PlainMessage<Detection> | undefined): boolean {
    return proto3.util.equals(Detection, a, b);
  }
}

/**
 * @generated from message analyzer.v1.AnalyzeRequest
 */
export class AnalyzeRequest extends Message<AnalyzeRequest> {
  /**
   * @generated from field: analyzer.v1.Recording recording = 1;
   */
  recording?: Recording;

  /**
   * @generated from field: analyzer.v1.Location location = 2;
   */
  location?: Location;

  constructor(data?: PartialMessage<AnalyzeRequest>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.AnalyzeRequest";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "recording", kind: "message", T: Recording },
    { no: 2, name: "location", kind: "message", T: Location },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): AnalyzeRequest {
    return new AnalyzeRequest().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): AnalyzeRequest {
    return new AnalyzeRequest().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): AnalyzeRequest {
    return new AnalyzeRequest().fromJsonString(jsonString, options);
  }

  static equals(a: AnalyzeRequest | PlainMessage<AnalyzeRequest> | undefined, b: AnalyzeRequest | PlainMessage<AnalyzeRequest> | undefined): boolean {
    return proto3.util.equals(AnalyzeRequest, a, b);
  }
}

/**
 * @generated from message analyzer.v1.AnalyzeResponse
 */
export class AnalyzeResponse extends Message<AnalyzeResponse> {
  /**
   * @generated from field: analyzer.v1.Status status = 1;
   */
  status?: Status;

  /**
   * @generated from field: repeated analyzer.v1.Detection detections = 2;
   */
  detections: Detection[] = [];

  constructor(data?: PartialMessage<AnalyzeResponse>) {
    super();
    proto3.util.initPartial(data, this);
  }

  static readonly runtime: typeof proto3 = proto3;
  static readonly typeName = "analyzer.v1.AnalyzeResponse";
  static readonly fields: FieldList = proto3.util.newFieldList(() => [
    { no: 1, name: "status", kind: "message", T: Status },
    { no: 2, name: "detections", kind: "message", T: Detection, repeated: true },
  ]);

  static fromBinary(bytes: Uint8Array, options?: Partial<BinaryReadOptions>): AnalyzeResponse {
    return new AnalyzeResponse().fromBinary(bytes, options);
  }

  static fromJson(jsonValue: JsonValue, options?: Partial<JsonReadOptions>): AnalyzeResponse {
    return new AnalyzeResponse().fromJson(jsonValue, options);
  }

  static fromJsonString(jsonString: string, options?: Partial<JsonReadOptions>): AnalyzeResponse {
    return new AnalyzeResponse().fromJsonString(jsonString, options);
  }

  static equals(a: AnalyzeResponse | PlainMessage<AnalyzeResponse> | undefined, b: AnalyzeResponse | PlainMessage<AnalyzeResponse> | undefined): boolean {
    return proto3.util.equals(AnalyzeResponse, a, b);
  }
}

