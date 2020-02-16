import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators, Dispatch} from 'redux';
import {RootState} from '../store';
import {Container, Grid, Menu} from 'semantic-ui-react';
import RootAction from '../actions';
import {listRepos, selectRepo} from '../actions/repos';
import {Repo} from '../proto/sid_pb';
import RepoJobs from "./RepoJobs";

type ReposProps = {
    repos: Repo.AsObject[],
    loading: boolean,
    error: Error | null,
    selected: Repo.AsObject | null,

    fetchRepos: () => void,
    selectRepo: (id: string) => void,
};

class Repos extends React.Component<ReposProps, {}> {

    componentDidMount() {
        this.props.fetchRepos();
    }

    render() {
        return (
            <Container style={{padding: '1em'}} fluid={true}>

                <Grid columns={2} divided>
                    <Grid.Column width={4} stretched>
                        <Menu vertical fluid>
                            {this.props.repos.map(repo => (
                                <Menu.Item name={repo.name} active={repo.sshUrl === this.props.selected?.sshUrl}
                                           onClick={() => this.props.selectRepo(repo.sshUrl)}/>
                            ))}
                        </Menu>
                    </Grid.Column>

                    <Grid.Column width={4} stretched={true}>
                        <RepoJobs/>
                    </Grid.Column>
                </Grid>

            </Container>
        );
    }

}

function mapStateToProps(state: RootState) {
    return {
        repos: Object.keys(state.repos.repos).map(key => state.repos.repos[key]),
        loading: state.repos.loading,
        error: state.repos.error,
        selected: state.repos.selected,
    };
}

function mapDispatchToProps(dispatch: Dispatch<RootAction>) {
    return bindActionCreators({
        fetchRepos: listRepos,
        selectRepo: selectRepo
    }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(Repos);