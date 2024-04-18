// @generated by protoc-gen-connect-es v1.4.0 with parameter "target=ts"
// @generated from file analyzer/v1/service.proto (package analyzer.v1, syntax proto3)
/* eslint-disable */
// @ts-nocheck

import { AnalyzeRequest, AnalyzeResponse } from "./service_pb.js";
import { MethodKind } from "@bufbuild/protobuf";

/**
 * @generated from service analyzer.v1.AnalyzerService
 */
export const AnalyzerService = {
  typeName: "analyzer.v1.AnalyzerService",
  methods: {
    /**
     * @generated from rpc analyzer.v1.AnalyzerService.Analyze
     */
    analyze: {
      name: "Analyze",
      I: AnalyzeRequest,
      O: AnalyzeResponse,
      kind: MethodKind.Unary,
    },
  }
} as const;

