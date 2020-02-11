// package: sid
// file: sid.proto

var sid_pb = require("./sid_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var Sid = (function () {
  function Sid() {}
  Sid.serviceName = "sid.Sid";
  return Sid;
}());

Sid.GetJob = {
  methodName: "GetJob",
  service: Sid,
  requestStream: false,
  responseStream: false,
  requestType: sid_pb.HealthStatus,
  responseType: sid_pb.Job
};

Sid.AddJob = {
  methodName: "AddJob",
  service: Sid,
  requestStream: false,
  responseStream: false,
  requestType: sid_pb.Job,
  responseType: sid_pb.Job
};

Sid.AddRepo = {
  methodName: "AddRepo",
  service: Sid,
  requestStream: false,
  responseStream: false,
  requestType: sid_pb.Repo,
  responseType: sid_pb.Repo
};

Sid.Login = {
  methodName: "Login",
  service: Sid,
  requestStream: false,
  responseStream: false,
  requestType: sid_pb.LoginRequest,
  responseType: sid_pb.Token
};

Sid.ChangePass = {
  methodName: "ChangePass",
  service: Sid,
  requestStream: false,
  responseStream: false,
  requestType: sid_pb.LoginRequest,
  responseType: sid_pb.Token
};

Sid.GetRepos = {
  methodName: "GetRepos",
  service: Sid,
  requestStream: false,
  responseStream: true,
  requestType: sid_pb.Repo,
  responseType: sid_pb.Repo
};

Sid.GetJobs = {
  methodName: "GetJobs",
  service: Sid,
  requestStream: false,
  responseStream: true,
  requestType: sid_pb.Repo,
  responseType: sid_pb.Job
};

Sid.HealthStatusCheckIn = {
  methodName: "HealthStatusCheckIn",
  service: Sid,
  requestStream: true,
  responseStream: false,
  requestType: sid_pb.HealthStatus,
  responseType: sid_pb.CheckInResponse
};

Sid.RecordJobRun = {
  methodName: "RecordJobRun",
  service: Sid,
  requestStream: true,
  responseStream: false,
  requestType: sid_pb.JobRunEvent,
  responseType: sid_pb.Job
};

exports.Sid = Sid;

function SidClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

SidClient.prototype.getJob = function getJob(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Sid.GetJob, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

SidClient.prototype.addJob = function addJob(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Sid.AddJob, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

SidClient.prototype.addRepo = function addRepo(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Sid.AddRepo, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

SidClient.prototype.login = function login(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Sid.Login, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

SidClient.prototype.changePass = function changePass(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Sid.ChangePass, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

SidClient.prototype.getRepos = function getRepos(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(Sid.GetRepos, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onMessage: function (responseMessage) {
      listeners.data.forEach(function (handler) {
        handler(responseMessage);
      });
    },
    onEnd: function (status, statusMessage, trailers) {
      listeners.status.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners.end.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners = null;
    }
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

SidClient.prototype.getJobs = function getJobs(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(Sid.GetJobs, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onMessage: function (responseMessage) {
      listeners.data.forEach(function (handler) {
        handler(responseMessage);
      });
    },
    onEnd: function (status, statusMessage, trailers) {
      listeners.status.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners.end.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners = null;
    }
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

SidClient.prototype.healthStatusCheckIn = function healthStatusCheckIn(metadata) {
  var listeners = {
    end: [],
    status: []
  };
  var client = grpc.client(Sid.HealthStatusCheckIn, {
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport
  });
  client.onEnd(function (status, statusMessage, trailers) {
    listeners.status.forEach(function (handler) {
      handler({ code: status, details: statusMessage, metadata: trailers });
    });
    listeners.end.forEach(function (handler) {
      handler({ code: status, details: statusMessage, metadata: trailers });
    });
    listeners = null;
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    write: function (requestMessage) {
      if (!client.started) {
        client.start(metadata);
      }
      client.send(requestMessage);
      return this;
    },
    end: function () {
      client.finishSend();
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

SidClient.prototype.recordJobRun = function recordJobRun(metadata) {
  var listeners = {
    end: [],
    status: []
  };
  var client = grpc.client(Sid.RecordJobRun, {
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport
  });
  client.onEnd(function (status, statusMessage, trailers) {
    listeners.status.forEach(function (handler) {
      handler({ code: status, details: statusMessage, metadata: trailers });
    });
    listeners.end.forEach(function (handler) {
      handler({ code: status, details: statusMessage, metadata: trailers });
    });
    listeners = null;
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    write: function (requestMessage) {
      if (!client.started) {
        client.start(metadata);
      }
      client.send(requestMessage);
      return this;
    },
    end: function () {
      client.finishSend();
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

exports.SidClient = SidClient;

