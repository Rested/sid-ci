import { Action } from 'redux';
import { Repo } from '../proto/sid_pb';
import { GrpcAction, grpcRequest } from '../middleware/grpc';
import {grpc}  from '@improbable-eng/grpc-web';
import { Sid } from '../proto/sid_pb_service';

export const REPOS_INIT = 'REPOS_INIT';
export const ADD_REPO = 'ADD_REPO';
export const SELECT_REPO = 'SELECT_REPO';

type AddRepo = {
    type: typeof ADD_REPO,
    payload: Repo,
};
export const addRepo = (repo: Repo) => ({ type: ADD_REPO, payload: repo });

type ListReposInit = {
    type: typeof REPOS_INIT,
};
export const listReposInit = (): ListReposInit => ({type: REPOS_INIT});

export const listRepos = () => {
    const repo = new Repo();
    repo.setEnabled(true);
    return grpcRequest<Repo, Repo>({
        request: repo,
        onStart: () => listReposInit(),
        onEnd: (code: grpc.Code, message: string | undefined, trailers: grpc.Metadata): Action | void => {
            console.log(code, message, trailers);
            return;
        },
        host: 'http://localhost:8080',
        methodDescriptor: Sid.GetRepos,
        onMessage: message => {
            if (message){
                return addRepo(message)
            }
            return
        },
    });
};

type SelectRepo = {
    type: typeof SELECT_REPO,
    payload: string,
};
export const selectRepo = (repoSshUrl: string): SelectRepo => ({ type: SELECT_REPO, payload: repoSshUrl });

export type RepoActionTypes =
    | ListReposInit
    | AddRepo
    | SelectRepo
    | GrpcAction<Repo, Repo>;