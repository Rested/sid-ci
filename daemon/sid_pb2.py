# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sid.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='sid.proto',
  package='sid',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\tsid.proto\x12\x03sid\x1a\x1fgoogle/protobuf/timestamp.proto\"F\n\x05Token\x12\r\n\x05token\x18\x01 \x01(\t\x12.\n\nexpires_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"J\n\x0cLoginRequest\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x14\n\x0cnew_password\x18\x03 \x01(\t\"\xa4\x01\n\x0cHealthStatus\x12(\n\x06status\x18\x01 \x01(\x0e\x32\x18.sid.HealthStatus.Status\x12-\n\tstatus_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\";\n\x06Status\x12\x0c\n\x08INACTIVE\x10\x00\x12\t\n\x05READY\x10\x01\x12\x0b\n\x07WORKING\x10\x02\x12\x0b\n\x07LEAVING\x10\x03\"\x92\x02\n\x03Job\x12\x11\n\trepo_name\x18\x01 \x01(\t\x12\x14\n\x0crepo_ssh_url\x18\x02 \x01(\t\x12\x15\n\rcommit_hexsha\x18\x03 \x01(\t\x12&\n\njob_status\x18\x04 \x01(\x0e\x32\x12.sid.Job.JobStatus\x12-\n\tstatus_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08job_uuid\x18\x06 \x01(\t\x12\x11\n\timage_url\x18\x07 \x01(\t\"O\n\tJobStatus\x12\n\n\x06QUEUED\x10\x00\x12\x0c\n\x08\x42UILDING\x10\x01\x12\r\n\tABANDONED\x10\x02\x12\r\n\tCOMPLETED\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x05\"\xb2\x01\n\x0bJobRunEvent\x12(\n\x04type\x18\x01 \x01(\x0e\x32\x1a.sid.JobRunEvent.EventType\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12,\n\x08\x65vent_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\x03job\x18\x04 \x01(\x0b\x32\x08.sid.Job\"#\n\tEventType\x12\x0b\n\x07RUN_LOG\x10\x00\x12\t\n\x05\x45RROR\x10\x01\"#\n\x0f\x43heckInResponse\x12\x10\n\x08response\x18\x01 \x01(\t\"v\n\x04Repo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07ssh_url\x18\x02 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x03 \x01(\x08\x12\x10\n\x08\x61\x64\x64\x65\x64_by\x18\x04 \x01(\x05\x12,\n\x08\x61\x64\x64\x65\x64_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\x88\x03\n\x03Sid\x12\'\n\x06GetJob\x12\x11.sid.HealthStatus\x1a\x08.sid.Job\"\x00\x12\x1e\n\x06\x41\x64\x64Job\x12\x08.sid.Job\x1a\x08.sid.Job\"\x00\x12!\n\x07\x41\x64\x64Repo\x12\t.sid.Repo\x1a\t.sid.Repo\"\x00\x12(\n\x05Login\x12\x11.sid.LoginRequest\x1a\n.sid.Token\"\x00\x12-\n\nChangePass\x12\x11.sid.LoginRequest\x1a\n.sid.Token\"\x00\x12$\n\x08GetRepos\x12\t.sid.Repo\x1a\t.sid.Repo\"\x00\x30\x01\x12\"\n\x07GetJobs\x12\t.sid.Repo\x1a\x08.sid.Job\"\x00\x30\x01\x12\x42\n\x13HealthStatusCheckIn\x12\x11.sid.HealthStatus\x1a\x14.sid.CheckInResponse\"\x00(\x01\x12.\n\x0cRecordJobRun\x12\x10.sid.JobRunEvent\x1a\x08.sid.Job\"\x00(\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_HEALTHSTATUS_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='sid.HealthStatus.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INACTIVE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='READY', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WORKING', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEAVING', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=305,
  serialized_end=364,
)
_sym_db.RegisterEnumDescriptor(_HEALTHSTATUS_STATUS)

_JOB_JOBSTATUS = _descriptor.EnumDescriptor(
  name='JobStatus',
  full_name='sid.Job.JobStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='QUEUED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUILDING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABANDONED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMPLETED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=4, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=562,
  serialized_end=641,
)
_sym_db.RegisterEnumDescriptor(_JOB_JOBSTATUS)

_JOBRUNEVENT_EVENTTYPE = _descriptor.EnumDescriptor(
  name='EventType',
  full_name='sid.JobRunEvent.EventType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RUN_LOG', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=787,
  serialized_end=822,
)
_sym_db.RegisterEnumDescriptor(_JOBRUNEVENT_EVENTTYPE)


_TOKEN = _descriptor.Descriptor(
  name='Token',
  full_name='sid.Token',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='sid.Token.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expires_at', full_name='sid.Token.expires_at', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=121,
)


_LOGINREQUEST = _descriptor.Descriptor(
  name='LoginRequest',
  full_name='sid.LoginRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='sid.LoginRequest.identifier', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='sid.LoginRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='new_password', full_name='sid.LoginRequest.new_password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=197,
)


_HEALTHSTATUS = _descriptor.Descriptor(
  name='HealthStatus',
  full_name='sid.HealthStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='sid.HealthStatus.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_at', full_name='sid.HealthStatus.status_at', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HEALTHSTATUS_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=200,
  serialized_end=364,
)


_JOB = _descriptor.Descriptor(
  name='Job',
  full_name='sid.Job',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='repo_name', full_name='sid.Job.repo_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='repo_ssh_url', full_name='sid.Job.repo_ssh_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='commit_hexsha', full_name='sid.Job.commit_hexsha', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_status', full_name='sid.Job.job_status', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_at', full_name='sid.Job.status_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_uuid', full_name='sid.Job.job_uuid', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_url', full_name='sid.Job.image_url', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOB_JOBSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=367,
  serialized_end=641,
)


