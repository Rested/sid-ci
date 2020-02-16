import React, {useEffect} from 'react';
import {Container, Menu} from "semantic-ui-react";
import {Job, Repo} from "../proto/sid_pb";
import {RootState} from "../store";
import {bindActionCreators, Dispatch} from "redux";
import RootAction from "../actions";
import {listJobs, selectJob} from "../actions/jobs";
import {connect} from "react-redux";
import RepoInfo from "./RepoInfo";


type RepoJobsProps = {
    jobs: Job.AsObject[]
    loading: boolean,
    error: Error | null,
    selected: Job.AsObject | null,
    selectedRepo: Repo.AsObject | null,

    fetchJobs: (repoSshUrl: string) => void,
    selectJob: (uuid: string) => void
}

const RepoJobs: React.FC<RepoJobsProps> = ({selectedRepo, loading, jobs, error, selected, fetchJobs, selectJob}) => {

    useEffect(() => {
        if (selectedRepo) fetchJobs(selectedRepo.sshUrl);
    }, [selectedRepo, fetchJobs]);
    if (!selectedRepo) {
        return null
    }
    if (loading) {
        return <div>loading...</div>
    }

    return (
        <Container>
            <RepoInfo repo={selectedRepo}/>
            <Menu fluid vertical>
                {jobs.map(job => (
                    <Menu.Item name={job.commitHexsha} active={job.jobUuid === selected?.jobUuid}
                               onClick={() => selectJob(job.jobUuid)}/>
                ))}
            </Menu>
        </Container>
    );
};

function mapStateToProps(state: RootState) {
    const {jobs} = state;
    return {
        ...jobs,
        jobs: Object.keys(jobs.jobs).map(uuid => jobs.jobs[uuid])
            .filter(job => job.repoSshUrl === state.repos.selected?.sshUrl),
        selectedRepo: state.repos.selected
    }
}

function mapDispatchToProps(dispatch: Dispatch<RootAction>) {
    return bindActionCreators({
        fetchJobs: listJobs,
        selectJob: selectJob,
    }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(RepoJobs)