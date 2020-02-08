// package: sid
// file: sid.proto

import * as jspb from "google-protobuf";
import * as google_protobuf_timestamp_pb from "google-protobuf/google/protobuf/timestamp_pb";

export class Token extends jspb.Message {
  getToken(): string;
  setToken(value: string): void;

  hasExpiresAt(): boolean;
  clearExpiresAt(): void;
  getExpiresAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setExpiresAt(value?: google_protobuf_timestamp_pb.Timestamp): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Token.AsObject;
  static toObject(includeInstance: boolean, msg: Token): Token.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Token, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Token;
  static deserializeBinaryFromReader(message: Token, reader: jspb.BinaryReader): Token;
}

export namespace Token {
  export type AsObject = {
    token: string,
    expiresAt?: google_protobuf_timestamp_pb.Timestamp.AsObject,
  }
}

export class LoginRequest extends jspb.Message {
  getIdentifier(): string;
  setIdentifier(value: string): void;

  getPassword(): string;
  setPassword(value: string): void;

  getNewPassword(): string;
  setNewPassword(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): LoginRequest.AsObject;
  static toObject(includeInstance: boolean, msg: LoginRequest): LoginRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: LoginRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): LoginRequest;
  static deserializeBinaryFromReader(message: LoginRequest, reader: jspb.BinaryReader): LoginRequest;
}

export namespace LoginRequest {
  export type AsObject = {
    identifier: string,
    password: string,
    newPassword: string,
  }
}

export class HealthStatus extends jspb.Message {
  getStatus(): HealthStatus.StatusMap[keyof HealthStatus.StatusMap];
  setStatus(value: HealthStatus.StatusMap[keyof HealthStatus.StatusMap]): void;

  hasStatusAt(): boolean;
  clearStatusAt(): void;
  getStatusAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setStatusAt(value?: google_protobuf_timestamp_pb.Timestamp): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): HealthStatus.AsObject;
  static toObject(includeInstance: boolean, msg: HealthStatus): HealthStatus.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: HealthStatus, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): HealthStatus;
  static deserializeBinaryFromReader(message: HealthStatus, reader: jspb.BinaryReader): HealthStatus;
}

export namespace HealthStatus {
  export type AsObject = {
    status: HealthStatus.StatusMap[keyof HealthStatus.StatusMap],
    statusAt?: google_protobuf_timestamp_pb.Timestamp.AsObject,
  }

  export interface StatusMap {
    INACTIVE: 0;
    READY: 1;
    WORKING: 2;
    LEAVING: 3;
  }

  export const Status: StatusMap;
}

export class Job extends jspb.Message {
  getRepoName(): string;
  setRepoName(value: string): void;

  getRepoSshUrl(): string;
  setRepoSshUrl(value: string): void;

  getCommitHexsha(): string;
  setCommitHexsha(value: string): void;

  getJobStatus(): Job.JobStatusMap[keyof Job.JobStatusMap];
  setJobStatus(value: Job.JobStatusMap[keyof Job.JobStatusMap]): void;

  hasStatusAt(): boolean;
  clearStatusAt(): void;
  getStatusAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setStatusAt(value?: google_protobuf_timestamp_pb.Timestamp): void;

  getJobUuid(): string;
  setJobUuid(value: string): void;

  getImageUrl(): string;
  setImageUrl(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Job.AsObject;
  static toObject(includeInstance: boolean, msg: Job): Job.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Job, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Job;
  static deserializeBinaryFromReader(message: Job, reader: jspb.BinaryReader): Job;
}

export namespace Job {
  export type AsObject = {
    repoName: string,
    repoSshUrl: string,
    commitHexsha: string,
    jobStatus: Job.JobStatusMap[keyof Job.JobStatusMap],
    statusAt?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    jobUuid: string,
    imageUrl: string,
  }

  export interface JobStatusMap {
    QUEUED: 0;
    BUILDING: 1;
    ABANDONED: 2;
    COMPLETED: 3;
    FAILED: 5;
  }

  export const JobStatus: JobStatusMap;
}

export class JobRunEvent extends jspb.Message {
  getType(): JobRunEvent.EventTypeMap[keyof JobRunEvent.EventTypeMap];
  setType(value: JobRunEvent.EventTypeMap[keyof JobRunEvent.EventTypeMap]): void;

  getContent(): string;
  setContent(value: string): void;

  hasEventAt(): boolean;
  clearEventAt(): void;
  getEventAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setEventAt(value?: google_protobuf_timestamp_pb.Timestamp): void;

  hasJob(): boolean;
  clearJob(): void;
  getJob(): Job | undefined;
  setJob(value?: Job): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): JobRunEvent.AsObject;
  static toObject(includeInstance: boolean, msg: JobRunEvent): JobRunEvent.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: JobRunEvent, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): JobRunEvent;
  static deserializeBinaryFromReader(message: JobRunEvent, reader: jspb.BinaryReader): JobRunEvent;
}

export namespace JobRunEvent {
  export type AsObject = {
    type: JobRunEvent.EventTypeMap[keyof JobRunEvent.EventTypeMap],
    content: string,
    eventAt?: google_protobuf_timestamp_pb.Timestamp.AsObject,
    job?: Job.AsObject,
  }

  export interface EventTypeMap {
    RUN_LOG: 0;
    ERROR: 1;
  }

  export const EventType: EventTypeMap;
}

export class CheckInResponse extends jspb.Message {
  getResponse(): string;
  setResponse(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CheckInResponse.AsObject;
  static toObject(includeInstance: boolean, msg: CheckInResponse): CheckInResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: CheckInResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CheckInResponse;
  static deserializeBinaryFromReader(message: CheckInResponse, reader: jspb.BinaryReader): CheckInResponse;
}

export namespace CheckInResponse {
  export type AsObject = {
    response: string,
  }
}

export class Repo extends jspb.Message {
  getName(): string;
  setName(value: string): void;

  getSshUrl(): string;
  setSshUrl(value: string): void;

  getEnabled(): boolean;
  setEnabled(value: boolean): void;

  getAddedBy(): number;
  setAddedBy(value: number): void;

  hasAddedAt(): boolean;
  clearAddedAt(): void;
  getAddedAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setAddedAt(value?: google_protobuf_timestamp_pb.Timestamp): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Repo.AsObject;
  static toObject(includeInstance: boolean, msg: Repo): Repo.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: Repo, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Repo;
  static deserializeBinaryFromReader(message: Repo, reader: jspb.BinaryReader): Repo;
}

export namespace Repo {
  export type AsObject = {
    name: string,
    sshUrl: string,
    enabled: boolean,
    addedBy: number,
    addedAt?: google_protobuf_timestamp_pb.Timestamp.AsObject,
  }
}

