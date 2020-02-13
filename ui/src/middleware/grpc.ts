import {Action, AnyAction, Dispatch, Middleware, MiddlewareAPI} from 'redux';
import { grpc } from '@improbable-eng/grpc-web';
import * as jspb from 'google-protobuf';

const GRPC_WEB_REQUEST = 'GRPC_WEB_REQUEST';
grpc.setDefaultTransport(grpc.WebsocketTransport())
// Descriptor of a grpc-web payload
// life-cycle methods mirror grpc-web but allow for an action to be dispatched when triggered
export type GrpcActionPayload<RequestType extends jspb.Message, ResponseType extends jspb.Message> = {
    // The method descriptor to use for a gRPC request, equivalent to grpc.invoke(methodDescriptor, ...)
    methodDescriptor: grpc.MethodDefinition<RequestType, ResponseType>,
    // The transport to use for grpc-web, automatically selected if empty
    transport?: grpc.TransportFactory,
    // toggle debug messages
    debug?: boolean,
    // the URL of a host this request should go to
    host: string,
    // An instance of of the request message
    request: RequestType,
    // Additional metadata to attach to the request, the same as grpc-web
    metadata?: grpc.Metadata.ConstructorArg,
    // Called immediately before the request is started, useful for toggling a loading status
    onStart?: () => Action | void,
    // Called when response headers are received
    onHeaders?: (headers: grpc.Metadata) => Action | void,
    // Called on each incoming message
    onMessage?: (res: ResponseType) => Action | void,
    // Called at the end of a request, make sure to check the exit code
    onEnd: (code: grpc.Code, message: string, trailers: grpc.Metadata) => Action | void,
};

// Basic type for a gRPC Action
export type GrpcAction<RequestType extends jspb.Message, ResponseType extends jspb.Message> = {
    type: typeof GRPC_WEB_REQUEST,
    payload: GrpcActionPayload<RequestType, ResponseType>,
};

// Action creator, Use it to create a new grpc action
export function grpcRequest<RequestType extends jspb.Message, ResponseType extends jspb.Message>(
    payload: GrpcActionPayload<RequestType, ResponseType>
): GrpcAction<RequestType, ResponseType> {
    return {
        type: GRPC_WEB_REQUEST,
        payload,
    };
}

/* tslint:disable:no-any*/
export function newGrpcMiddleware(): Middleware {
    return ({getState, dispatch}: MiddlewareAPI<any>) => (next: Dispatch) => (action: AnyAction) => {
        // skip non-grpc actions
        if (!isGrpcWebUnaryAction(action)) {
            return next(action);
        }

        const payload = action.payload;

        if (payload.onStart) {
            payload.onStart();
        }

        grpc.invoke(payload.methodDescriptor, {
            debug: payload.debug,
            host: payload.host,
            request: payload.request,
            metadata: payload.metadata,
            transport: payload.transport,
            onHeaders: headers => {
                if (!payload.onHeaders) { return; }
                const actionToDispatch = payload.onHeaders(headers);
                return actionToDispatch && dispatch(actionToDispatch);
            },
            onMessage: res => {
                if (!payload.onMessage) { return; }
                const actionToDispatch = payload.onMessage(res as jspb.Message);
                return actionToDispatch && dispatch(actionToDispatch);
            },
            onEnd: (code, msg, trailers) => {
                const actionToDispatch = payload.onEnd(code, msg, trailers);
                return actionToDispatch && dispatch(actionToDispatch);
            },
        });

        return next(action);
    };
}

function isGrpcWebUnaryAction(action: any): action is GrpcAction<jspb.Message, jspb.Message> {
    return action && action.type && action.type === GRPC_WEB_REQUEST && isGrpcWebPayload(action);
}

function isGrpcWebPayload(action: any): boolean {
    return action &&
        action.payload &&
        action.payload.methodDescriptor &&
        action.payload.request &&
        action.payload.onEnd &&
        action.payload.host;
}

// based on: https://github.com/easyCZ/grpc-web-hacker-news/blob/master/app/src/middleware/grpc.ts