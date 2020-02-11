import RootAction from '../actions';
import { ADD_JOB, SELECT_JOB, JOBS_INIT } from '../actions/jobs';
import { Job } from '../proto/sid_pb';

export type JobsState = {
    readonly jobs: { [jobUuid: string]: Job.AsObject },
    readonly error: Error | null,
    readonly loading: boolean,
    readonly selected: Job.AsObject | null,
};

const initialState = {
    jobs: {},
    error: null,
    loading: false,
    selected: null,
};

export default function (state: JobsState = initialState, action: RootAction): JobsState {

    switch (action.type) {

        case JOBS_INIT:
            return {...state, loading: true};

        case ADD_JOB:
            const job: Job.AsObject = action.payload.toObject();
            const selected = state.selected !== null ? state.selected : job;
            if (job) {
                return {
                    ...state,
                    loading: false,
                    jobs: {...state.jobs, [job.jobUuid]: job},
                    selected,
                };
            }
            return state;

        case SELECT_JOB:
            return {...state, selected: state.jobs[action.payload]};

        default:
            return state;
    }

}