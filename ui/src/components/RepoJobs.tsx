import React, {useEffect} from 'react';
import {Container} from "semantic-ui-react";
import {Job} from "../proto/sid_pb";
import {RootState} from "../store";
import {bindActionCreators, Dispatch} from "redux";
import RootAction from "../actions";
import {listJobs, selectJob} from "../actions/jobs";
import {connect} from "react-redux";


type RepoJobsProps = {
    jobs: Job.AsObject[]
    loading: boolean,
    error: Error | null,
    selected: Job.AsObject | null,
    repoSshUrl: string | null,

    fetchJobs: (repoSshUrl: string) => void,
    selectJob: (uuid: string) => void
}

const RepoJobs: React.FC<RepoJobsProps> = ({repoSshUrl, loading, jobs, error, selected, fetchJobs, selectJob}) => {

    useEffect(() => {
        if (repoSshUrl) fetchJobs(repoSshUrl);
    }, [repoSshUrl]);
    if (!repoSshUrl){
        return null
    }
    if (loading) {
        return <div>loading...</div>
    }

    return (
        <Container>
            {jobs.map( j => <div onClick={()=> selectJob(j.jobUuid)}>{JSON.stringify(j)}</div>)}
        </Container>
    );
};

function mapStateToProps(state: RootState) {
    const {jobs} = state;
    return {
        ...jobs,
        jobs: Object.keys(jobs.jobs).map(uuid => jobs.jobs[uuid]),
        repoSshUrl: state.repos.selected ? state.repos.selected?.sshUrl : null
    }
}

function mapDispatchToProps(dispatch: Dispatch<RootAction>) {
    return bindActionCreators({
        fetchJobs: listJobs,
        selectJob: selectJob,
    }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(RepoJobs)