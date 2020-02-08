import { applyMiddleware, combineReducers, createStore } from 'redux';
import repos, { ReposState } from './reducers/repos';
import { newGrpcMiddleware } from './middleware/grpc';

interface StoreEnhancerState {
}

export interface RootState extends StoreEnhancerState {
    repos: ReposState;
}

const reducers = combineReducers<RootState>({
    repos,
});

export default createStore(
    reducers,
    applyMiddleware(
        newGrpcMiddleware(),
    )
);