// package: sid
// file: sid.proto

import * as sid_pb from "./sid_pb";
import {grpc} from "@improbable-eng/grpc-web";

type SidGetJob = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.HealthStatus;
  readonly responseType: typeof sid_pb.Job;
};

type SidAddJob = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.Job;
  readonly responseType: typeof sid_pb.Job;
};

type SidLogin = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.LoginRequest;
  readonly responseType: typeof sid_pb.Token;
};

type SidChangePass = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.LoginRequest;
  readonly responseType: typeof sid_pb.Token;
};

type SidGetRepos = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: false;
  readonly responseStream: true;
  readonly requestType: typeof sid_pb.Repo;
  readonly responseType: typeof sid_pb.Repo;
};

type SidHealthStatusCheckIn = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: true;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.HealthStatus;
  readonly responseType: typeof sid_pb.CheckInResponse;
};

type SidRecordJobRun = {
  readonly methodName: string;
  readonly service: typeof Sid;
  readonly requestStream: true;
  readonly responseStream: false;
  readonly requestType: typeof sid_pb.JobRunEvent;
  readonly responseType: typeof sid_pb.Job;
};

export class Sid {
  static readonly serviceName: string;
  static readonly GetJob: SidGetJob;
  static readonly AddJob: SidAddJob;
  static readonly Login: SidLogin;
  static readonly ChangePass: SidChangePass;
  static readonly GetRepos: SidGetRepos;
  static readonly HealthStatusCheckIn: SidHealthStatusCheckIn;
  static readonly RecordJobRun: SidRecordJobRun;
}

export type ServiceError = { message: string, code: number; metadata: grpc.Metadata }
export type Status = { details: string, code: number; metadata: grpc.Metadata }

interface UnaryResponse {
  cancel(): void;
}
interface ResponseStream<T> {
  cancel(): void;
  on(type: 'data', handler: (message: T) => void): ResponseStream<T>;
  on(type: 'end', handler: (status?: Status) => void): ResponseStream<T>;
  on(type: 'status', handler: (status: Status) => void): ResponseStream<T>;
}
interface RequestStream<T> {
  write(message: T): RequestStream<T>;
  end(): void;
  cancel(): void;
  on(type: 'end', handler: (status?: Status) => void): RequestStream<T>;
  on(type: 'status', handler: (status: Status) => void): RequestStream<T>;
}
interface BidirectionalStream<ReqT, ResT> {
  write(message: ReqT): BidirectionalStream<ReqT, ResT>;
  end(): void;
  cancel(): void;
  on(type: 'data', handler: (message: ResT) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'end', handler: (status?: Status) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'status', handler: (status: Status) => void): BidirectionalStream<ReqT, ResT>;
}

export class SidClient {
  readonly serviceHost: string;

  constructor(serviceHost: string, options?: grpc.RpcOptions);
  getJob(
    requestMessage: sid_pb.HealthStatus,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Job|null) => void
  ): UnaryResponse;
  getJob(
    requestMessage: sid_pb.HealthStatus,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Job|null) => void
  ): UnaryResponse;
  addJob(
    requestMessage: sid_pb.Job,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Job|null) => void
  ): UnaryResponse;
  addJob(
    requestMessage: sid_pb.Job,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Job|null) => void
  ): UnaryResponse;
  login(
    requestMessage: sid_pb.LoginRequest,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Token|null) => void
  ): UnaryResponse;
  login(
    requestMessage: sid_pb.LoginRequest,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Token|null) => void
  ): UnaryResponse;
  changePass(
    requestMessage: sid_pb.LoginRequest,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Token|null) => void
  ): UnaryResponse;
  changePass(
    requestMessage: sid_pb.LoginRequest,
    callback: (error: ServiceError|null, responseMessage: sid_pb.Token|null) => void
  ): UnaryResponse;
  getRepos(requestMessage: sid_pb.Repo, metadata?: grpc.Metadata): ResponseStream<sid_pb.Repo>;
  healthStatusCheckIn(metadata?: grpc.Metadata): RequestStream<sid_pb.HealthStatus>;
  recordJobRun(metadata?: grpc.Metadata): RequestStream<sid_pb.JobRunEvent>;
}

