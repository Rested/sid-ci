import RootAction from '../actions';
import { ADD_REPO, SELECT_REPO, REPOS_INIT } from '../actions/repos';
import { Repo } from '../proto/sid_pb';

export type ReposState = {
    readonly repos: { [repoSshUrl: string]: Repo.AsObject },
    readonly error: Error | null,
    readonly loading: boolean,
    readonly selected: Repo.AsObject | null,
};

const initialState = {
    repos: {},
    error: null,
    loading: false,
    selected: null,
};

export default function (state: ReposState = initialState, action: RootAction): ReposState {

    switch (action.type) {

        case REPOS_INIT:
            return {...state, loading: true};

        case ADD_REPO:
            const repo: Repo.AsObject = action.payload.toObject();
            const selected = state.selected !== null ? state.selected : repo;
            if (repo) {
                return {
                    ...state,
                    loading: false,
                    repos: {...state.repos, [repo.sshUrl]: repo},
                    selected,
                };
            }
            return state;

        case SELECT_REPO:
            return {...state, selected: state.repos[action.payload]};

        default:
            return state;
    }

}