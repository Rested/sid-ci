import { Action } from 'redux';
import { Job, Repo } from '../proto/sid_pb';
import { GrpcAction, grpcRequest } from '../middleware/grpc';
import {grpc}  from '@improbable-eng/grpc-web';
import { Sid } from '../proto/sid_pb_service';

export const JOBS_INIT = 'JOBS_INIT';
export const ADD_JOB = 'ADD_JOB';
export const SELECT_JOB = 'SELECT_JOB';

type AddJob = {
    type: typeof ADD_JOB,
    payload: Job,
};
export const addJob = (repo: Job) => ({ type: ADD_JOB, payload: repo });

type ListJobsInit = {
    type: typeof JOBS_INIT,
    payload: string
};
export const listJobsInit = (repoSshUrl: string): ListJobsInit => ({type: JOBS_INIT, payload: repoSshUrl});

export const listJobs = (repoSshUrl: string) => {
    const repo = new Repo();
    repo.setSshUrl(repoSshUrl);
    return grpcRequest<Repo,Job>({
        request: repo,
        onStart: () => listJobsInit(repoSshUrl),
        onEnd: (code: grpc.Code, message: string | undefined, trailers: grpc.Metadata): Action | void => {
            console.log(code, message, trailers);
            return;
        },
        host: 'http://localhost:8080',
        methodDescriptor: Sid.GetJobs,
        onMessage: message => {
            if (message){
                return addJob(message)
            }
            return
        },
    });
};

type SelectJob = {
    type: typeof SELECT_JOB,
    payload: string,
};
export const selectJob = (jobUuid: string): SelectJob => ({ type: SELECT_JOB, payload: jobUuid });

export type JobActionTypes =
    | ListJobsInit
    | AddJob
    | SelectJob
    | GrpcAction<Job, Repo>;