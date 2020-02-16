import React from "react";
import {Container, Item} from "semantic-ui-react";
import {Repo} from "../proto/sid_pb";


type RepoInfoProps = {
    repo: Repo.AsObject
}

const RepoInfo: React.FC<RepoInfoProps> = ({repo}) => (
    <Container>
        <Item.Group relaxed>
            <Item>
                <Item.Content>
                    <Item.Header as='h2'>{repo.name}</Item.Header>
                    <Item.Meta>
                        <span>{repo.sshUrl}</span>
                    </Item.Meta>
                    <Item.Description>Added at: {repo.addedAt}<br/>Added by: {repo.addedBy}</Item.Description>
                </Item.Content>
            </Item>
        </Item.Group>
    </Container>
);

export default RepoInfo;