_JOBRUNEVENT = _descriptor.Descriptor(
  name='JobRunEvent',
  full_name='sid.JobRunEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='sid.JobRunEvent.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='sid.JobRunEvent.content', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='event_at', full_name='sid.JobRunEvent.event_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job', full_name='sid.JobRunEvent.job', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOBRUNEVENT_EVENTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=644,
  serialized_end=822,
)


_CHECKINRESPONSE = _descriptor.Descriptor(
  name='CheckInResponse',
  full_name='sid.CheckInResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='sid.CheckInResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=824,
  serialized_end=859,
)


_REPO = _descriptor.Descriptor(
  name='Repo',
  full_name='sid.Repo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='sid.Repo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssh_url', full_name='sid.Repo.ssh_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='sid.Repo.enabled', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='added_by', full_name='sid.Repo.added_by', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='added_at', full_name='sid.Repo.added_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=861,
  serialized_end=979,
)

_TOKEN.fields_by_name['expires_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_HEALTHSTATUS.fields_by_name['status'].enum_type = _HEALTHSTATUS_STATUS
_HEALTHSTATUS.fields_by_name['status_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_HEALTHSTATUS_STATUS.containing_type = _HEALTHSTATUS
_JOB.fields_by_name['job_status'].enum_type = _JOB_JOBSTATUS
_JOB.fields_by_name['status_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOB_JOBSTATUS.containing_type = _JOB
_JOBRUNEVENT.fields_by_name['type'].enum_type = _JOBRUNEVENT_EVENTTYPE
_JOBRUNEVENT.fields_by_name['event_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOBRUNEVENT.fields_by_name['job'].message_type = _JOB
_JOBRUNEVENT_EVENTTYPE.containing_type = _JOBRUNEVENT
_REPO.fields_by_name['added_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Token'] = _TOKEN
DESCRIPTOR.message_types_by_name['LoginRequest'] = _LOGINREQUEST
DESCRIPTOR.message_types_by_name['HealthStatus'] = _HEALTHSTATUS
DESCRIPTOR.message_types_by_name['Job'] = _JOB
DESCRIPTOR.message_types_by_name['JobRunEvent'] = _JOBRUNEVENT
DESCRIPTOR.message_types_by_name['CheckInResponse'] = _CHECKINRESPONSE
DESCRIPTOR.message_types_by_name['Repo'] = _REPO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Token = _reflection.GeneratedProtocolMessageType('Token', (_message.Message,), {
  'DESCRIPTOR' : _TOKEN,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.Token)
  })
_sym_db.RegisterMessage(Token)

LoginRequest = _reflection.GeneratedProtocolMessageType('LoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.LoginRequest)
  })
_sym_db.RegisterMessage(LoginRequest)

HealthStatus = _reflection.GeneratedProtocolMessageType('HealthStatus', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHSTATUS,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.HealthStatus)
  })
_sym_db.RegisterMessage(HealthStatus)

Job = _reflection.GeneratedProtocolMessageType('Job', (_message.Message,), {
  'DESCRIPTOR' : _JOB,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.Job)
  })
_sym_db.RegisterMessage(Job)

JobRunEvent = _reflection.GeneratedProtocolMessageType('JobRunEvent', (_message.Message,), {
  'DESCRIPTOR' : _JOBRUNEVENT,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.JobRunEvent)
  })
_sym_db.RegisterMessage(JobRunEvent)

CheckInResponse = _reflection.GeneratedProtocolMessageType('CheckInResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHECKINRESPONSE,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.CheckInResponse)
  })
_sym_db.RegisterMessage(CheckInResponse)

Repo = _reflection.GeneratedProtocolMessageType('Repo', (_message.Message,), {
  'DESCRIPTOR' : _REPO,
  '__module__' : 'sid_pb2'
  # @@protoc_insertion_point(class_scope:sid.Repo)
  })
_sym_db.RegisterMessage(Repo)



_SID = _descriptor.ServiceDescriptor(
  name='Sid',
  full_name='sid.Sid',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=982,
  serialized_end=1374,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetJob',
    full_name='sid.Sid.GetJob',
    index=0,
    containing_service=None,
    input_type=_HEALTHSTATUS,
    output_type=_JOB,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddJob',
    full_name='sid.Sid.AddJob',
    index=1,
    containing_service=None,
    input_type=_JOB,
    output_type=_JOB,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddRepo',
    full_name='sid.Sid.AddRepo',
    index=2,
    containing_service=None,
    input_type=_REPO,
    output_type=_REPO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Login',
    full_name='sid.Sid.Login',
    index=3,
    containing_service=None,
    input_type=_LOGINREQUEST,
    output_type=_TOKEN,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ChangePass',
    full_name='sid.Sid.ChangePass',
    index=4,
    containing_service=None,
    input_type=_LOGINREQUEST,
    output_type=_TOKEN,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetRepos',
    full_name='sid.Sid.GetRepos',
    index=5,
    containing_service=None,
    input_type=_REPO,
    output_type=_REPO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetJobs',
    full_name='sid.Sid.GetJobs',
    index=6,
    containing_service=None,
    input_type=_REPO,
    output_type=_JOB,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='HealthStatusCheckIn',
    full_name='sid.Sid.HealthStatusCheckIn',
    index=7,
    containing_service=None,
    input_type=_HEALTHSTATUS,
    output_type=_CHECKINRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RecordJobRun',
    full_name='sid.Sid.RecordJobRun',
    index=8,
    containing_service=None,
    input_type=_JOBRUNEVENT,
    output_type=_JOB,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SID)

DESCRIPTOR.services_by_name['Sid'] = _SID

# @@protoc_insertion_point(module_scope)
