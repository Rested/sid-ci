# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import sid_pb2 as sid__pb2


class SidStub(object):
  """Interface exported by the server.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetJob = channel.unary_unary(
        '/sid.Sid/GetJob',
        request_serializer=sid__pb2.HealthStatus.SerializeToString,
        response_deserializer=sid__pb2.Job.FromString,
        )
    self.AddJob = channel.unary_unary(
        '/sid.Sid/AddJob',
        request_serializer=sid__pb2.Job.SerializeToString,
        response_deserializer=sid__pb2.Job.FromString,
        )
    self.AddRepo = channel.unary_unary(
        '/sid.Sid/AddRepo',
        request_serializer=sid__pb2.Repo.SerializeToString,
        response_deserializer=sid__pb2.Repo.FromString,
        )
    self.Login = channel.unary_unary(
        '/sid.Sid/Login',
        request_serializer=sid__pb2.LoginRequest.SerializeToString,
        response_deserializer=sid__pb2.Token.FromString,
        )
    self.ChangePass = channel.unary_unary(
        '/sid.Sid/ChangePass',
        request_serializer=sid__pb2.LoginRequest.SerializeToString,
        response_deserializer=sid__pb2.Token.FromString,
        )
    self.GetRepos = channel.unary_stream(
        '/sid.Sid/GetRepos',
        request_serializer=sid__pb2.Repo.SerializeToString,
        response_deserializer=sid__pb2.Repo.FromString,
        )
    self.GetJobs = channel.unary_stream(
        '/sid.Sid/GetJobs',
        request_serializer=sid__pb2.Repo.SerializeToString,
        response_deserializer=sid__pb2.Job.FromString,
        )
    self.HealthStatusCheckIn = channel.stream_unary(
        '/sid.Sid/HealthStatusCheckIn',
        request_serializer=sid__pb2.HealthStatus.SerializeToString,
        response_deserializer=sid__pb2.CheckInResponse.FromString,
        )
    self.RecordJobRun = channel.stream_unary(
        '/sid.Sid/RecordJobRun',
        request_serializer=sid__pb2.JobRunEvent.SerializeToString,
        response_deserializer=sid__pb2.Job.FromString,
        )


class SidServicer(object):
  """Interface exported by the server.
  """

  def GetJob(self, request, context):
    """Obtains a job from the queue
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddJob(self, request, context):
    """Adds a job to the queue
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddRepo(self, request, context):
    """Add a repo
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Login(self, request, context):
    """Log in
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ChangePass(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetRepos(self, request, context):
    """server to client stream of repos matching repo filter
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetJobs(self, request, context):
    """server to client stream of jobs for a repo
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def HealthStatusCheckIn(self, request_iterator, context):
    """A client-to-server streaming RPC.

    Streams health status of the client as it changes.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RecordJobRun(self, request_iterator, context):
    """A client-to-server streaming RPC.

    Accepts a stream of JobRunEvents on a job being run, returning a
    job when done.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SidServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetJob': grpc.unary_unary_rpc_method_handler(
          servicer.GetJob,
          request_deserializer=sid__pb2.HealthStatus.FromString,
          response_serializer=sid__pb2.Job.SerializeToString,
      ),
      'AddJob': grpc.unary_unary_rpc_method_handler(
          servicer.AddJob,
          request_deserializer=sid__pb2.Job.FromString,
          response_serializer=sid__pb2.Job.SerializeToString,
      ),
      'AddRepo': grpc.unary_unary_rpc_method_handler(
          servicer.AddRepo,
          request_deserializer=sid__pb2.Repo.FromString,
          response_serializer=sid__pb2.Repo.SerializeToString,
      ),
      'Login': grpc.unary_unary_rpc_method_handler(
          servicer.Login,
          request_deserializer=sid__pb2.LoginRequest.FromString,
          response_serializer=sid__pb2.Token.SerializeToString,
      ),
      'ChangePass': grpc.unary_unary_rpc_method_handler(
          servicer.ChangePass,
          request_deserializer=sid__pb2.LoginRequest.FromString,
          response_serializer=sid__pb2.Token.SerializeToString,
      ),
      'GetRepos': grpc.unary_stream_rpc_method_handler(
          servicer.GetRepos,
          request_deserializer=sid__pb2.Repo.FromString,
          response_serializer=sid__pb2.Repo.SerializeToString,
      ),
      'GetJobs': grpc.unary_stream_rpc_method_handler(
          servicer.GetJobs,
          request_deserializer=sid__pb2.Repo.FromString,
          response_serializer=sid__pb2.Job.SerializeToString,
      ),
      'HealthStatusCheckIn': grpc.stream_unary_rpc_method_handler(
          servicer.HealthStatusCheckIn,
          request_deserializer=sid__pb2.HealthStatus.FromString,
          response_serializer=sid__pb2.CheckInResponse.SerializeToString,
      ),
      'RecordJobRun': grpc.stream_unary_rpc_method_handler(
          servicer.RecordJobRun,
          request_deserializer=sid__pb2.JobRunEvent.FromString,
          response_serializer=sid__pb2.Job.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'sid.Sid', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
