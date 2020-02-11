import { applyMiddleware, combineReducers, createStore } from 'redux';
import repos, { ReposState } from './reducers/repos';
import jobs, {JobsState} from "./reducers/jobs";
import { newGrpcMiddleware } from './middleware/grpc';

interface StoreEnhancerState {
}

export interface RootState extends StoreEnhancerState {
    repos: ReposState;
    jobs: JobsState;
}

const reducers = combineReducers<RootState>({
    repos,
    jobs,
});

export default createStore(
    reducers,
    applyMiddleware(
        newGrpcMiddleware(),
    )
);